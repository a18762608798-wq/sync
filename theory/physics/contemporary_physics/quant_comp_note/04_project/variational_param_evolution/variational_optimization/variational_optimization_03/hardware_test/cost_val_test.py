import sys
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from get_initial_state import get_initial_state
from get_evolution_qc import get_evolution_qc
from get_op import get_ssh_constrained_H
from get_cost_val import get_cost_val


TARGET_QUBITS = [126, 127, 128, 129, 142, 141, 140, 139]


def get_cost(n=0, chip="qiskit_aer", theta=5e-4):
    initial_state = get_initial_state()
    evolution_qc = get_evolution_qc(initial_state, theta, theta, n=n)
    cost_op = get_ssh_constrained_H(1)
    chip_options = {
        "shot_num": 1024 * 20,
        "name": theta,
        "target_qubits": TARGET_QUBITS,
    }
    cost_val = get_cost_val(evolution_qc, cost_op, chip=chip, chip_options=chip_options)
    print(f"theta = {theta} ({chip}) =>", cost_val)
    return float(cost_val)


if __name__ == "__main__":
    results = []

    print("=" * 50)
    print("quark平台允许的角度下限(猜的)以上")
    for theta in [2.5e-3, 2e-3, 1.5e-3, 1e-3, 5.1e-4]:
        for chip in ["qiskit_aer", "Baihua"]:
            cost_val = get_cost(n=0, chip=chip, theta=theta)
            results.append({"chip": chip, "theta": theta, "cost_val": cost_val})

    print("=" * 50)
    print("quark平台允许的角度下限(猜的)以下")
    for theta in [1.1e-4, 5.1e-5]:
        for chip in ["qiskit_aer", "Baihua"]:
            cost_val = get_cost(n=0, chip=chip, theta=theta)
            results.append({"chip": chip, "theta": theta, "cost_val": cost_val})

    data_dir = HERE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    out_path = data_dir / "cost_val_test_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")
