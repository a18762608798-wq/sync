"""PRA publication figures for Experiment 02 — saved data only."""

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt

from ssh_xxz.io.store import iter_points

plt.rcParams.update({"font.family": "serif", "font.size": 8,
                     "figure.figsize": (3.4, 2.6)})


def _pivot(recs, key):
    s = sorted({r["s"] for r in recs})
    d = sorted({r["delta"] for r in recs})
    Z = np.full((len(d), len(s)), np.nan)
    lut = {(r["s"], r["delta"]): r[key] for r in recs}
    for i, dd in enumerate(d):
        for j, ss in enumerate(s):
            Z[i, j] = lut.get((ss, dd), np.nan)
    return s, d, Z


def rebuild_all(data_dir, out_dir):
    import pathlib

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    made = []
    heat = [r for r in iter_points(data_dir, "exp02") if r.get("status") == "ok"]
    curves = [r for r in iter_points(data_dir, "exp02sq") if r.get("status") == "ok"]

    if curves:
        styles = {"afm": ("-", "o"), "topological": ("--", "s"),
                  "trivial": (":", "^")}
        fig, ax = plt.subplots()
        for r in sorted(curves, key=lambda r: r["rep"]):
            ls, mk = styles.get(r["rep"], ("-", "o"))
            ax.plot(np.asarray(r["q"]), np.asarray(r["Sq"]), ls, marker=mk,
                    markevery=4, markersize=3, label=r["rep"])
        ax.set_xlabel("$q$")
        ax.set_ylabel("$S(q)$")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(out / "sq_pra.pdf")
        fig.savefig(out / "sq_pra.png", dpi=600)
        plt.close(fig)
        made.append(str(out / "sq_pra.pdf"))

    for key, name, lab in (("Spi", "S_pi", r"$S(\pi)$"),
                           ("Ostr", "Ostr", "$O_{str}$"),
                           ("Q", "Q", "$Q$"),
                           ("ZtR", "ZtR", r"$\tilde Z_R$")):
        if not heat:
            continue
        s, d, Z = _pivot(heat, key)
        fig, ax = plt.subplots()
        im = ax.imshow(Z, origin="lower", aspect="auto",
                       extent=[min(s), max(s), min(d), max(d)])
        ax.set_xlabel("$s$")
        ax.set_ylabel(r"$\delta$")
        fig.colorbar(im, ax=ax, label=lab)
        fig.tight_layout()
        fig.savefig(out / f"{name}_pra.pdf")
        fig.savefig(out / f"{name}_pra.png", dpi=600)
        plt.close(fig)
        made.append(str(out / f"{name}_pra.pdf"))
    return made
