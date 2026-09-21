import numpy as np


from get_cost_val import get_cost_val
from get_evolution_qc import get_qc_from_t
from get_op import get_ssh_constrained_H


τ = 20


def objective(
    t,
    end,
    pidx=1,
    step=1,
    order=1,
    chip="qiskit_aer",
    chip_options=None,
    history=None,
):
    # t → qc
    qc = get_qc_from_t(t, end, pidx=pidx, step=step, order=order, τ=τ)

    if chip_options is not None and chip_options.get("name"):
        chip_options = dict(chip_options)
        chip_options["name"] = (
            f"{chip_options['name']}_pidx={pidx}_step={step}_order={order}"
        )

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
