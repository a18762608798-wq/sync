from pathlib import Path


import numpy as np
import matplotlib.pyplot as plt


def plot_compare_spec(
    ideal_spec_path, compare_spec_path, aer_path=None, quark_path=None
):
    data = np.load(ideal_spec_path)
    slist = data["slist"]
    spectrum = data["spectrum"]

    E0 = spectrum[:, 0]
    E1 = spectrum[:, 1]

    plt.plot(slist, E0, label="Ideal E0")
    plt.plot(slist, E1, label="Ideal E1")

    if aer_path is not None:
        qc = np.load(aer_path)
        plt.scatter(qc["slist"], qc["vals"], label="Aer vals", color="purple", zorder=5)

    if quark_path is not None:
        quark = np.load(quark_path)
        plt.scatter(
            quark["slist"], quark["vals"], label="Quark vals", color="orange", zorder=5
        )

    plt.xlabel("s")
    plt.ylabel("E")
    plt.legend()
    plt.title("Spectrum Comparison(δ=0.3)")
    plt.tight_layout()
    plt.savefig(compare_spec_path)


def plot_compare_params(aer_path, output_dir, quark_path=None):
    qc = np.load(aer_path)

    s_qc = qc["slist"]

    plots = [
        ("steps", qc["steps"], "s", "step", "Best Step"),
        ("orders", qc["orders"], "s", "order", "Best Order"),
        ("pidxs", qc["pidxs"], "s", "phase_idx", "Best Phase Index"),
    ]

    for name, data, xlab, ylab, title in plots:
        plt.figure()
        plt.scatter(s_qc, data, label=f"{name} (aer)")
        if quark_path is not None:
            quark = np.load(quark_path)
            plt.scatter(quark["slist"], quark[name], label=f"{name} (quark)")
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"compare_{name}.jpg")


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    ideal_spec_path = HERE / "./data/ideal_spectrum.npz"
    compare_spec_path = HERE / "./pics/compare_spectrum.jpg"

    aer_path = HERE / "./data/aer_qc_spectrum.npz"
    quark_path = HERE / "./data/quark_qc_spectrum.npz"
    plot_compare_spec(
        ideal_spec_path, compare_spec_path, aer_path=aer_path, quark_path=quark_path
    )
    plot_compare_params(aer_path, HERE / "./pics", quark_path=quark_path)
