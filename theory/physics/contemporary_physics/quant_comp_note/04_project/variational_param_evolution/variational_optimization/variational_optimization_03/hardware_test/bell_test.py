import asyncio
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

BAIHUA_TARGET_QUBITS = []
BAIHUA_TARGET_QUBITS.append([2, 3, 4, 5, 6, 19, 18, 17, 16, 15])
BAIHUA_TARGET_QUBITS.append([13, 14, 15, 16, 17, 30, 29, 28, 27, 26])
BAIHUA_TARGET_QUBITS.append([69, 70, 71, 72, 73, 86, 85, 84, 83, 82])

SHENGLIAN_TARGET_QUBITS = []
SHENGLIAN_TARGET_QUBITS.append([74, 67, 61, 68, 62, 69, 76, 82, 75, 81])


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


def _bell_quarkoptions(target_qubits, chip="Baihua"):
    return QuarkEstimatorOptions(
        chip=chip,
        shots=1024 * 20,
        target_qubits=target_qubits,
        name="Baihua-estimator-check",
    )


async def bell_aer():
    qc = _bell_qc()
    aer_config = EstimatorConfig(
        qc=qc,
        observables=_bell_obs(),
        runner_opts=AerEstimatorOptions(),
    )
    return await run_estimator(aer_config)


async def bell_quark(target_qubits, chip="Baihua"):
    qc = _bell_qc()
    baihua_config = EstimatorConfig(
        qc=qc,
        observables=_bell_obs(),
        runner_opts=_bell_quarkoptions(target_qubits, chip=chip),
    )
    return await run_estimator(baihua_config)


async def main(target_qubits, chip="Baihua"):
    aer_res = await bell_aer()
    print(f"Aer bell res: {aer_res['evs']}")

    pairs = []
    for qubits in target_qubits:
        for bit_idx in range(len(qubits) - 1):
            pairs.append((qubits[bit_idx], qubits[bit_idx + 1]))
        pairs.append((qubits[-1], qubits[0]))

    async def _run(pair):
        return pair, np.mean(np.abs((await bell_quark(pair, chip=chip))["evs"]))

    res = {}
    tasks = [asyncio.create_task(_run(p)) for p in pairs]
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="bell_quark"):
        pair, value = await coro
        res[f"({pair[0]}, {pair[1]})"] = value
    res = dict(sorted(res.items(), key=lambda kv: kv[1]))  # 排序
    print(res)
    HERE = Path(__file__).resolve().parent
    path = HERE / f"data/{chip}_bell_compare.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    asyncio.run(main(SHENGLIAN_TARGET_QUBITS, chip="Shenglian"))
    # asyncio.run(main(BAIHUA_TARGET_QUBITS, chip="Baihua"))
