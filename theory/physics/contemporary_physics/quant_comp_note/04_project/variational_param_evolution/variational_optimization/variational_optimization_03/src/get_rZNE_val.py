import asyncio

import numpy as np
from scipy.optimize import curve_fit


def zne_fun(m, a, b, c):
    return a * np.exp(-b * m) + c


def _get_rZNE_vals(record, ideal_val=None, r=None):
    m, y = np.array(record["m"]), record["vals"]
    popt, _ = curve_fit(zne_fun, m, y, p0=[y[0] - y[-1], 0.3, y[-1]])
    if r is None:
        r = (ideal_val - popt[2]) / popt[0]

    record = dict(record)
    record["popt"] = popt.tolist()
    record["r"] = float(r)
    record["ideal_val"] = ideal_val
    record["zne_res"] = zne_fun(0, *popt)
    record["rzne_res"] = zne_fun(0, popt[0] * r, *popt[1:])
    return record


async def get_rZNE_vals(record, ideal_val=None, r=None):
    return await asyncio.to_thread(_get_rZNE_vals, record, ideal_val, r)
