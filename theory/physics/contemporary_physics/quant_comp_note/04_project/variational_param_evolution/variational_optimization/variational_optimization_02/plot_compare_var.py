from pathlib import Path
import json


import numpy as np
import matplotlib.pyplot as plt


def plot_compare_spec(
    ideal_spec_path, direct_path, aer_path, compare_spec_path, quark_path=None
):
    plt.figure()  # 新开一个空白画布，重置所有状态
    # Get ideal spec
    data = np.load(ideal_spec_path)
    slist = data["slist"]
    spectrum = data["spectrum"]

    E0 = spectrum[:, 0]
    E1 = spectrum[:, 1]

    plt.plot(slist, E0, label="Ideal E0")
    plt.plot(slist, E1, label="Ideal E1")

    # Get direct
    with open(direct_path) as f:
        direct = json.load(f)
    vals = [direct[k]["res"]["fun"] for k in direct]  # the key will be str
    best_idx = np.argmin(vals)
    print(f"The best direct discreate_vars: f{direct[str(best_idx)]['discrete_vars']}")
    best_val = vals[best_idx]
    plt.scatter(
        [0.25],
        [best_val],
        label="Direct vals",
        color="blue",
        zorder=10,
        marker="x",
    )

    # Get aer
    with open(aer_path) as f:
        aer = json.load(f)
    vals = [aer[k]["res"]["fun"] for k in aer]  # the key will be str
    best_idx = np.argmin(vals)
    print(f"The best aer discreate_vars: f{aer[str(best_idx)]['discrete_vars']}")
    best_val = vals[best_idx]
    plt.scatter([0.25], [best_val], label="Aer vals", color="red", zorder=5, marker="o")

    # Get quark
    if quark_path is not None:
        with open(quark_path) as f:
            quark = json.load(f)
        vals = [quark[k]["res"]["fun"] for k in quark]  # the key will be str
        best_idx = np.argmin(vals)
        print(
            f"The best quark discreate_vars: f{quark[str(best_idx)]['discrete_vars']}"
        )
        best_val = vals[best_idx]
        plt.scatter(
            [0.25], [best_val], label="Quark vals", color="yellow", zorder=5, marker="*"
        )

    plt.xlabel("s")
    plt.ylabel("E")
    plt.legend()
    plt.title("Spectrum Comparison(δ=0.3)")
    plt.tight_layout()
    plt.savefig(compare_spec_path)


def plot_update_energy(direct_path, aer_path, update_energy_path, quark_path=None):
    plt.figure()  # 新开一个空白画布，重置所有状态
    # ----------
    # 遵循quark的最优分支
    # ----------
    if quark_path is not None:
        with open(quark_path) as f:
            quark = json.load(f)
        vals = [quark[k]["res"]["fun"] for k in quark]  # the key will be str
        best_idx = np.argmin(vals)
    # Get direct
    with open(direct_path) as f:
        direct = json.load(f)
    vals = [direct[k]["res"]["fun"] for k in direct]  # the key will be str
    best_idx = np.argmin(vals) if quark_path is None else best_idx
    direct_history = direct[str(best_idx)]["history"]
    # Get aer
    with open(aer_path) as f:
        aer = json.load(f)
    vals = [aer[k]["res"]["fun"] for k in aer]  # the key will be str
    best_idx = np.argmin(vals) if quark_path is None else best_idx
    aer_history = aer[str(best_idx)]["history"]
    history = direct_history + aer_history
    # Get quark
    if quark_path is not None:
        quark_history = quark[str(best_idx)]["history"]
        history = history + quark_history
    best_vals_history = [history[i]["fun"] for i in range(len(history))]
    plt.plot(range(len(history)), best_vals_history, label="Best val optimization")
    plt.xlabel("update times")
    plt.ylabel("H")
    plt.legend()
    plt.title(
        f"Update energy(s=0.25, δ=0.3), discrete_vars: {
            quark[str(best_idx)]['discrete_vars']
            if quark_path is not None
            else aer[str(best_idx)]['discrete_vars']
        }"
    )
    plt.tight_layout()
    plt.savefig(update_energy_path)


def plot_update_t(direct_path, aer_path, update_energy_path, quark_path=None):
    plt.figure()  # 新开一个空白画布，重置所有状态
    # ----------
    # 遵循quark的最优分支
    # ----------
    if quark_path is not None:
        with open(quark_path) as f:
            quark = json.load(f)
        vals = [quark[k]["res"]["fun"] for k in quark]  # the key will be str
        best_idx = np.argmin(vals)
    # Get direct
    with open(direct_path) as f:
        direct = json.load(f)
    vals = [direct[k]["res"]["fun"] for k in direct]  # the key will be str
    best_idx = np.argmin(vals) if quark_path is None else best_idx
    direct_history = direct[str(best_idx)]["history"]
    # Get aer
    with open(aer_path) as f:
        aer = json.load(f)
    vals = [aer[k]["res"]["fun"] for k in aer]  # the key will be str
    best_idx = np.argmin(vals) if quark_path is None else best_idx
    aer_history = aer[str(best_idx)]["history"]
    history = direct_history + aer_history
    # Get quark
    if quark_path is not None:
        quark_history = quark[str(best_idx)]["history"]
        history = history + quark_history
    best_t_history = [history[i]["t"] for i in range(len(history))]
    step = (
        quark[str(best_idx)]["discrete_vars"][1]
        if quark_path is not None
        else aer[str(best_idx)]["discrete_vars"][1]
    )
    plt.plot(
        range(len(history)),
        [best_t_history[i][0] for i in range(len(history))],
        label="p0",
    )
    for j in range(step):
        plt.plot(
            range(len(history)),
            [best_t_history[i][j + 1] for i in range(len(history))],
            label=f"tx{j}",
        )
        plt.plot(
            range(len(history)),
            [best_t_history[i][j + step + 1] for i in range(len(history))],
            label=f"tΔt{j}",
        )
    plt.xlabel("update times")
    plt.ylabel("t")
    plt.legend()
    plt.title(
        f"Update t(s=0.25, δ=0.3), discrete_vars: {aer[str(best_idx)]['discrete_vars']}"
    )
    plt.tight_layout()
    plt.savefig(update_energy_path)


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    ideal_spec_path = HERE / "./data/ideal_spectrum.npz"
    compare_spec_path = HERE / "./pics/compare_spec.jpg"

    direct_path = HERE / "./data/direct_dic.json"
    aer_path = HERE / "./data/aer_dic.json"
    quark_path = HERE / "./data/quark_dic.json"

    plot_compare_spec(
        ideal_spec_path, direct_path, aer_path, compare_spec_path, quark_path=quark_path
    )
    update_energy_path = HERE / "./pics/update_energy_path.jpg"
    plot_update_energy(
        direct_path,
        aer_path,
        update_energy_path,
        quark_path=quark_path,
    )
    update_t_path = HERE / "./pics/update_t_path.jpg"
    plot_update_t(
        direct_path,
        aer_path,
        update_t_path,
        quark_path=quark_path,
    )
