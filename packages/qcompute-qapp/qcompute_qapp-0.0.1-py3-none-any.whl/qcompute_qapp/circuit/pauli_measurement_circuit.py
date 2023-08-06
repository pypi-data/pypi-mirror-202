# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) 2021 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pauli Measurement Circuit
"""

from typing import List
from copy import deepcopy
import itertools
import numpy as np
from QCompute.QPlatform.QEnv import QEnv
from QCompute.QPlatform.QRegPool import QRegPool
from QCompute.QPlatform.QOperation.RotationGate import RX, RY
from QCompute.QPlatform.QOperation.FixedGate import H, S, CX
from QCompute.QPlatform.QOperation.Measure import MeasureZ
from ..utils import grouping_hamiltonian
from .basic_circuit import BasicCircuit


class PauliMeasurementCircuit(BasicCircuit):
    r""" Pauli Measurement Circuit class
    """
    def __init__(self, num: int, pauli_terms: str):
        r"""The constructor of the PauliMeasurementCircuit class

        Args:
            num (int): Number of qubits
            pauli_terms (str): Pauli terms to be measured

        """
        super().__init__(num)
        self._pauli_terms = deepcopy(pauli_terms)

    def add_circuit(self, q: QRegPool, pauli_str: str) -> None:
        r"""Adds the pauli measurement circuit to the register

        Args:
            q (QRegPool): Quantum register to which this circuit is added
            pauli_str (str): Pauli string to be measured

        """
        for i in range(self._num):
            # Set up Pauli measurement circuit
            if pauli_str[i] == 'x':
                RY(-np.pi / 2)(q[i])
            elif pauli_str[i] == 'y':
                RX(np.pi / 2)(q[i])
        # Measure all qubits
        MeasureZ(q, list(range(len(q))))

    def get_expectation(self, preceding_circuits: List[BasicCircuit], shots: int, backend: str) -> float:
        r"""Computes the expectation value of the Pauli terms

        Args:
            preceding_circuits (List[BasicCircuit]): Circuit precedes the measurement circuit
            shots (int): Number of measurement shots
            backend (str): Backend to be used in this task

        Returns:
            float: Expectation value of the Pauli terms

        """
        expectation = 0
        for coeff, pauli_str in self._pauli_terms:
            # Return coeff if all Pauli operators are I
            if pauli_str.lower().count('i') == len(pauli_str):
                expectation += coeff
                continue
            active_qubits = [i for i, c in enumerate(pauli_str) if c != 'i']
            env = QEnv()
            env.backend(backend)
            q = env.Q.createList(self._num)
            # Add circuit
            for circuit in preceding_circuits:
                circuit.add_circuit(q)
            self.add_circuit(q, pauli_str.lower())
            # Submit job
            counts = env.commit(shots, fetchMeasure=True)['counts']
            # Expectation
            filtered_counts = [(counts[key], [key[-i - 1] for i in active_qubits]) for key in counts]
            expecval = sum([((-1) ** key.count('1')) * val / shots for val, key in filtered_counts])
            expectation += coeff * expecval

        return expectation


class PauliMeasurementCircuitWithAncilla(BasicCircuit):
    r"""Pauli Measurement Circuit with Ancilla class
    """
    def __init__(self, num: int, pauli_terms: str):
        r"""The constructor of the PauliMeasurementCircuitWithAncilla class

        Args:
            num (int): Number of qubits
            pauli_terms (str): Pauli terms to be measured

        """
        super().__init__(num)
        self._pauli_terms = pauli_terms

    def add_circuit(self, q: QRegPool, pauli_str: str) -> None:
        r"""Adds the pauli measurement circuit to the register

        Args:
            q (QRegPool): Quantum register to which this circuit is added
            pauli_str (str): Pauli string to be measured

        """
        for i in range(self._num):
            # Set up Pauli measurement circuit
            if pauli_str[i] == 'x':
                H(q[i])
                CX(q[i], q[-1])
            elif pauli_str[i] == 'y':
                S(q[i])
                H(q[i])
                CX(q[i], q[-1])
            elif pauli_str[i] == 'z':
                CX(q[i], q[-1])
        # Measure the ancilla qubit
        MeasureZ([q[-1]], [0])

    def get_expectation(self, preceding_circuits: List[BasicCircuit], shots: int, backend: str) -> float:
        r"""Computes the expectation value of the Pauli terms

        Args:
            preceding_circuits (List[BasicCircuit]): Circuit precedes the measurement circuit
            shots (int): Number of measurement shots
            backend (str): Backend to be used in this task

        Returns:
            float: Expectation value of the Pauli terms

        """
        expectation = 0
        for coeff, pauli_str in self._pauli_terms:
            # Return coeff if all Pauli operators are I
            if pauli_str.lower().count('i') == len(pauli_str):
                expectation += coeff
                continue
            env = QEnv()
            env.backend(backend)
            q = env.Q.createList(self._num + 1)
            # Add circuit
            for circuit in preceding_circuits:
                circuit.add_circuit(q[:self._num])
            self.add_circuit(q, pauli_str.lower())
            # Submit job
            counts = env.commit(shots, fetchMeasure=True)['counts']
            # Expectation
            expecval = (counts.get('0', 0) - counts.get('1', 0)) / shots
            expectation += coeff * expecval

        return expectation


class SimultaneousPauliMeasurementCircuit(BasicCircuit):
    r"""Simultaneous Pauli Measurement Circuit for Qubitwise Commute Pauli Terms
    """
    def __init__(self, num: int, pauli_terms: list):
        r"""The constructor of the SimultaneousPauliMeasurementCircuit class

        Args:
            num (int): Number of qubits
            pauli_terms (list): Pauli terms to be measured

        """
        super().__init__(num)
        self._pauli_terms = pauli_terms

    def add_circuit(self, q: 'QRegPool', clique: list) -> None:
        r"""Adds the simultaneous pauli measurement circuit to the register

        Args:
            q (QRegPool): Quantum register to which this circuit is added
            clique (list): Clique of Pauli terms to be measured together

        """
        for index in range(self._num):
            # Set up Pauli measurement circuit
            term = [pauli[index] for _, pauli in clique]
            if 'x' in term:
                RY(-np.pi / 2)(q[index])
            elif 'y' in term:
                RX(np.pi / 2)(q[index])
        # Measure all qubits
        MeasureZ(q, range(self._num))

    def _single_clique_expectation(self, clique: list, counts: dict, shots: int) -> float:
        r"""Computes the expectation value of the target Pauli clique

        Args:
            clique (list): Pauli clique
            counts (dict): measurement counts
            shots (int): number of measurements

        Returns:
            float: expectation value
        """
        # Reformulate the measurement counts in the form of a probability list
        basis = [''.join(x) for x in itertools.product('01', repeat=self._num)]
        prob = [counts.get(key, 0) / shots for key in basis]
        # Calculate the expectation value of each term in the pauli_clique according to the same measured results
        expecval = 0
        for coeff, pauli_str in clique:
            first = True
            for operator in pauli_str:
                if first:
                    eigenvalues = np.array([1.0, 1.0 if operator == 'i' else -1.0])
                    first = False
                else:
                    eigenvalues = np.kron(np.array([1.0, 1.0 if operator == 'i' else -1.0]), eigenvalues)
            expecval_index = np.dot(eigenvalues, prob)
            expecval += coeff * expecval_index

        return expecval

    def get_expectation(self, preceding_circuits: List[BasicCircuit], shots: int, backend: str) -> float:
        r"""Computes the expectation value of the Pauli terms

        Args:
            preceding_circuits (List[BasicCircuit]): Circuit precedes the measurement circuit
            shots (int): Number of measurement shots
            backend (str): Backend to be used in this task

        Returns:
            float: Expectation value of the Pauli terms
        """
        # Generate Pauli cliques for the hamiltonian graph
        cliques = grouping_hamiltonian(self._pauli_terms)
        # Calculate each
        expectation = 0
        for pauli_clique in cliques:
            env = QEnv()
            env.backend(backend)
            q = env.Q.createList(self._num)
            # Add circuit
            for circuit in preceding_circuits:
                circuit.add_circuit(q)
            self.add_circuit(q, pauli_clique)
            # Submit job
            counts = env.commit(shots, fetchMeasure=True)['counts']
            # Expectation
            result = self._single_clique_expectation(pauli_clique, counts, shots)
            expectation += result

        return expectation
