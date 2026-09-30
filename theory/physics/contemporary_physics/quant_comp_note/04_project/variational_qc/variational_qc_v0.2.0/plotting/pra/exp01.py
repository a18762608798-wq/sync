"""PRA publication figures for Experiment 01 — saved data only.

Constrained by `pra-paper-figures` + experiment specs; style changes here
MUST NOT require physics reruns (VII).
"""

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib import pyplot as plt

from plotting.diagnostic.exp01_scaling import fit_scaling
from ssh_xxz.io.store import iter_points

plt.rcParams.update({"font.family": "serif", "font.size": 8,
                     "figure.figsize": (3.4, 2.6)})


def rebuild_all(data_dir, out_dir):
    import pathlib

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    made = []
    grid = [r for r in iter_points(data_dir, "exp01") if r.get("status") == "ok"]
    gaps = [r for r in iter_points(data_dir, "exp01gap") if r.get("status") == "ok"]

    if grid:
        s = sorted({r["s"] for r in grid})
        d = sorted({r["delta"] for r in grid})
        Z = np.full((len(d), len(s)), np.nan)
        lut = {(r["s"], r["delta"]): r["ZtR"] for r in grid}
        for i, dd in enumerate(d):
            for j, ss in enumerate(s):
                Z[i, j] = lut.get((ss, dd), np.nan)
        fig, ax = plt.subplots()
        im = ax.imshow(Z, origin="lower", aspect="auto",
                       extent=[min(s), max(s), min(d), max(d)])
        ax.set_xlabel("$s$")
        ax.set_ylabel(r"$\delta$")
        fig.colorbar(im, ax=ax, label=r"$\tilde Z_R$")
        fig.tight_layout()
        fig.savefig(out / "phase_pra.pdf")
        fig.savefig(out / "phase_pra.png", dpi=600)
        plt.close(fig)
        made.append(str(out / "phase_pra.pdf"))

    if gaps:
        fig, ax = plt.subplots()
        for L in sorted({r["L"] for r in gaps}):
            pts = sorted((r["s"], r["draw"]) for r in gaps if r["L"] == L)
            ax.plot([p[0] for p in pts], [p[1] for p in pts], label=f"$L={L}$")
        ax.set_xlabel("$s$")
        ax.set_ylabel(r"$\Delta_{\rm raw}$")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(out / "gaps_pra.pdf")
        fig.savefig(out / "gaps_pra.png", dpi=600)
        plt.close(fig)
        made.append(str(out / "gaps_pra.pdf"))

        sc = [(1.0 / r["L"], r["draw"]) for r in gaps if r["s"] == 0.5]
        if sc:
            xs = np.array([p[0] for p in sc])
            ys = np.array([p[1] for p in sc])
            a, b = fit_scaling(xs, ys)
            fig, ax = plt.subplots()
            ax.scatter(xs, ys, s=8)
            xx = np.array([0.0, max(xs)])
            ax.plot(xx, a * xx + b)
            ax.set_xlabel("$1/L$")
            ax.set_ylabel(r"$\Delta_{\rm raw}(s=0.5)$")
            ax.text(0.05, 0.9, rf"$a={a:.4g},\ b={b:.4g}$",
                    transform=ax.transAxes, va="top")
            fig.tight_layout()
            fig.savefig(out / "scaling_pra.pdf")
            fig.savefig(out / "scaling_pra.png", dpi=600)
            plt.close(fig)
            made.append(str(out / "scaling_pra.pdf"))
    return made
