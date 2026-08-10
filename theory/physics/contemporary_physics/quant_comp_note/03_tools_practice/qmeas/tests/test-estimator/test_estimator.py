import asyncio
import os

import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

from qmeas.estimator import (
    AerEstimatorOptions,
    EstimatorConfig,
    QuarkEstimatorOptions,
    group_qubitwise,
    run_estimator,
)


def _example_qc() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx([0], [1])
    return qc


def _observables():
    return [
        SparsePauliOp(["XX"], coeffs=[1.0]),
        SparsePauliOp(["YY"], coeffs=[1.0]),
        SparsePauliOp(["ZZ"], coeffs=[1.0]),
    ]


if __name__ == "__main__":
    # group_qubitwise check
    groups, bases = group_qubitwise(_observables())
    print("groups:", [g.to_labels() for g in groups])
    print("bases:", [str(b) for b in bases])

    # Aer EstimatorV2 check
    qc = _example_qc()

    aer_config = EstimatorConfig(
        qc=qc,
        observables=_observables(),
        runner_opts=AerEstimatorOptions(),
    )
    result = asyncio.run(run_estimator(aer_config))
    print("aer evs:", result["evs"])

    # Baihua check
    Baihua_config = EstimatorConfig(
        qc=qc,
        observables=_observables(),
        runner_opts=QuarkEstimatorOptions(
            chip="Baihua",
            shots=1024,
            target_qubits=[138, 125],
            name="Baihua-estimator-check",
        ),
    )
    result = asyncio.run(run_estimator(Baihua_config))
    print("Baihua evs:", result["evs"])
