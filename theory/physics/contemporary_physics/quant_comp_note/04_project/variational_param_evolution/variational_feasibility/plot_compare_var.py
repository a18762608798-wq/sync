from pathlib import Path


import numpy as np
import matplotlib.pyplot as plt


def plot_compare_spec(
    ideal_spec_path, compare_spec_path, direct_path=None, aer_path=None, quark_path=None
):
    data = np.load(ideal_spec_path)
    slist = data["slist"]
    spectrum = data["spectrum"]

    E0 = spectrum[:, 0]
    E1 = spectrum[:, 1]

    plt.plot(slist, E0, label="Ideal E0")
    plt.plot(slist, E1, label="Ideal E1")

    if direct_path is not None:
        direct = np.load(direct_path)
        plt.scatter(
            direct["slist"], direct["vals"], label="Direct vals", color="blue", zorder=5
        )

    if aer_path is not None:
        qc = np.load(aer_path)
        plt.scatter(
            qc["slist"], qc["vals"], label="Aer vals", color="purple", marker="^",
            zorder=5,
        )

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


def plot_compare_params(direct_path, aer_path, output_dir, quark_path=None):
    direct = np.load(direct_path)
    qc = np.load(aer_path)

    s_direct = direct["slist"]
    s_qc = qc["slist"]

    plots = [
        ("steps", "s", "step", "Best Step"),
        ("orders", "s", "order", "Best Order"),
        ("pidxs", "s", "phase_idx", "Best Phase Index"),
    ]

    for name, xlab, ylab, title in plots:
        plt.figure()
        plt.scatter(s_direct, direct[name], label=f"{name} (direct)")
        plt.scatter(s_qc, qc[name], label=f"{name} (aer)", marker="^")
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

    direct_path = HERE / "./data/aer_qc_spectrum_direct.npz"
    aer_path = HERE / "./data/aer_qc_spectrum.npz"
    # quark_path = HERE / "./data/quark_qc_spectrum.npz"
    quark_path = None
    plot_compare_spec(
        ideal_spec_path,
        compare_spec_path,
        direct_path=direct_path,
        aer_path=aer_path,
        quark_path=quark_path,
    )
    plot_compare_params(direct_path, aer_path, HERE / "./pics", quark_path=quark_path)
