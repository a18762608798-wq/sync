"""PRA reference curves for Experiment 03 — saved data only."""

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt

from experiments.exp03_reference import iter_reference

plt.rcParams.update({"font.family": "serif", "font.size": 8,
                     "figure.figsize": (3.4, 2.6)})


def rebuild_all(data_dir, out_dir):
    import pathlib

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    recs = list(iter_reference(data_dir))
    made = []
    for key, lab in (("E0", "$E_0$"), ("Spi", r"$S(\pi)$"), ("Ostr", "$O_{str}$")):
        fig, ax = plt.subplots()
        for d in sorted({r["delta"] for r in recs}):
            pts = sorted((r["s"], r[key]) for r in recs if r["delta"] == d)
            ax.plot([p[0] for p in pts], [p[1] for p in pts], label=rf"$\delta={d:g}$")
        ax.set_xlabel("$s$")
        ax.set_ylabel(lab)
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(out / f"ref_{key}_pra.pdf")
        fig.savefig(out / f"ref_{key}_pra.png", dpi=600)
        plt.close(fig)
        made.append(str(out / f"ref_{key}_pra.pdf"))
    return made
