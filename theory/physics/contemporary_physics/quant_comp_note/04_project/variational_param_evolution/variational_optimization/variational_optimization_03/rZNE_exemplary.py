import json
from pathlib import Path


import numpy as np
from scipy.optimize import curve_fit


IDEAL_BELL_VAL = -12.0
IDEAL_E0_VAL = -13.49973


def zne_fun(m, a, b, c):
    return a * np.exp(-b * m) + c


def save_fitting_data(zne_path, bell_path, zne_fitting_path, bell_fitting_path):
    with open(zne_path, encoding="utf-8") as f:
        zne = json.load(f)
    with open(bell_path, encoding="utf-8") as f:
        bell = json.load(f)
    # fitting zne
    m, y = np.array(zne["m"]), zne["vals"]
    zne_popt, _ = curve_fit(zne_fun, m, y)
    # fitting bell
    m, y = np.array(bell["m"]), bell["vals"]
    bell_popt, _ = curve_fit(zne_fun, m, y)
    r = (IDEAL_BELL_VAL - bell_popt[2]) / bell_popt[0]

    # clean the data and calculate zne/rzne res
    zne_record = dict(zne)
    zne_record["popt"] = zne_popt.tolist()
    zne_record["r"] = float(r)
    zne_record["ideal_val"] = IDEAL_E0_VAL
    zne_record["zne_res"] = zne_fun(
        0,
        *zne_record["popt"],
    )
    zne_record["rzne_res"] = zne_fun(
        0,
        zne_record["popt"][0] * r,
        *zne_record["popt"][1:],
    )

    bell_record = dict(bell)
    bell_record["popt"] = bell_popt.tolist()
    bell_record["r"] = float(r)
    bell_record["ideal_val"] = IDEAL_BELL_VAL
    bell_record["zne_res"] = zne_fun(
        0,
        *bell_record["popt"],
    )
    bell_record["rzne_res"] = zne_fun(
        0,
        bell_record["popt"][0] * r,
        *bell_record["popt"][1:],
    )

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
    save_fitting_data(
        HERE / "data" / "ZNE_exemplary.json",
        HERE / "data" / "bell_ZNE_exemplary.json",
        HERE / "data" / "rZNE_exemplary.json",
        HERE / "data" / "bell_rZNE_exemplary.json",
    )
