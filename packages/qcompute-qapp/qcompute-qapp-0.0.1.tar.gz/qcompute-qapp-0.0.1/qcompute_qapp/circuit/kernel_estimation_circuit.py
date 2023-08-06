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
Kernel Estimation Circuit
"""

import numpy as np
from QCompute.QPlatform.QRegPool import QRegPool
from QCompute.QPlatform import Error
from QCompute.QPlatform.QOperation.Measure import MeasureZ
from .basic_circuit import BasicCircuit
from .encoding_circuit import IQPEncodingCircuit


class KernelEstimationCircuit(BasicCircuit):
    r""" Kernel Estimation Circuit class
    """
    def __init__(self, num: int, encoding_style: str):
        r"""The constructor of the KernelEstimationCircuit class

        Args:
            num (int): Number of qubits
            encoding_style (str): Encoding circuit, only accepts ``'IQP'`` for now

        """
        super().__init__(num)
        self._encoding_style = encoding_style

    def add_circuit(self, q: QRegPool, x1: np.ndarray, x2: np.ndarray) -> None:
        """Adds the kernel estimation circuit used to evaluate the kernel entry value between
        two classical data vectors

        Args:
            q (QRegPool): Quantum register to which this circuit is added
            x1 (np.ndarray): First classical vector
            x2 (np.ndarray): Second classical vector

        """

        if self._encoding_style == 'IQP':
            encoding_circuit_first = IQPEncodingCircuit(num=self._num)
            encoding_circuit_first.add_circuit(q, x1)

            encoding_circuit_second = IQPEncodingCircuit(num=self._num, inverse=True)
            encoding_circuit_second.add_circuit(q, x2)
        else:
            raise Error.ArgumentError('Error EA03001(QAPP): Encoding style not yet supported!')

        MeasureZ(q, range(self._num))
