import sys
from pathlib import Path
import json
from qiskit.quantum_info.operators.channel import chi
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

DATA_DIR = HERE / "data"


N_LIST = list(range(5))
TARGET_QUBITS = [126, 127, 128, 129, 142, 141, 140, 139]


from get_initial_state import get_initial_state
from optimize_branch import optimize_branch
from get_ZNE_vals import get_ZNE_vals


def _dump(record, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {out_path}")


def save_ZNE_exemplary(s, chip="qiskit_aer", chip_options=None, out_path=None):
    # optimize and get the params
    direct_optimizer = DIRECT_L(
        max_evals=500,
    )
    slsqp_optimizer = SLSQP(
        maxiter=1000,
        ftol=1e-12,
        disp=False,
    )

    initial_state = get_initial_state()
    direct_res = optimize_branch(initial_state, s=1, optimizer=direct_optimizer)
    slsqp_res = optimize_branch(
        initial_state, t0=direct_res["t"], s=1, optimizer=slsqp_optimizer
    )
    # get ZNE
    θodd, θeven = slsqp_res["t"]
    m_ls, op_vals = get_ZNE_vals(
        s, N_LIST, θodd, θeven, chip=chip, chip_options=chip_options
    )
    record = {"s": s, "chip": chip, "m": m_ls, "vals": op_vals}
    _dump(record, out_path)


def save_bell_exemplary(s, chip="qiskit_aer", chip_options=None, out_path=None):
    # get ZNE
    θodd, θeven = 5.1e-4, 5.1e-4
    m_ls, op_vals = get_ZNE_vals(
        s, N_LIST, θodd, θeven, chip=chip, chip_options=chip_options
    )
    record = {"s": s, "chip": chip, "m": m_ls, "vals": op_vals}
    _dump(record, out_path)


if __name__ == "__main__":
    s = 1
    chip_options = {
        "shot_num": 1024 * 10,
        "correction": False,
        "name": f"s = {s}",
        # "target_qubits": TARGET_QUBITS,
    }
    save_ZNE_exemplary(
        s,
        chip="Shenglian",
        chip_options=chip_options,
        out_path=DATA_DIR / "ZNE_exemplary.json",
    )
    save_bell_exemplary(
        s,
        chip="Shenglian",
        chip_options=chip_options,
        out_path=DATA_DIR / "bell_ZNE_exemplary.json",
    )
