import asyncio

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp

from qmeas.estimator import (
    AerEstimatorOptions,
    EstimatorConfig,
    QuarkEstimatorOptions,
    QubitwiseBasis,
    group_qubitwise,
    run_estimator,
)


def _example_qc() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.h(1)
    return qc


def test_group_qubitwise():
    observables = [
        SparsePauliOp(["XX", "XI", "IX"], coeffs=[1.0, 1.0, 1.0]),
        SparsePauliOp(["ZZ"], coeffs=[1.0]),
        SparsePauliOp(["YY"], coeffs=[1.0]),
    ]
    groups, meas_bases = group_qubitwise(observables)

    labels = [{p.to_label() for p in g} for g in groups]
    assert {"XX", "XI", "IX"} in labels
    assert {"ZZ"} in labels
    assert {"YY"} in labels
    assert len(groups) == 3

    bases = [str(b) for b in meas_bases]
    assert "XX" in bases
    assert "ZZ" in bases
    assert "YY" in bases


def test_recover_group_matches_analytic():
    group = PauliList(["XX", "XI", "IX"])
    basis = QubitwiseBasis()

    # |++⟩ → H⊗H|++⟩ = |00⟩ → all Z outcomes 00
    counts = {"00": 1024}
    expval = basis.recover(group, counts, shots=1024)

    assert expval[Pauli("XX")] == 1.0
    assert expval[Pauli("XI")] == 1.0
    assert expval[Pauli("IX")] == 1.0


def test_recover_group_parity():
    group = PauliList(["XI"])
    basis = QubitwiseBasis()

    # |+−⟩: X 测量 q1, H|−⟩ = |1⟩ → q1 始终为 1 → <XI> = -1
    counts = {"10": 512, "11": 512}
    expval = basis.recover(group, counts, shots=1024)

    assert expval[Pauli("XI")] == -1.0


def _observables():
    return [
        SparsePauliOp(["XX", "XI", "IX"], coeffs=[1.0, 1.0, 1.0]),
        SparsePauliOp(["ZZ"], coeffs=[1.0]),
    ]


def test_estimator_dongling():
    qc = _example_qc()
    config = EstimatorConfig(
        qc=qc,
        observables=_observables(),
        runner_opts=QuarkEstimatorOptions(
            quark_options={
                "chip": "Dongling",
                "shots": 1024,
                "name": "estimator-dongling",
            }
        ),
    )
    result = asyncio.run(run_estimator(config))
    print("dongling evs:", result["evs"])

    expected = [3.0, 0.0]
    for got, want in zip(result["evs"], expected):
        np.testing.assert_allclose(got, want, atol=0.8)


if __name__ == "__main__":
    # group_qubitwise check
    groups, bases = group_qubitwise(_observables())
    print("groups:", [g.to_labels() for g in groups])
    print("bases:", [str(b) for b in bases])

    # Aer EstimatorV2 check
    qc = _example_qc()
    expected = [3.0, 0.0]

    aer_config = EstimatorConfig(
        qc=qc,
        observables=_observables(),
        runner_opts=AerEstimatorOptions(),
    )
    result = asyncio.run(run_estimator(aer_config))
    print("aer evs:", result["evs"])
    for got, want in zip(result["evs"], expected):
        np.testing.assert_allclose(got, want, atol=1e-6)
    print("Aer EstimatorV2 check passed.")

    # Dongling check
    dongling_config = EstimatorConfig(
        qc=qc,
        observables=_observables(),
        runner_opts=QuarkEstimatorOptions(
            quark_options={
                "chip": "Dongling",
                "shots": 1024,
                "name": "dongling-estimator-check",
            }
        ),
    )
    result = asyncio.run(run_estimator(dongling_config))
    print("dongling evs:", result["evs"])
    for got, want in zip(result["evs"], expected):
        np.testing.assert_allclose(got, want, atol=0.8)
    print("Dongling Estimator check passed.")
