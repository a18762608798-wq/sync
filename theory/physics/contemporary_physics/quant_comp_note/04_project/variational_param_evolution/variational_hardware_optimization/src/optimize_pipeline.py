from multiprocessing import Pool
from tqdm import tqdm
import itertools

from optimize_branch import optimize_branch


def _wrapper(args):
    (
        end,
        pidx,
        step,
        order,
        t0,
        optimizer,
        chip,
        chip_options,
        robust,
        robust_options,
    ) = args

    return optimize_branch(
        end,
        pidx=pidx,
        step=step,
        order=order,
        t0=t0,
        optimizer=optimizer,
        chip=chip,
        chip_options=chip_options,
        history=[],
        robust=robust,
        robust_options=robust_options,
    )


def optimize_pipeline(
    end,
    discrete_vars=None,
    t0=None,
    optimizer=None,
    chip="qiskit_aer",
    chip_options=None,
    robust=False,
    robust_options=None,
    progress=True,
):
    if discrete_vars is None:
        discrete_vars = [
            [1, 1, 1],
            [1, 1, 2],
            [1, 2, 1],
            [0, 1, 1],
            [0, 1, 2],
            [0, 2, 1],
            [-1, 1, 1],
            [-1, 1, 2],
            [-1, 2, 1],
        ]
    if t0 is None:
        t0 = [None for _ in range(len(discrete_vars))]

    pidx_ls = [discrete_vars[i][0] for i in range(len(discrete_vars))]
    step_ls = [discrete_vars[i][1] for i in range(len(discrete_vars))]
    order_ls = [discrete_vars[i][2] for i in range(len(discrete_vars))]

    with Pool(processes=9) as pool:
        iterable = pool.imap(
            _wrapper,
            zip(
                itertools.repeat(end),
                pidx_ls,
                step_ls,
                order_ls,
                t0,
                itertools.repeat(optimizer),
                itertools.repeat(chip),
                itertools.repeat(chip_options),
                itertools.repeat(robust),
                itertools.repeat(robust_options),
            ),
        )
        if progress:
            iterable = tqdm(
                iterable,
                total=len(discrete_vars),
                desc="s 扫描",
            )
        iterables = list(iterable)
        result_dic = {
            i: {
                "discrete_vars": discrete_vars[i],
                "res": iterables[i][0],
                "history": iterables[i][1],
            }
            for i in range(len(iterables))
        }

    return result_dic
