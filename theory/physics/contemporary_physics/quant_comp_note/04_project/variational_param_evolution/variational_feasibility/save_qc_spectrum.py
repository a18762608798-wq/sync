import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from var_optimization import outer_optimize


def _run_one(s):
    best_step, best_order, best_phase_idx, best_result = outer_optimize(
        8,
        s,
        0.3,
        max_steps=[5, 3],
        orders=[1, 2],
        method="SLSQP",
        options={"maxiter": 50, "ftol": 1e-4, "disp": False},
        disp=False,
    )
    return best_step, best_order, best_phase_idx, best_result.fun


def save_qc_spectrum(path, processes=8):
    slist = np.arange(0.1, 0.9 + 1e-6, 0.1)

    with Pool(processes=processes) as pool:
        results = list(
            tqdm(pool.imap(_run_one, slist), total=len(slist), desc="s 扫描")
        )

    steps = [o[0] for o in results]
    orders = [o[1] for o in results]
    pidxs = [o[2] for o in results]
    vals = [o[3] for o in results]

    np.savez(
        path,
        slist=slist,
        steps=steps,
        orders=orders,
        pidxs=pidxs,
        vals=vals,
    )


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    path = HERE / "./data/qc_spectrum.npz"
    save_qc_spectrum(path)
