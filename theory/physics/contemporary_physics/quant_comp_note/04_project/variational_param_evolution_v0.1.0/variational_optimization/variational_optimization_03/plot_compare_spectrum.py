import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def plot_compare_spec(ideal_spec_path, rzne_spec_path, compare_spec_path):
    plt.figure()  # 新开一个空白画布，重置所有状态
    # Get ideal spec
    data = np.load(ideal_spec_path)
    slist = data["slist"]
    spectrum = data["spectrum"]

    E0 = spectrum[:, 0]
    E1 = spectrum[:, 1]

    plt.plot(slist, E0, label="Ideal E0")
    plt.plot(slist, E1, label="Ideal E1")
    # Get gs zne and rzne spec
    with open(rzne_spec_path, encoding="utf-8") as f:
        rzne = json.load(f)
    gs = rzne["gs"]
    s_ls = [record["s"] for record in gs]
    zne_ls = [record["zne_res"] for record in gs]
    rzne_ls = [record["rzne_res"] for record in gs]
    plt.plot(s_ls, zne_ls, "o", label="gs ZNE", linestyle="")
    plt.plot(s_ls, rzne_ls, "x", ms=9, label="gs rZNE", linestyle="")

    plt.xlabel("s")
    plt.ylabel("E")
    plt.legend()
    plt.title(f"Ideal Spectrum({gs[0]['chip']})")
    plt.tight_layout()
    plt.savefig(compare_spec_path)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    # Baihua
    chip = "Baihua"
    ideal_spec_path = HERE / "./data/ideal_spectrum.npz"
    rzne_spec_path = HERE / f"./data/{chip}/rZNE_spectrum.json"
    compare_spec_path = HERE / f"./pics/{chip}/compare_spec.jpg"
    plot_compare_spec(ideal_spec_path, rzne_spec_path, compare_spec_path)

    # Shenglian
    chip = "Shenglian"
    ideal_spec_path = HERE / "./data/ideal_spectrum.npz"
    rzne_spec_path = HERE / f"./data/{chip}/rZNE_spectrum.json"
    compare_spec_path = HERE / f"./pics/{chip}/compare_spec.jpg"
    plot_compare_spec(ideal_spec_path, rzne_spec_path, compare_spec_path)
