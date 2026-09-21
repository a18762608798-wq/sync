from pathlib import Path


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plot_ssh_phase(data_path, pic_path):
    data = np.load(data_path)
    s = data["s"]
    δ = data["delta"]
    ZR = data["ZR"]

    # figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    n = len(s)
    step = max(1, n // 5)
    ax = sns.heatmap(ZR, cmap="coolwarm", ax=ax)
    ax.set_xticks(np.arange(0, n, step))
    ax.set_xticklabels(np.round(δ[::step], 2))
    ax.set_yticks(np.arange(0, n, step))
    ax.set_yticklabels(np.round(s[::step], 2))
    ax.set_xlabel(r"$\delta$")
    ax.set_ylabel(r"$s$")
    # output
    plt.savefig(pic_path)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    data_path = HERE / "./data/phase.npz"
    pic_path = HERE / "./pics/phase.jpg"
    plot_ssh_phase(data_path, pic_path)
