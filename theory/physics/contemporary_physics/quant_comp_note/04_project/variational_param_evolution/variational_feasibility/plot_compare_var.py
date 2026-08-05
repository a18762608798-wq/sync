from pathlib import Path


import numpy as np
import matplotlib.pyplot as plt


def plot_compare_var(input_path, output_path, qc_path=None):
    data = np.load(input_path)
    slist = data["slist"]
    spectrum = data["spectrum"]

    E0 = spectrum[:, 0]
    E1 = spectrum[:, 1]

    plt.plot(slist, E0, label="Ideal E0")
    plt.plot(slist, E1, label="Ideal E1")

    if qc_path is not None:
        qc = np.load(qc_path)
        plt.scatter(qc["slist"], qc["vals"], label="QC vals", color="purple", zorder=5)

    plt.xlabel("s")
    plt.ylabel("E")
    plt.legend()
    plt.title("Spectrum Comparison(δ=0.3)")
    plt.tight_layout()
    plt.savefig(output_path)


def plot_qc_spectrum(qc_path, output_dir):
    qc = np.load(qc_path)

    s_qc = qc["slist"]

    plots = [
        ("steps", qc["steps"], "s", "step", "Best Step"),
        ("orders", qc["orders"], "s", "order", "Best Order"),
        ("pidxs", qc["pidxs"], "s", "phase_idx", "Best Phase Index"),
    ]

    for name, data, xlab, ylab, title in plots:
        plt.figure()
        plt.scatter(s_qc, data, label=name)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"qc_{name}.jpg")


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    input_path = HERE / "./data/ideal_spectrum.npz"
    output_path = HERE / "./pics/compare_spectrum.jpg"

    qc_path = HERE / "./data/qc_spectrum.npz"
    plot_compare_var(input_path, output_path, qc_path=qc_path)
    plot_qc_spectrum(qc_path, HERE / "./pics")
