import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from var_optimization import inner_optimize, outer_optimize, get_branch_start


def test_get_branch_start():
    assert get_branch_start(1, 0.3) == (0, 0.3)
    assert get_branch_start(0, 0.3) == (0.3, 0)
    assert get_branch_start(-1, 0.3) == (1, 0.3)


def test_inner_optimize_output():
    best_phase_idx, best_result = inner_optimize(
        8,
        0.4,
        0.9,
        step=4,
        order=1,
        method="SLSQP",
        options={"maxiter": 100, "ftol": 0.01, "disp": False},
        disp=True,
    )
    assert best_phase_idx in (1, 0, -1)


def test_outer_optimize_output():
    best_step, best_order, best_phase_idx, best_result = outer_optimize(
        8,
        0.1,
        0.9,
        max_steps=[2],
        orders=[1],
        method="SLSQP",
        options={"maxiter": 50, "ftol": 1e-4, "disp": False},
        disp=True,
    )
    assert best_phase_idx in (1, 0, -1)
    # print(best_step, best_order, best_phase_idx, best_result.fun)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_outer"):
            fn()
            print(f"PASS {name}")
