import numpy as np
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP
from functools import partial


from objective import objective


BOUNDS = [
    (5.1e-4, 1.0),
    (5.1e-4, 1.0),
]


def optimize_branch(
    initial_state,
    s=1,
    ϵ=0,
    t0=None,
    optimizer=None,
):
    # 默认参数设置
    if optimizer is None:
        optimizer = SLSQP(
            maxiter=200,
            ftol=1e-6,
            disp=False,
        )
    if t0 is None:
        t0 = np.array([0.5, 0.5])

    # 优化正文
    partial_objective = partial(
        objective,
        initial_state=initial_state,
        s=s,
        ϵ=ϵ,
    )

    result = optimizer.minimize(
        partial_objective,
        x0=t0,
        bounds=BOUNDS,
    )

    record_re = {
        "fun": float(result.fun),
        "t": result.x.tolist(),
    }

    return record_re
