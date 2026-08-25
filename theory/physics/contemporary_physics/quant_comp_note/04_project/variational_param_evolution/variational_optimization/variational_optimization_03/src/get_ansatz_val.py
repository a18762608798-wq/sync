from qiskit_algorithms.optimizers import DIRECT_L, SLSQP

from get_initial_state import get_initial_state
from optimize_branch import optimize_branch


def get_ansatz_val(s=1):
    direct_optimizer = DIRECT_L(
        max_evals=500,
    )
    slsqp_optimizer = SLSQP(
        maxiter=1000,
        ftol=1e-12,
        disp=False,
    )

    initial_state = get_initial_state()
    direct_res = optimize_branch(initial_state, s=s, optimizer=direct_optimizer)
    slsqp_res = optimize_branch(
        initial_state, t0=direct_res["t"], s=s, optimizer=slsqp_optimizer
    )
    return slsqp_res
