import sys
import os
import numpy as np


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))  # 根目录

from get_cost_val import get_cost_val
from get_hw_evolution_qc import get_evolution_qc, get_evolution_path
from get_hw_initial_state import get_initial_state
from get_op import get_ssh_constrained_H


τ = 0.5


def get_branch_start(phase_idx, p0):
    """phase_idx ∈ {1, 0, -1}, v0 ∈ [0, 1] → 起点 (s0, δ0)."""
    if phase_idx == 1:
        return 0, p0
    elif phase_idx == 0:
        return p0, 0
    elif phase_idx == -1:
        return 1, p0
    else:
        raise ValueError("phase_idx must be 1, 0 or -1")


def _sigmoid(t):
    return 1.0 / (1.0 + np.exp(-np.array(t)))


def robust_objective(
    t,
    end,
    pidx=1,
    step=1,
    order=1,
    chip="qiskit_aer",
    chip_options=None,
    history=None,
    robust_options=None,
):
    if robust_options is None:
        robust_options = {
            "ϵ": 0.05,
            "n_samples": 10,
        }
    vals = []
    n_samples = robust_options.get("n_samples", 10)
    ϵ = robust_options.get("ϵ", 0.05)
    for _ in range(n_samples):
        delta = np.random.normal(size=len(t))
        delta /= np.linalg.norm(delta)
        robust_t = t + ϵ * delta
        evs = objective(
            robust_t,
            end,
            pidx=pidx,
            step=step,
            order=order,
            chip=chip,
            chip_options=chip_options,
            history=history,
        )
        vals.append(evs)
    mean_val = np.mean(vals)

    return float(mean_val)


def objective(
    t,
    end,
    pidx=1,
    step=1,
    order=1,
    chip="qiskit_aer",
    chip_options=None,
    history=None,
    robust_options=None,
):
    assert len(t) == 1 + 2 * step, f"t 长度应为 1+2*step={1 + 2 * step}, 实际 {len(t)}"
    # R^n → [0, 1]
    u = _sigmoid(t)
    up0 = u[0]
    ux = u[1 : 1 + step]
    uΔ = u[1 + step : 1 + 2 * step]

    # [0, 1]映射到实际取值范围
    Δt = τ * uΔ
    p0 = up0
    start = get_branch_start(pidx, p0)
    path = get_evolution_path(start, end, ux)

    # get qc
    initial_state = get_initial_state(pidx)
    qc = get_evolution_qc(
        initial_state,
        path,
        Δt,
        order=order,
    )

    # get cost vals
    Hc = get_ssh_constrained_H(end[0], end[1], ϵ=1)
    evs = get_cost_val(qc, Hc, chip=chip, chip_options=chip_options)

    # 记录优化器实际访问的点
    if history is not None and (history == [] or history[-1]["fun"] > float(evs)):
        history.append(
            {
                "fun": evs,
                "t": np.array(t, copy=True),
            }
        )

    return float(evs)
