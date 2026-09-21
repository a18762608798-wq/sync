import numpy as np
from qiskit_algorithms.optimizers import SLSQP, SPSA, DIRECT_L
from functools import partial


from get_cost_val import get_cost_val
from get_evolution_qc import get_evolution_qc
from get_initial_state import get_initial_state
from create_op import get_ssh_constrained_H


τ = 3


def get_branch_start(phase_idx, v0):
    """phase_idx ∈ {1, 0, -1}, v0 ∈ [0, 1] → 起点 (s0, δ0)."""
    if phase_idx == 1:
        return 0, v0
    elif phase_idx == 0:
        return v0, 0
    elif phase_idx == -1:
        return 1, v0
    else:
        raise ValueError("phase_idx must be 1, 0 or -1")


def _sigmoid(t):
    return 1.0 / (1.0 + np.exp(-t))


def objective(
    t,
    phase_idx,
    qubit_num,
    s1,
    δ1,
    step,
    order,
    chip="qiskit_aer",
    chip_options=None,
    history=None,
):
    x = _sigmoid(t)
    # 第一次换元: 映射到[0, 1]
    v0, us, uδ = x[0:3]
    u_Δts = x[3 : 3 + step]
    Δtds = x[3 + step : 3 + 2 * step]

    # 第二次换元: 映射到实际取值范围
    Δts = τ * u_Δts
    s0, δ0 = get_branch_start(phase_idx, v0)
    sp = s0 + us * (s1 - s0)
    δp = δ0 + uδ * (δ1 - δ0)

    # get qc
    initial_state = get_initial_state(qubit_num, phase_idx)
    qc, _ = get_evolution_qc(
        initial_state,
        (s0, δ0),
        (s1, δ1),
        (sp, δp),
        Δts,
        Δtds,
        order=order,
    )
    Hc = get_ssh_constrained_H(qubit_num, s1, δ1, ϵ=1)
    evs = get_cost_val(qc, Hc, chip=chip, chip_options=chip_options)

    # 记录优化器实际访问的点
    if history is not None and (history == [] or history[-1]["fun"] > float(evs)):
        history.append(
            {
                "t": np.array(t, copy=True),
                "fun": evs,
            }
        )

    return float(evs)


def _default_t0(step):
    """默认初值: t=0 → 各 u=sigmoid(0)=0.5."""
    t0 = np.zeros(3 + 2 * step)
    return t0


def optimize_branch(
    phase_idx,
    qubit_num,
    s1,
    δ1,
    step,
    order,
    t0=None,
    optimizer=None,
    chip="qiskit_aer",
    chip_options=None,
):
    # 默认参数设置
    if optimizer is None:
        optimizer = SLSQP(
            maxiter=5000,
            ftol=1e-5,
            disp=False,
        )
    if t0 is None:
        t0 = _default_t0(step)

    # 优化正文 (用关键字绑定固定参数, 让优化向量 t 保持在第一个位置)
    history = []
    partial_objective = partial(
        objective,
        phase_idx=phase_idx,
        qubit_num=qubit_num,
        s1=s1,
        δ1=δ1,
        step=step,
        order=order,
        chip=chip,
        chip_options=chip_options,
        history=history,
    )
    result = optimizer.minimize(
        partial_objective,
        x0=t0,
    )
    return result, history


def inner_optimize(
    qubit_num,
    s1,
    δ1,
    step,
    order,
    t0=None,
    optimizer=None,
    disp=False,
    chip="qiskit_aer",
    chip_options=None,
):
    """t0: dict {phase_idx: 初值向量} 或 None. 返回 (best_phase_idx, best_result, t0_map, history_map)."""
    best_phase_idx, best_result = None, None
    t0_map = {}
    history_map = {}
    for phase_idx in [1, 0, -1]:
        branch_t0 = None if t0 is None else t0.get(phase_idx)
        result, history = optimize_branch(
            phase_idx,
            qubit_num,
            s1,
            δ1,
            step,
            order,
            t0=branch_t0,
            optimizer=optimizer,
            chip=chip,
            chip_options=chip_options,
        )
        t0_map[phase_idx] = result.x
        history_map[phase_idx] = history
        if best_result is None or result.fun < best_result.fun:
            best_phase_idx, best_result = phase_idx, result

    if disp:
        print(f"\n最优分支 phase_idx={best_phase_idx}")
        print(f"t = {best_result.x}")
        print(f"目标值 = {best_result.fun}")

    return best_phase_idx, best_result, t0_map, history_map


def outer_optimize(
    qubit_num,
    s1,
    δ1,
    max_steps,
    orders,
    t0=None,
    optimizer=None,
    disp=False,
    chip="qiskit_aer",
    chip_options=None,
):
    """t0: dict {(order, step, phase_idx): 初值向量} 或 None.
    返回 (best_step, best_order, best_phase_idx, best_result, t0_map, history_map)."""
    best_step, best_order, best_phase_idx, best_result = None, None, None, None
    t0_map = {}
    history_map = {}
    for order, max_s in zip(orders, max_steps):
        for step in range(1, max_s + 1):
            # 取出本 (order, step) 的 phase_idx→初值 子字典
            inner_t0 = None
            if t0 is not None:
                inner_t0 = {
                    pid: t0[(order, step, pid)]
                    for pid in [1, 0, -1]
                    if (order, step, pid) in t0
                }
            phase_idx, result, inner_t0_map, inner_history_map = inner_optimize(
                qubit_num,
                s1,
                δ1,
                step,
                order,
                t0=inner_t0,
                optimizer=optimizer,
                disp=False,
                chip=chip,
                chip_options=chip_options,
            )
            for pid, ti in inner_t0_map.items():
                t0_map[(order, step, pid)] = ti
            for pid, hi in inner_history_map.items():
                history_map[(order, step, pid)] = hi
            if best_result is None or result.fun < best_result.fun:
                best_step, best_order, best_phase_idx, best_result = (
                    step,
                    order,
                    phase_idx,
                    result,
                )

    if best_result is None:
        raise RuntimeError("没有做任何优化.")

    if disp:
        print(
            f"\n最优: step={best_step}, order={best_order}, phase_idx={best_phase_idx}"
        )
        print(f"t = {best_result.x}")
        print(f"目标值 = {best_result.fun}")

    return best_step, best_order, best_phase_idx, best_result, t0_map, history_map
