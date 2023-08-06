# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""
UCC ansatzs implementation.
This file is inspired by TenCirChem and OpenFermion.
"""

from .ucc import UCC
from isqlab.circuits import QuantumCircuit
from isqlab.vqe.chem import ex_op_to_fop, reverse_qop_idx
import numpy as np
from typing import Tuple, List, Union, Sequence
from openfermion import jordan_wigner


DISCARD_EPS = 1e-12


class UCCSD(UCC):
    """UCCSD"""

    def __init__(
        self,
        mol,
        active_space=None,
        mo_coeff=None,
        pick_ex2: bool = True,
        epsilon: float = DISCARD_EPS,
        sort_ex2: bool = True,
    ) -> None:
        super().__init__(
            mol,
            active_space,
            mo_coeff,
        )

        self.pick_ex2 = pick_ex2
        self.sort_ex2 = sort_ex2

        # screen out excitation operators based on t2 amplitude
        self.t2_discard_eps = epsilon

        self.ex_ops, self.param_ids, self.init_guess = self.get_ex_ops(
            self.t1,
            self.t2,
        )
        self.num_params = self.param_ids[-1] + 1

    def get_circuit(
        self,
        params_name: str = "theta",
        ex_ops: list = None,
        param_ids: Sequence = None,
        init_state: Union[QuantumCircuit, str] = None,
        trotter: bool = True,
    ):

        if ex_ops is None:
            ex_ops = self.ex_ops

        if param_ids is None:
            param_ids = self.param_ids

        circuit = QuantumCircuit(self.n_qubits)

        if init_state:
            init_circuit = self.get_init_circuit(
                self.n_qubits, self.n_elec, init_state)
            circuit.extend(init_circuit)

        for param_id, f_idx in zip(param_ids, ex_ops):
            theta = f"{params_name}[{param_id}]"
            fop = ex_op_to_fop(f_idx, with_conjugation=True)
            qop = reverse_qop_idx(jordan_wigner(fop), self.n_qubits)
            if trotter:
                for pauli_string, value in qop.terms.items():
                    self.evolve_pauli(circuit, pauli_string, theta, value)
            else:
                raise NotImplementedError("multicontrol_ry")
                # TODO:
                # https://arxiv.org/pdf/2005.14475.pdf
                # circuit = evolve_excitation(
                #     circuit, f_idx, qop, 2 * theta, decompose_multicontrol)
        return circuit

    def get_ex_ops(
        self,
        t1: np.ndarray = None,
        t2: np.ndarray = None,
    ) -> Tuple[List[Tuple], List[int], List[float]]:
        """Get one-body and two-body excitation operators for UCCSD ansatz."""

        ex1_ops, ex1_param_ids, ex1_init_guess = self.get_ex1_ops(self.t1)
        ex2_ops, ex2_param_ids, ex2_init_guess = self.get_ex2_ops(self.t2)

        # screen out symmetrically not allowed excitation
        # ex2_ops, ex2_param_ids, ex2_init_guess = self.pick_and_sort(
        #     ex2_ops,
        #     ex2_param_ids,
        #     ex2_init_guess,
        #     self.pick_ex2,
        #     self.sort_ex2,
        # )

        ex_op = ex1_ops + ex2_ops
        param_ids = ex1_param_ids + \
            [i + max(ex1_param_ids) + 1 for i in ex2_param_ids]
        init_guess = ex1_init_guess + ex2_init_guess
        return ex_op, param_ids, init_guess

    def pick_and_sort(
        self,
        ex_ops,
        param_ids,
        init_guess,
        do_pick=True,
        do_sort=True,
    ):
        # sort operators according to amplitude
        if do_sort:
            sorted_ex_ops = sorted(
                zip(ex_ops, param_ids), key=lambda x: -np.abs(init_guess[x[1]]))
        else:
            sorted_ex_ops = list(zip(ex_ops, param_ids))
        ret_ex_ops = []
        ret_param_ids = []
        # print(sorted_ex_ops)
        # [((1, 3, 2, 0), 0)]
        # print(init_guess)
        # [0.0]
        for ex_op, param_id in sorted_ex_ops:
            # discard operators with tiny amplitude.
            # The default eps is so small that the screened out excitations are probably not allowed
            if do_pick and np.abs(init_guess[param_id]) < self.t2_discard_eps:
                continue
            ret_ex_ops.append(ex_op)
            ret_param_ids.append(param_id)
        unique_ids = np.unique(ret_param_ids)
        ret_init_guess = np.array(init_guess)[unique_ids]
        id_mapping = {old: new for new, old in enumerate(unique_ids)}
        ret_param_ids = [id_mapping[i] for i in ret_param_ids]
        return ret_ex_ops, ret_param_ids, list(ret_init_guess)
