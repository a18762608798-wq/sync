from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def plot_ideal_spec(ideal_spec_path, ideal_spec_fig_path):
    plt.figure()  # 新开一个空白画布，重置所有状态
    # Get ideal spec
    data = np.load(ideal_spec_path)
    slist = data["slist"]
    spectrum = data["spectrum"]

    E0 = spectrum[:, 0]
    E1 = spectrum[:, 1]

    plt.plot(slist, E0, label="Ideal E0")
    plt.plot(slist, E1, label="Ideal E1")

    plt.xlabel("s")
    plt.ylabel("E")
    plt.legend()
    plt.title(f"Ideal Spectrum(E0(1) = {E0[-1]:.2f})")
    plt.tight_layout()
    plt.savefig(ideal_spec_fig_path)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    ideal_spec_path = HERE / "./data/ideal_spectrum.npz"
    ideal_spec_fig_path = HERE / "./pics/ideal_spec.jpg"

    plot_ideal_spec(ideal_spec_path, ideal_spec_fig_path)
