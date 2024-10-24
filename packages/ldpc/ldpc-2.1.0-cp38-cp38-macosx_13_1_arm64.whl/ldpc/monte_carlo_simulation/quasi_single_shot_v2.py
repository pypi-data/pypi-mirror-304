# from Timo and Lucas' paper https://github.com/cda-tum/mqt-qecc/tree/analog-information-decoding/src/mqt/qecc/analog_information_decoding
from typing import List, Optional

import numpy as np
from pymatching import Matching

from data_utils import _check_convergence, create_outpath, BpParams
from ldpc.bplsd_decoder import BpLsdDecoder
from ldpc.bposd_decoder import BpOsdDecoder
from memory_experiment_v2 import (
    build_multiround_pcm,
    move_syndrome, decode_multiround,
)
from simulation_utils import (
    is_logical_err,
    save_results,
    error_channel_setup,
    set_seed,
    generate_err,
    generate_syndr_err,
    get_sigma_from_syndr_er,
    get_noisy_analog_syndrome,
    get_binary_from_analog,
)


class QSS_SimulatorV2:
    def __init__(
            self,
            H: np.ndarray,
            per: float,
            ser: float,
            L: np.ndarray,
            bias: List[float],
            codename: str,
            bp_params: Optional[BpParams],
            decoding_method: str = "bposd",  # bposd or matching
            check_side: str = "X",
            seed: int = 666,
            analog_tg: bool = False,
            repetitions: int = 0,
            rounds: int = 0,
            experiment: str = "qss",
            **kwargs,
    ) -> None:
        """

        :param H: parity-check matrix of code
        :param per: physical data error rate
        :param ser: syndrome error rate
        :param L: logical matrix
        :param bias: bias array
        :param codename: name of the code
        :param bp_params: BP decoder parameters
        :param check_side: side of the check (X or Z)
        :param seed: random seed
        :param analog_tg: switch analog decoding on/off
        :param repetitions: number of total syndrome measurements, i.e., total time steps. Must be even.
        :param rounds: number of decoding runs, i.e., number of times we slide the window - 1
        :param experiment: name of experiment, for outpath creation
        :param kwargs:
        """
        self.H = H
        self.data_err_rate = per
        self.syndr_err_rate = ser
        self.check_side = check_side
        self.L = L
        self.bias = bias
        self.codename = codename
        self.bp_params = bp_params
        self.decoding_method = decoding_method
        self.save_interval = kwargs.get("save_interval", 50)
        self.eb_precission = kwargs.get("eb_precission", 1e-2)
        self.analog_tg = analog_tg
        self.repetitions = repetitions
        if repetitions % 2 != 0:
            raise ValueError("repetitions must be even")

        if self.decoding_method not in ["bposd", "matching", "lsd"]:
            raise ValueError("Decoding method must be either bposd or matching")

        if self.repetitions % 2 != 0:
            raise ValueError("Repetitions must be even!")

        self.rounds = rounds
        self.experiment = experiment
        set_seed(seed)
        # load code parameters
        self.code_params = eval(
            open(
                f"/home/luca/Documents/codeRepos/ss-cats/single-shot-cats/codes/lifted-product/3d_ldpc/code_params.txt").read()
        )
        self.input_values = self.__dict__.copy()

        self.outfile = create_outpath(**self.input_values)

        # Remove Arrays
        del self.input_values["H"]
        del self.input_values["L"]

        self.num_checks, self.num_qubits = self.H.shape

        self.x_bit_chnl, self.y_bit_chnl, self.z_bit_chnl = error_channel_setup(
            error_rate=self.data_err_rate,
            xyz_error_bias=bias,
            N=self.num_qubits,
        )
        self.x_syndr_err_chnl, self.y_syndr_err_chnl, self.z_syndr_err_chnl = error_channel_setup(
            error_rate=self.syndr_err_rate,
            xyz_error_bias=bias,
            N=self.num_checks,
        )
        if self.check_side == "X":
            self.err_idx = 1
            # Z bit/syndrome errors
            self.data_err_channel = self.y_bit_chnl + self.z_bit_chnl
            self.syndr_err_channel = 1.0 * (self.z_syndr_err_chnl + self.y_syndr_err_chnl)
        else:
            # we have X errors on qubits
            self.err_idx = 0
            # X bit/syndrome errors
            self.data_err_channel = self.x_bit_chnl + self.y_bit_chnl
            self.syndr_err_channel = 1.0 * (self.x_syndr_err_chnl + self.y_syndr_err_chnl)

        # initialize the multiround parity-check matrix as described in the paper
        self.H3D = build_multiround_pcm(
            self.H, self.repetitions - 1,
        )

        # the number of columns of the diagonal check matrix of the H3D matrix
        self.check_block_size = self.num_qubits * (self.repetitions)

        channel_probs = np.zeros(self.H3D.shape[1])
        # The bits corresponding to the columns of the diagonal H-bock of H3D are initialized with the bit channel
        channel_probs[: self.check_block_size] = np.array(
            self.data_err_channel.tolist() * (self.repetitions)
        )

        # The remaining bits (corresponding to the identity block of H3D) are initialized with the syndrome error channel
        channel_probs[self.check_block_size:] = np.array(
            self.syndr_err_channel.tolist() * (self.repetitions)
        )

        # If we do ATG decoding, initialize sigma (syndrome noise strength)
        if self.analog_tg:
            self.sigma = get_sigma_from_syndr_er(
                self.syndr_err_channel[0]  # x/z + y
            )  # assumes all sigmas are the same
        else:
            self.sigma = None
        self.bp_iterations = 0
        if self.decoding_method == "bposd":
            self.decoder = BpOsdDecoder(
                self.H3D,
                error_channel=channel_probs.tolist(),
                max_iter=self.bp_params.max_bp_iter,
                bp_method="minimum_sum",
                osd_order=self.bp_params.osd_order,
                osd_method=self.bp_params.osd_method,
                ms_scaling_factor=self.bp_params.ms_scaling_factor
            )
        elif self.decoding_method == "matching":
            weights = np.log((1 - channel_probs) / channel_probs)
            self.decoder = Matching(self.H3D, weights=weights)
        elif self.decoding_method == 'lsd':
            self.decoder = BpLsdDecoder(
                self.H3D,
                error_channel=channel_probs,
                max_iter=5,
                bp_method='ms',
                ms_scaling_factor=0.6,
                schedule=self.bp_params.schedule,
                omp_thread_count=self.bp_params.omp_thread_count,
                serial_schedule_order=self.bp_params.serial_schedule_order,
                lsd_order=0
            )
        self.channel_probs = channel_probs

    def _decode_multiround(
            self,
            syndrome_mat: np.ndarray,
            analog_syndr_mat: np.ndarray,
            last_round: bool = False,
    ) -> np.ndarray:
        return decode_multiround(
            syndrome=syndrome_mat,
            H=self.H,
            decoder=self.decoder,
            repetitions=self.repetitions,
            last_round=last_round,
            analog_syndr=analog_syndr_mat,
            check_block_size=self.check_block_size,
            sigma=self.sigma,
            H3D=self.H3D if self.decoding_method == "matching" else None,  # avoid passing matrix in case not needed
            channel_probs=self.channel_probs,
            decoding_method=self.decoding_method,
        )

    def _single_sample(self) -> int:
        # prepare fresh syndrome matrix and error vector
        # each column == measurement result of a single timestep
        syndrome_mat = np.zeros(
            (self.num_checks, self.repetitions), dtype=np.int32
        )
        analog_syndr_mat = None

        if self.analog_tg:
            analog_syndr_mat = np.zeros(
                (self.num_checks, self.repetitions), dtype=np.float64
            )

        err = np.zeros(self.num_qubits, dtype=np.int32)
        cnt = 0  # counter for syndrome_mat

        for round in range(self.rounds):
            residual_err = [np.copy(err), np.copy(err)]
            err = generate_err(
                N=self.num_qubits,
                channel_probs=[
                    self.x_bit_chnl,
                    self.y_bit_chnl,
                    self.z_bit_chnl,
                ],
                residual_err=residual_err,
            )[self.err_idx]  # only first or last vector needed, depending on side (X or Z)
            noiseless_syndrome = (self.H @ err) % 2

            # add syndrome error
            if round != (self.rounds - 1):
                if self.analog_tg:
                    analog_syndrome = get_noisy_analog_syndrome(
                        noiseless_syndrome, self.sigma
                    )
                    syndrome = get_binary_from_analog(
                        analog_syndrome
                    )
                else:
                    syndrome_error = generate_syndr_err(self.syndr_err_channel)
                    syndrome = (noiseless_syndrome + syndrome_error) % 2
            else:  # last round is perfect
                syndrome = np.copy(noiseless_syndrome)
                analog_syndrome = get_noisy_analog_syndrome(
                    noiseless_syndrome, 0.0
                )  # no noise

            # fill the corresponding column of the syndrome/analog syndrome matrix
            syndrome_mat[:, cnt] += syndrome
            if self.analog_tg:
                analog_syndr_mat[:, cnt] += analog_syndrome

            cnt += 1  # move to next column of syndrome matrix

            if (cnt == self.repetitions):  # if we have filled the syndrome matrix, decode
                if round != (self.rounds - 1):  # if not last round, decode and move syndrome
                    cnt = (self.repetitions // 2)  # reset counter to start of tentative region

                    # the correction is only the correction of the commit region
                    (
                        corr,
                        syndrome_mat,
                        analog_syndr_mat,
                        bp_iters
                    ) = self._decode_multiround(
                        syndrome_mat,
                        analog_syndr_mat,
                        last_round=False,
                    )
                    # we compute the average for all rounds since this equals a single sample
                    self.bp_iterations += bp_iters / self.rounds
                    err = (err + corr) % 2
                    syndrome_mat = move_syndrome(syndrome_mat)
                    if self.analog_tg:
                        analog_syndr_mat = move_syndrome(
                            analog_syndr_mat, data_type=np.float64
                        )

                else:  # if we are in the last round, decode and stop
                    # the correction is the correction of the commit and tentative region
                    (
                        corr,
                        syndrome_mat,
                        analog_syndr_mat,
                        bp_iters
                    ) = self._decode_multiround(
                        syndrome_mat,
                        analog_syndr_mat,
                        last_round=True,
                    )
                    self.bp_iterations += bp_iters / self.rounds
                    err = (err + corr) % 2
        return int(not is_logical_err(self.L, err))

    def _save_results(self, success_cnt: int, samples: int) -> dict:
        return save_results(
            success_cnt=success_cnt,
            nr_runs=samples,
            p=self.data_err_rate,
            s=self.syndr_err_rate,
            input_vals=self.input_values,
            outfile=self.outfile,
            code_params=self.code_params,
            err_side="z" if self.check_side == "X" else "x",
            bp_iterations=self.bp_iterations,
            bp_params=self.bp_params
        )

    def run(self, samples: int = 1):
        """Returns single data point"""
        success_cnt = 0
        for run in range(1, samples + 1):
            success_cnt += self._single_sample()
            if run % self.save_interval == 1:
                self._save_results(success_cnt, run)
                if _check_convergence(
                        success_cnt, run, self.code_params, self.eb_precission):
                    print("Converged")
                    break
        return self._save_results(success_cnt, run)
