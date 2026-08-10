import os
import sys

from qiskit.circuit.tools.pi_check import D


from qiskit_algorithms.optimizers import SPSA, SLSQP, DIRECT_L


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from var_optimization import inner_optimize, outer_optimize, get_branch_start


def test_get_branch_start():
    assert get_branch_start(1, 0.3) == (0, 0.3)
    assert get_branch_start(0, 0.3) == (0.3, 0)
    assert get_branch_start(-1, 0.3) == (1, 0.3)


def test_inner_optimize_output():
    """
    optimizer = DIRECT_L(
        max_evals=10000,
    )
    optimizer = SLSQP(
        maxiter=5000,
        ftol=1e-5,
        disp=False,
    )
    optimizer = SPSA(
        maxiter=500,
        blocking=True,
        trust_region=True,
        resamplings=1,
    )
    """
    direct_l_optimizer = DIRECT_L(max_evals=1000)
    slsqp_optimizer = SLSQP(maxiter=500, ftol=1e-12, disp=False)
    spsa_optimizer = SPSA(maxiter=1, blocking=True, trust_region=True, resamplings=1)

    # 先 DIRECT_L 全局初搜，再 SLSQP 精化，最后真机 SPSA 微调
    best_phase_idx, _, t0_map, history = inner_optimize(
        8,
        0.5,
        0.5,
        step=1,
        order=1,
        optimizer=direct_l_optimizer,
        chip="qiskit_aer",
        disp=True,
    )
    best_phase_idx, _, t0_map, _ = inner_optimize(
        8,
        0.5,
        0.5,
        step=1,
        order=1,
        t0=t0_map,
        optimizer=slsqp_optimizer,
        chip="qiskit_aer",
        disp=True,
    )
    print(history[0])
    best_phase_idx, _, t0_map, _ = inner_optimize(
        8,
        0.5,
        0.5,
        step=1,
        order=1,
        t0=t0_map,
        optimizer=spsa_optimizer,
        chip="Baihua",
        chip_options={
            "target_qubits": [138, 125, 126, 127, 128, 129, 142, 141],
            "name": "inner_optimize",
        },
        disp=True,
    )
    print(history[0])
    assert best_phase_idx in (1, 0, -1)


def test_outer_optimize_output():
    best_step, best_order, best_phase_idx, best_result, t0_map, history_map = (
        outer_optimize(
            8,
            0.1,
            0.9,
            max_steps=[2],
            orders=[1],
            optimizer=SLSQP(maxiter=500, ftol=5e-2, disp=False),
            disp=True,
        )
    )
    print(t0_map)
    assert best_phase_idx in (1, 0, -1)
    # print(best_step, best_order, best_phase_idx, best_result.fun)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_inner"):
            fn()
            print(f"PASS {name}")
