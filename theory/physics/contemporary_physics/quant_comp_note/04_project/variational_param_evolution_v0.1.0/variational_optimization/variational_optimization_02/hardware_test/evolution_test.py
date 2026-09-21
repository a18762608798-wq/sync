import sys
from pathlib import Path
import json
import numpy as np


from qiskit_algorithms.optimizers import SPSA, DIRECT_L


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


from optimize_branch import optimize_branch
from get_cost_val import get_cost_val
from get_evolution_qc import get_qc_from_t
from get_op import get_ssh_constrained_H


TARGET_QUBITS = [125, 126, 127, 128, 129, 142, 141, 140, 139, 138]


direct_optimizer = DIRECT_L(
    max_evals=500,
)
spsa_optimizer = SPSA(
    maxiter=100,
    blocking=True,
    trust_region=True,
    resamplings=1,
)

chip_options = {
    "name": "evolution_test",
    "shot_num": 1024 * 10,
    "target_qubits": TARGET_QUBITS,
}


def run_evolution_test(end, pidx=1, step=1, order=1):
    """模拟机求最优参数 → 复现电路 → 真机求 evs. 返回 (aer_res, evs)."""
    # 模拟机上求出固定离散指标的最优参数组
    direct_res, _ = optimize_branch(
        end,
        pidx=pidx,
        step=step,
        order=order,
        t0=None,
        optimizer=direct_optimizer,
    )

    aer_res, _ = optimize_branch(
        end,
        pidx=pidx,
        step=step,
        order=order,
        t0=direct_res["t"],
        optimizer=spsa_optimizer,
    )
    print(aer_res)

    # 复现所得电路
    qc = get_qc_from_t(aer_res["t"], end, pidx=pidx, step=step, order=order)
    Hc = get_ssh_constrained_H(end[0], end[1], ϵ=1)
    evs = get_cost_val(qc, Hc, chip="Baihua", chip_options=chip_options)
    print(evs)

    return aer_res, evs


if __name__ == "__main__":
    end = [0.1, 0.9]

    tests = [
        (1, 1),
        (1, 2),
        (2, 1),
    ]

    # 存储结果
    result_dic = {}
    for step, order in tests:
        aer_res, evs = run_evolution_test(step=step, end=end, order=order)
        result_dic[f"step={step},order={order}"] = {
            "end": end,
            "aer_res": {
                "fun": aer_res["fun"],
                "t": np.asarray(aer_res["t"]).tolist(),
            },
            "quark_evs": float(evs),
        }

    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    out_path = data_dir / "evolution_test_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result_dic, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")
