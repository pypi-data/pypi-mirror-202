# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Molecular Hamiltonian measurement."""

from isqlab.circuits import QuantumCircuit
from openfermion.ops.operators import QubitOperator
from typing import Tuple, List
import numpy as np


def hamiltonian_measure(
    circuit: QuantumCircuit,
    qubit_hamiltonian: QubitOperator,
    **params,
) -> np.float64:
    """transform qubit hamiltonian to pauli measurements."""

    coeffs, gates = _openfermion_to_pauligates(qubit_hamiltonian)
    measure_results = [1.0, ]
    for gate in gates:
        circuit.pauli(gate, format="openfermion")
        # circuit.pauli(gate, format="str")
        measure_results.append(circuit.pauli_measure(**params))
    return np.dot(measure_results, coeffs)


def _openfermion_to_pauligates(
    qubit_hamiltonian: QubitOperator,
) -> Tuple[List[float], List[str]]:
    """
    extract coefficients and gates of qubit hamiltonian.
    """
    coeffs = []
    gates = []
    for gate, coeff in qubit_hamiltonian.terms.items():
        coeffs.append(coeff)
        gates.append(gate)
    return coeffs, gates[1:]

    # hamiltonian_strs = str(qubit_hamiltonian).split("\n")
    # hamiltonian_strs[-1] += " +"
    #
    # coeffs = []
    # gates = []
    #
    # for hamiltonian_str in hamiltonian_strs:
    #     hamiltonian_ele = hamiltonian_str.split(" ")
    #     coeffs.append(float(hamiltonian_ele[0]))
    #     gates.append("".join(hamiltonian_ele[1:-1])[1:-1])
    # # the first gate is None
    # return coeffs, gates[1:]
