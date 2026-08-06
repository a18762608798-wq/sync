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


def objective(x, phase_idx, qubit_num, s1, δ1, step, order, chip="qiskit_aer"):
    # clean data
    v0, sp, δp = x[0:3]
    s0, δ0 = get_branch_start(phase_idx, v0)
    Δts = x[3 : 3 + step]
    Δtds = x[3 + step : 3 + 2 * step]
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
    evs = get_cost_vals(qc, Hc, chip=chip)

    return float(evs)


def optimize_branch(
    phase_idx,
    qubit_num,
    s1,
    δ1,
    step,
    order,
    method="SLSQP",
    options=None,
    chip="qiskit_aer",
):
    if options is None:
        options = {
            "maxiter": 1000,
            "ftol": 1e-6,
            "disp": False,
        }
    # bound
    lb = [0] * 3 + [1e-2] * step + [0] * step
    ub = [1, 1, 1] + [10] * step + [1] * step
    bounds = Bounds(
        lb=lb,
        ub=ub,
    )

    # 注意: s0 可能 > s1 (如 pidx=-1), 控制点应落在两端点之间
    constraints = [
        {
            "type": "ineq",
            "fun": lambda x: x[1] - min(get_branch_start(phase_idx, x[0])[0], s1),
        },
        {
            "type": "ineq",
            "fun": lambda x: max(get_branch_start(phase_idx, x[0])[0], s1) - x[1],
        },
        {
            "type": "ineq",
            "fun": lambda x: x[2] - min(get_branch_start(phase_idx, x[0])[1], δ1),
        },
        {
            "type": "ineq",
            "fun": lambda x: max(get_branch_start(phase_idx, x[0])[1], δ1) - x[2],
        },
    ]

    # optimize
    s0, δ0 = get_branch_start(phase_idx, 0.5)
    x0 = (
        [
            0.5,
            (s0 + s1) / 2,
            (δ0 + δ1) / 2,
        ]
        + [5] * step
        + [0.5] * step
    )
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
    qubit_num, s1, δ1, step, order, method="SLSQP", options=None, disp=False, chip="qiskit_aer"
):
    best_phase_idx, best_result = None, None
    for phase_idx in [1, 0, -1]:
        result = optimize_branch(
            phase_idx, qubit_num, s1, δ1, step, order, method=method, options=options, chip=chip
        )
        if not result.success and getattr(result, "status", None) != 9:
            continue
        if best_result is None or result.fun < best_result.fun:
            best_phase_idx, best_result = phase_idx, result

    if best_result is None:
        raise RuntimeError("所有分支优化均失败")

    if disp:
        print(f"\n最优分支 phase_idx={best_phase_idx}")
        print(f"x = {best_result.x}")
        print(f"目标值 = {best_result.fun}")

    return best_phase_idx, best_result


def outer_optimize(
    qubit_num, s1, δ1, max_steps, orders, method="SLSQP", options=None, disp=False, chip="qiskit_aer"
):
    best_step, best_order, best_phase_idx, best_result = None, None, None, None
    for order, max_s in zip(orders, max_steps):
        for step in range(1, max_s + 1):
            phase_idx, result = inner_optimize(
                qubit_num,
                s1,
                δ1,
                step,
                order,
                method=method,
                options=options,
                disp=False,
                chip=chip,
            )
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

    return best_step, best_order, best_phase_idx, best_result
