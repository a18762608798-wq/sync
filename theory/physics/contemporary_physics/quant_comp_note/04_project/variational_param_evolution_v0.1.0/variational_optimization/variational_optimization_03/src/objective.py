from get_cost_val import get_cost_val
from get_evolution_qc import get_evolution_qc
from get_op import get_ssh_constrained_H


def objective(
    theta,
    initial_state,
    *,
    s=1,
    ϵ=0,
):
    # get params
    θodd = theta[0]
    θeven = theta[1]
    qc = get_evolution_qc(initial_state, θodd, θeven)
    # get cost vals
    Hc = get_ssh_constrained_H(s, ϵ=ϵ)
    evs = get_cost_val(qc, Hc)

    return float(evs)
