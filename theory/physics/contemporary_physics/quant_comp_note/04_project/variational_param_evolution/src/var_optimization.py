import numpy as np
from scipy.optimize import minimize, Bounds


from get_cost_vals import get_cost_vals
from get_evolution_qc import get_evolution_qc
from get_initial_state import get_initial_state
from create_op import get_ssh_constrained_H


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


def objective(
    x, phase_idx, qubit_num, s1, δ1, step, order, chip="qiskit_aer", chip_options=None
):
    # 优化变量: v0, us, uδ, Δts, Δtds
    v0, us, uδ = x[0:3]
    Δts = x[3 : 3 + step]
    Δtds = x[3 + step : 3 + 2 * step]

    # 边界约束.
    BAD_VAL = 1e6
    if (
        not np.all(np.isfinite(x))
        or not 0 <= v0 <= 1
        or not 0 <= us <= 1
        or not 0 <= uδ <= 1
        or np.any(Δts < 1e-2)
        or np.any(Δts > 10)
        or np.any(Δtds < 0)
        or np.any(Δtds > 1)
    ):
        return BAD_VAL

    # 线性换元得到物理控制点, 保证 sp∈[min(s0,s1),max(s0,s1)].
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
    evs = get_cost_vals(qc, Hc, chip=chip, options=chip_options)

    return float(evs)


def _default_x0(step):
    """默认初值: v0, us, uδ=0.5, Δts=5, Δtds=0.5."""
    return [0.5, 0.5, 0.5] + [5] * step + [0.5] * step


def optimize_branch(
    phase_idx,
    qubit_num,
    s1,
    δ1,
    step,
    order,
    x0=None,
    method="COBYLA",
    options=None,
    chip="qiskit_aer",
    chip_options=None,
):
    if options is None:
        options = {
            "maxiter": 1000,
            "tol": 1e-6,
            "disp": False,
        }
    # bound
    lb = [0] * 3 + [1e-2] * step + [0] * step
    ub = [1, 1, 1] + [10] * step + [1] * step
    bounds = Bounds(
        lb=lb,
        ub=ub,
    )

    # sp, δp 已用 us, uδ∈[0,1] 线性换元, 自动落在两端点之间, 无需动态约束.
    constraints = []
    # COBYLA 忽略 bounds，需把每个变量的上下界也转成不等式约束，否则不生效。
    for i, (lo, hi) in enumerate(zip(lb, ub)):
        constraints.append(
            {
                "type": "ineq",
                "fun": lambda x, i=i, lo=lo: x[i] - lo,
            }
        )
        constraints.append(
            {
                "type": "ineq",
                "fun": lambda x, i=i, hi=hi: hi - x[i],
            }
        )

    # optimize
    if x0 is None:
        x0 = _default_x0(step)
    result = minimize(
        objective,
        x0=x0,
        args=(
            phase_idx,
            qubit_num,
            s1,
            δ1,
            step,
            order,
            chip,
            chip_options,
        ),
        method=method,
        bounds=bounds,
        constraints=constraints,
        options=options,
    )
    if result.success:
        pass
    elif getattr(result, "status", None) == 9:
        if options.get("disp", True):
            print(f"phase_idx={phase_idx}: 达到最大迭代次数, 使用当前解")
    else:
        if options.get("disp", True):
            print(f"phase_idx={phase_idx}: 优化失败")
            print(result.message)

    return result


def inner_optimize(
    qubit_num,
    s1,
    δ1,
    step,
    order,
    x0=None,
    method="COBYLA",
    options=None,
    disp=False,
    chip="qiskit_aer",
    chip_options=None,
):
    """x0: dict {phase_idx: 初值向量} 或 None. 返回 (best_phase_idx, best_result, x0_map)."""
    best_phase_idx, best_result = None, None
    x0_map = {}
    for phase_idx in [1, 0, -1]:
        branch_x0 = None if x0 is None else x0.get(phase_idx)
        result = optimize_branch(
            phase_idx,
            qubit_num,
            s1,
            δ1,
            step,
            order,
            x0=branch_x0,
            method=method,
            options=options,
            chip=chip,
            chip_options=chip_options,
        )
        if not result.success and getattr(result, "status", None) != 9:
            continue
        x0_map[phase_idx] = result.x
        if best_result is None or result.fun < best_result.fun:
            best_phase_idx, best_result = phase_idx, result

    if best_result is None:
        raise RuntimeError("所有分支优化均失败")

    if disp:
        print(f"\n最优分支 phase_idx={best_phase_idx}")
        print(f"x = {best_result.x}")
        print(f"目标值 = {best_result.fun}")

    return best_phase_idx, best_result, x0_map


def outer_optimize(
    qubit_num,
    s1,
    δ1,
    max_steps,
    orders,
    x0=None,
    method="COBYLA",
    options=None,
    disp=False,
    chip="qiskit_aer",
    chip_options=None,
):
    """x0: dict {(order, step, phase_idx): 初值向量} 或 None.
    返回 (best_step, best_order, best_phase_idx, best_result, x0_map)."""
    best_step, best_order, best_phase_idx, best_result = None, None, None, None
    x0_map = {}
    for order, max_s in zip(orders, max_steps):
        for step in range(1, max_s + 1):
            # 取出本 (order, step) 的 phase_idx→初值 子字典
            inner_x0 = None
            if x0 is not None:
                inner_x0 = {
                    pid: x0[(order, step, pid)]
                    for pid in [1, 0, -1]
                    if (order, step, pid) in x0
                }
            phase_idx, result, inner_x0_map = inner_optimize(
                qubit_num,
                s1,
                δ1,
                step,
                order,
                x0=inner_x0,
                method=method,
                options=options,
                disp=False,
                chip=chip,
                chip_options=chip_options,
            )
            for pid, xi in inner_x0_map.items():
                x0_map[(order, step, pid)] = xi
            if best_result is None or result.fun < best_result.fun:
                best_step, best_order, best_phase_idx, best_result = (
                    step,
                    order,
                    phase_idx,
                    result,
                )

    if best_result is None:
        raise RuntimeError("所有 (step, order) 组合优化均失败")

    if disp:
        print(
            f"\n最优: step={best_step}, order={best_order}, phase_idx={best_phase_idx}"
        )
        print(f"x = {best_result.x}")
        print(f"目标值 = {best_result.fun}")

    return best_step, best_order, best_phase_idx, best_result, x0_map
