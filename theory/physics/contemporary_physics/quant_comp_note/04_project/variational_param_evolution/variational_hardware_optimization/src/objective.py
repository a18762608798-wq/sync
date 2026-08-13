import numpy as np


from get_cost_val import get_cost_val
from get_evolution_qc import get_qc_from_t
from get_op import get_ssh_constrained_H


τ = 20


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
    # t → qc
    qc = get_qc_from_t(t, end, pidx=pidx, step=step, order=order, τ=τ)

    # get cost vals
    Hc = get_ssh_constrained_H(end[0], end[1], ϵ=1)
    evs = get_cost_val(qc, Hc, chip=chip, chip_options=chip_options)

    # 记录优化器实际访问的点
    if history is not None and (history == [] or history[-1]["fun"] > float(evs)):
        history.append(
            {
                "fun": float(evs),
                "t": np.array(t, copy=True).tolist(),
            }
        )

    return float(evs)
