import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from var_optimization import inner_optimize, outer_optimize, get_branch_start


def test_get_branch_start():
    assert get_branch_start(1, 0.3) == (0, 0.3)
    assert get_branch_start(0, 0.3) == (0.3, 0)
    assert get_branch_start(-1, 0.3) == (1, 0.3)


def test_inner_optimize_output():
    best_phase_idx, best_result, _ = inner_optimize(
        8,
        0.4,
        0.9,
        step=1,
        order=1,
        method="COBYLA",
        chip="qiskit_aer",
        options={"maxiter": 100, "tol": 0.01, "disp": False},
        disp=True,
    )
    best_phase_idx, best_result, _ = inner_optimize(
        8,
        0.4,
        0.9,
        step=1,
        order=1,
        method="COBYLA",
        chip="Baihua",
        options={"maxiter": 100, "tol": 0.01, "disp": False},
        disp=True,
    )
    assert best_phase_idx in (1, 0, -1)


def test_outer_optimize_output():
    best_step, best_order, best_phase_idx, best_result, x0_map = outer_optimize(
        8,
        0.1,
        0.9,
        max_steps=[2],
        orders=[1],
        method="COBYLA",
        options={"maxiter": 500, "tol": 5e-2, "disp": False},
        disp=True,
    )
    print(x0_map)
    assert best_phase_idx in (1, 0, -1)
    # print(best_step, best_order, best_phase_idx, best_result.fun)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_outer"):
            fn()
            print(f"PASS {name}")
