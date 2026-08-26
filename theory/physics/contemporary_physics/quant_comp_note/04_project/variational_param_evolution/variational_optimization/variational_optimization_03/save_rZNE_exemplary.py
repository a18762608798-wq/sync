import json
from pathlib import Path


import numpy as np
from scipy.optimize import curve_fit


IDEAL_BELL_VAL = -12.0
IDEAL_E0_VAL = -13.49973


def zne_fun(m, a, b, c):
    return a * np.exp(-b * m) + c


def get_rZNE_vals(record, ideal_val=None, r=None):
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


def save_rZNE_vals(zne_path, bell_path, zne_fitting_path, bell_fitting_path):
    with open(zne_path, encoding="utf-8") as f:
        zne = json.load(f)
    with open(bell_path, encoding="utf-8") as f:
        bell = json.load(f)

    bell_record = get_rZNE_vals(bell, ideal_val=IDEAL_BELL_VAL)
    r = bell_record["r"]
    zne_record = get_rZNE_vals(zne, ideal_val=IDEAL_E0_VAL, r=r)

    # save to json
    for record, path in [
        (zne_record, zne_fitting_path),
        (bell_record, bell_fitting_path),
    ]:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {path}")


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    save_rZNE_vals(
        HERE / "data" / "ZNE_exemplary.json",
        HERE / "data" / "bell_ZNE_exemplary.json",
        HERE / "data" / "rZNE_exemplary.json",
        HERE / "data" / "bell_rZNE_exemplary.json",
    )
