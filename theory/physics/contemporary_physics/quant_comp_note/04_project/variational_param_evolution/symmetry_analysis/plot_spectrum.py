from pathlib import Path


import matplotlib.pyplot as plt
import numpy as np


def plot_spectrum(data_path, pic_path_s, pic_path_d):
    data = np.load(data_path)
    param_list = data["param_list"]
    s_spectrum = data["s_spectrum"]
    δ_spectrum = data["delta_spectrum"]

    grid_length, eigvals, param_num = s_spectrum.shape
    grid = np.linspace(0, 1, grid_length)

    # Figure 1: s scan, spectrum vs δ for each fixed s
    cols = min(param_num, 3)
    rows = (param_num + cols - 1) // cols
    fig1, axes1 = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)
    for i in range(param_num):
        ax = axes1[i // cols, i % cols]
        for j in range(eigvals):
            ax.plot(grid, s_spectrum[:, j, i], color=f"C{j}", linewidth=1)
        ax.set_title(f"s={param_list[i]:.2f}")
        ax.set_xlabel(r"$\delta$")
        ax.set_ylabel("Energy")
    for i in range(param_num, rows * cols):
        axes1[i // cols, i % cols].set_visible(False)
    fig1.tight_layout()
    fig1.savefig(pic_path_s)

    # Figure 2: δ scan, spectrum vs s for each fixed δ
    fig2, axes2 = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), squeeze=False)
    for i in range(param_num):
        ax = axes2[i // cols, i % cols]
        for j in range(eigvals):
            ax.plot(grid, δ_spectrum[:, j, i], color=f"C{j}", linewidth=1)
        ax.set_title(r"$\delta$=" + f"{param_list[i]:.2f}")
        ax.set_xlabel(r"$s$")
        ax.set_ylabel("Energy")
    for i in range(param_num, rows * cols):
        axes2[i // cols, i % cols].set_visible(False)
    fig2.tight_layout()
    fig2.savefig(pic_path_d)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "./data/spectrum.npz"
    pic_path_s = HERE / "./pics/spectrum_s_scan.jpg"
    pic_path_d = HERE / "./pics/spectrum_delta_scan.jpg"
    plot_spectrum(data_path, pic_path_s, pic_path_d)
