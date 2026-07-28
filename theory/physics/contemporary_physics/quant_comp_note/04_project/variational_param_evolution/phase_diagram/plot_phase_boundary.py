from pathlib import Path


import matplotlib.pyplot as plt
import numpy as np


def plot_phase_boundary(data_path, pic_path):
    data = np.load(data_path)
    QUBIT_NUMS = data["QUBIT_NUMS"]
    s_points = data["s_points"]
    delta_boundaries = data["delta_boundaries"]
    s_boundaries = data["s_boundaries"]

    n_s = s_boundaries.shape[1]

    fig = plt.figure(figsize=(14, 5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # Plot 1: s boundary vs qubit_num at delta=1
    ax1.plot(QUBIT_NUMS, delta_boundaries, "o-", color="tab:blue", markersize=6)
    ax1.set_xlabel("Qubit Number")
    ax1.set_ylabel("s")
    ax1.set_title(r"$s$ vs Qubit Number at $\delta=1$")

    # Plot 2: delta vs qubit_num for each s
    s_means = s_points.mean(axis=0)
    for i in range(n_s):
        ax2.plot(
            QUBIT_NUMS,
            s_boundaries[:, i],
            "o-",
            markersize=6,
            label=f"s≈{s_means[i]:.2f}",
        )
    ax2.set_xlabel("Qubit Number")
    ax2.set_ylabel(r"$\delta$")
    ax2.set_title(r"$\delta$ vs Qubit Number for different $s$")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(pic_path)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "./data/boundary.npz"
    pic_path = HERE / "./pics/phase_boundary.jpg"
    plot_phase_boundary(data_path, pic_path)
