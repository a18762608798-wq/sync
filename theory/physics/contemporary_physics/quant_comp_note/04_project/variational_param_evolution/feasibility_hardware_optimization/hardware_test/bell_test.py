import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json

import numpy as np
from qiskit import QuantumCircuit
from tqdm import tqdm
from qiskit.quantum_info import SparsePauliOp
from qmeas.estimator import (
    AerEstimatorOptions,
    EstimatorConfig,
    QuarkEstimatorOptions,
    run_estimator,
)

TARGET_QUBITS = []
TARGET_QUBITS.append([2, 3, 4, 5, 6, 19, 18, 17, 16, 15])
TARGET_QUBITS.append(list(range(69, 74)) + list(range(86, 81, -1)))
TARGET_QUBITS.append(list(range(125, 130)) + list(range(142, 137, -1)))


def _bell_qc() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx([0], [1])
    return qc


def _bell_obs():
    return [
        SparsePauliOp(["XX"], coeffs=[1.0]),
        SparsePauliOp(["YY"], coeffs=[1.0]),
        SparsePauliOp(["ZZ"], coeffs=[1.0]),
    ]


def _bell_quarkoptions(target_qubits):
    return QuarkEstimatorOptions(
        chip="Baihua",
        shots=1024 * 10,
        target_qubits=target_qubits,
        name="Baihua-estimator-check",
    )


def bell_aer():
    qc = _bell_qc()
    aer_config = EstimatorConfig(
        qc=qc,
        observables=_bell_obs(),
        runner_opts=AerEstimatorOptions(),
    )
    result = asyncio.run(run_estimator(aer_config))
    return result


def bell_quark(target_qubits):
    qc = _bell_qc()
    baihua_config = EstimatorConfig(
        qc=qc,
        observables=_bell_obs(),
        runner_opts=_bell_quarkoptions(target_qubits),
    )
    return asyncio.run(run_estimator(baihua_config))


if __name__ == "__main__":
    print(f"Aer bell res: {bell_aer()['evs']}")

    pairs = []
    for qubits in TARGET_QUBITS:
        for bit_idx in range(len(qubits) - 1):
            pairs.append((qubits[bit_idx], qubits[bit_idx + 1]))
        pairs.append((qubits[-1], qubits[0]))

    def _run(pair):
        return pair, np.mean(np.abs(bell_quark(pair)["evs"]))

    res = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_run, p) for p in pairs]
        for fut in tqdm(as_completed(futures), total=len(futures), desc="bell_quark"):
            pair, value = fut.result()
            res[f"({pair[0]}, {pair[1]})"] = value
    res = dict(sorted(res.items(), key=lambda kv: kv[1]))  # 排序
    print(res)
    HERE = Path(__file__).resolve().parent
    path = HERE / "data/bell_compare.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
