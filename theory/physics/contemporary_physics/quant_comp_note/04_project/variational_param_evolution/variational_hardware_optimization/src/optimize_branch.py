import numpy as np
from qiskit_algorithms.optimizers import SPSA, DIRECT_L
from functools import partial

from objective import objective, robust_objective


def _default_t0(step):
    """默认初值: t=0 → 各 u=sigmoid(0)=0.5."""
    t0 = np.zeros(1 + 2 * step)
    return t0


def optimize_branch(
    end,
    pidx=1,
    step=1,
    order=1,
    t0=None,
    optimizer=None,
    chip="qiskit_aer",
    chip_options=None,
    history=None,
    robust=False,
    robust_options=None,
):
    # 默认参数设置
    if optimizer is None:
        optimizer = SPSA(
            maxiter=500,
            blocking=True,
            trust_region=True,
            resamplings=1,
        )

    if t0 is None:
        t0 = _default_t0(step)

    if history is None:
        history = []

    if robust and (robust_options is None):
        robust_options = {
            "ϵ": 0.05,
            "n_samples": 10,
        }

    # 判断是不是 SPSA
    is_spsa = isinstance(optimizer, SPSA)

    # SPSA: history 只记录真正 accepted 的更新点
    if is_spsa:

        def callback(nfev, parameters, value, stepsize, accepted):
            if accepted:
                history.append(
                    {
                        "fun": float(value),
                        "t": np.array(parameters, copy=True).tolist(),
                    }
                )

        optimizer.callback = callback

    # 优化正文
    partial_objective = partial(
        robust_objective if robust else objective,
        end=end,
        pidx=pidx,
        step=step,
        order=order,
        chip=chip,
        chip_options=chip_options,
        # SPSA 不让 objective 记录 history
        # DIRECT_L 保持原来的 history 记录方式
        history=None if is_spsa else history,
        robust_options=robust_options,
    )

    result = optimizer.minimize(
        partial_objective,
        x0=t0,
    )

    record_re = {
        "fun": float(result.fun),
        "t": result.x.tolist(),
    }

    return record_re, history
