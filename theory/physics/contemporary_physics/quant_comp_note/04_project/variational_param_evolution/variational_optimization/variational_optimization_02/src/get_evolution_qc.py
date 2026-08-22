import numpy as np

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter

from get_initial_state import get_initial_state
from get_op import get_ssh_H


def _sigmoid(t):
    return 1.0 / (1.0 + np.exp(-np.array(t)))


def get_branch_start(phase_idx, p0):
    """phase_idx ∈ {1, 0, -1}, p0 ∈ [0, 1] → 起点 (s0, δ0)."""
    if phase_idx == 1:
        return 0.05, p0  # 边界保护, 防止量子计算机优化0门.
    elif phase_idx == 0:
        return p0, 0.05  # 边界保护, 防止量子计算机优化0门.
    elif phase_idx == -1:
        return 0.95, p0  # 边界保护, 防止量子计算机优化0门.
    else:
        raise ValueError("phase_idx must be 1, 0 or -1")


def get_evolution_path(start, end, x):
    a = end[0] - start[0]
    b = end[1] - start[1]
    p = []
    for x_val in x:
        s = start[0] + a * x_val
        δ = start[1] + b * x_val
        p.append((s, δ))
    return p


def get_evolution_qc(
    initial_state,
    path,
    Δts,
    order=1,
):
    qc = initial_state
    qubit_num = qc.num_qubits
    path_length = len(path)
    for path_idx in range(path_length):
        s, δ = path[path_idx]
        Δt = Δts[path_idx]
        H = get_ssh_H(s, δ)

        synth = SuzukiTrotter(order=order, reps=1)
        evo = PauliEvolutionGate(
            H,
            time=Δt,
            synthesis=synth,
        )

        qc.append(evo, range(qubit_num))

    return qc


def get_qc_from_t(t, end, pidx=1, step=1, order=1, τ=20):
    """由无约束参数向量 t 生成演化电路 qc.

    t 长度必须为 1 + 2*step, 依次映射为:
      t[0]            → 起点参数 p0 (经 sigmoid 到 [0,1])
      t[1:1+step]     → 路径插值参数 ux
      t[1+step:1+2*step] → 时间 uΔ, 经 τ 放大
    返回演化电路 qc.
    """
    assert len(t) == 1 + 2 * step, f"t 长度应为 1+2*step={1 + 2 * step}, 实际 {len(t)}"

    # R^n → [0, 1]
    u = _sigmoid(t)
    up0 = u[0]
    ux = u[1 : 1 + step]
    uΔ = u[1 + step : 1 + 2 * step]

    # [0, 1] 映射到实际取值范围
    Δt = τ * (0.05 + 0.95 * uΔ)  # 单边界保护
    p0 = 1 * (0.05 + 0.9 * up0)  # 双边界保护
    start = get_branch_start(pidx, p0)
    path = get_evolution_path(start, end, ux)

    # get qc
    initial_state = get_initial_state(pidx)
    qc = get_evolution_qc(initial_state, path, Δt, order=order)

    return qc
