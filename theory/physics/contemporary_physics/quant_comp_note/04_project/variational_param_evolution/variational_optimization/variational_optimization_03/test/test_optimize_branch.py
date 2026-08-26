import sys
from pathlib import Path
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from get_initial_state import get_initial_state
from optimize_branch import optimize_branch


def main():
    direct_optimizer = DIRECT_L(
        max_evals=1000,
    )
    slsqp_optimizer = SLSQP(
        maxiter=5000,
        ftol=1e-12,
        disp=False,
    )

    initial_state = get_initial_state()
    direct_res = optimize_branch(initial_state, s=1, optimizer=direct_optimizer)
    slsqp_res = optimize_branch(
        initial_state, x0=direct_res["x"], s=1, optimizer=slsqp_optimizer
    )
    print(slsqp_res)


if __name__ == "__main__":
    main()
