"""Diagnostic comparison figures for Experiment 04 — saved data only."""

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from experiments.exp03_reference import iter_reference
from ssh_xxz.io.store import iter_points


def _selected(var_dir):
    return [r for r in iter_points(var_dir, "exp04s") if r.get("status") == "ok"]


def rebuild_all(ref_dir, var_dir, out_dir):
    import pathlib

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ref = {(r["s"], r["delta"]): r for r in iter_reference(ref_dir)}
    sel = _selected(var_dir)
    made = []
    for key, rkey, title in (("Evar", "E0", "E"), ("Spi", "Spi", "S(pi)"),
                             ("Ostr", "Ostr", "Ostr")):
        fig, ax = plt.subplots()
        for d in sorted({r["delta"] for r in sel}):
            er = sorted((r["s"], ref[(r["s"], r["delta"])][rkey])
                        for r in sel if r["delta"] == d)
            ax.plot([p[0] for p in er], [p[1] for p in er], "k--", label="exact")
            for p in sorted({r["p"] for r in sel}):
                pts = sorted((r["s"], r[key]) for r in sel
                             if r["delta"] == d and r["p"] == p)
                ax.plot([q[0] for q in pts], [q[1] for q in pts], label=f"p={p}")
        ax.set_xlabel("s")
        ax.set_ylabel(title)
        ax.legend()
        ax.set_title(f"{title}(s) exact vs variational (diagnostic)")
        fig.savefig(out / f"cmp_{key}_diag.png")
        plt.close(fig)
        made.append(str(out / f"cmp_{key}_diag.png"))
    return made
