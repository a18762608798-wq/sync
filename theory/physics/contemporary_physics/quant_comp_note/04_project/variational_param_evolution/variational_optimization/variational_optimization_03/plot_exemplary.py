from pathlib import Path
import json
import sys


import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

from get_rZNE_val import zne_fun


def plot_exemplary(zne_path, bell_path, fig_path):
    # get exprimental data
    plt.close("all")
    with open(zne_path, encoding="utf-8") as f:
        zne = json.load(f)
    with open(bell_path, encoding="utf-8") as f:
        bell = json.load(f)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, record, name in [
        (axes[0], zne, "ZNE"),
        (axes[1], bell, "Bell"),
    ]:
        # plot scatter of exprimental data
        ax.plot(
            record["m"],
            record["vals"],
            marker="o",
            linestyle="",
            label="primal_exprimental_data",
        )
        # plot fitting data
        fitting_m = np.linspace(0, max(record["m"]), 100)
        fitting_y = zne_fun(fitting_m, *record["popt"])
        ax.plot(fitting_m, fitting_y, label="fitting_data")
        # plot res
        ax.plot(
            [0],
            record["ideal_val"],
            marker="^",
            label=f"ideal_val: {record['ideal_val']:.3f}",
        )
        ax.plot(
            [0],
            record["zne_res"],
            marker="s",
            label=f"zne_res: {record['zne_res']:.3f}",
        )
        ax.plot(
            [0],
            record["rzne_res"],
            marker="+",
            label=f"rzne_res: {record['rzne_res']:.3f}",
        )
        ax.legend(loc="lower right")
        ax.set_xlabel("m")
        ax.set_ylabel("vals")
        ax.set_title(f"{name} exemplary (s = {record['s']}, {record['chip']})")

    fig.tight_layout()
    fig.savefig(fig_path)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    # chip = "Baihua"
    chip = "Baihua"
    plot_exemplary(
        HERE / "data" / chip / "rZNE_exemplary.json",
        HERE / "data" / chip / "bell_rZNE_exemplary.json",
        HERE / "pics" / chip / "exemplary.jpg",
    )
    # chip = "Shenglian"
    chip = "Shenglian"
    plot_exemplary(
        HERE / "data" / chip / "rZNE_exemplary.json",
        HERE / "data" / chip / "bell_rZNE_exemplary.json",
        HERE / "pics" / chip / "exemplary.jpg",
    )
