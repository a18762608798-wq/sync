import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import sys

import numpy as np
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from get_initial_state import get_initial_state
from get_op import get_ssh_constrained_H

from qmeas.estimator import (
    AerEstimatorOptions,
    EstimatorConfig,
    QuarkEstimatorOptions,
    run_estimator,
)

TARGET_QUBITS = [125, 126, 127, 128, 129, 142, 141, 140, 139, 138]


def _aer_expect(qc, obs):
    config = EstimatorConfig(
        qc=qc, observables=[obs], runner_opts=AerEstimatorOptions()
    )
    return np.real(asyncio.run(run_estimator(config))["evs"][0])


def _quark_expect(qc, obs):
    config = EstimatorConfig(
        qc=qc,
        observables=[obs],
        runner_opts=QuarkEstimatorOptions(
            chip="Baihua",
            shots=1024 * 10,
            target_qubits=TARGET_QUBITS,
            name="ssh-initial-test",
        ),
    )
    return np.real(asyncio.run(run_estimator(config))["evs"][0])


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    results = []

    print("=" * 50)
    print("The vals of pidx = 1")
    print("=" * 50)
    s = 0
    delta = 1
    state = get_initial_state(1)
    Hc = get_ssh_constrained_H(s, delta)
    aer, quark = float(_aer_expect(state, Hc)), float(_quark_expect(state, Hc))
    print(f"Aer: {aer}")
    print(f"Quark: {quark}")
    results.append({"pidx": 1, "s": s, "delta": delta, "aer": aer, "quark": quark})

    print("=" * 50)
    print("The vals of pidx = 0")
    print("=" * 50)
    s = 0.5
    delta = 0
    state = get_initial_state(0)
    Hc = get_ssh_constrained_H(s, delta)
    aer, quark = float(_aer_expect(state, Hc)), float(_quark_expect(state, Hc))
    print(f"Aer: {aer}")
    print(f"Quark: {quark}")
    results.append({"pidx": 0, "s": s, "delta": delta, "aer": aer, "quark": quark})

    print("=" * 50)
    print("The vals of pidx = -1")
    print("=" * 50)
    s = 1
    delta = 1
    state = get_initial_state(-1)
    Hc = get_ssh_constrained_H(s, delta)
    aer, quark = float(_aer_expect(state, Hc)), float(_quark_expect(state, Hc))
    print(f"Aer: {aer}")
    print(f"Quark: {quark}")
    results.append({"pidx": -1, "s": s, "delta": delta, "aer": aer, "quark": quark})

    out_path = data_dir / "initial_test_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")
