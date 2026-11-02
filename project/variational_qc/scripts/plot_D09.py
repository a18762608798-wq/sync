"""D09 cost-function comparison (exp04 T021): one combined 1x2 figure, one panel per δ line.

Reads data/exp04/exp04_S06.npz (p=1 subset) and data/exp04/exp04_D09.npz
(exact E0 + physical phase labels, built in Julia from shared-01 S01).
No physics recomputed here.

Each figure: three initial states C_a(s) at p=1, exact E0(s), and the physical
phase bands (trivial red / AFM white / topo blue, same family as D04d).
Inside each phase band the cheapest initial state is marked.

Run through scripts/run_py.jl (CondaPkg env; needs env\\Library\\bin on PATH).
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "..", "data", "exp04")
FIGDIR = os.path.join(HERE, "..", "figs", "exp04")

P_LAYER = 1
LEGS = ["triv", "topo", "AFM"]
LEG_DISPLAY = {"triv": "triv", "topo": "topo", "AFM": "Néel"}
LEG_STYLE = {"triv": "--", "topo": ":", "AFM": "-."}
# Leg colors complement their phase bands (Okabe-Ito, colorblind-safe):
# trivial red band -> bluish green, topo blue band -> vermillion,
# AFM white band -> black (E0 stays black solid, wider; AFM is dashdot).
LEG_COLOR = {"triv": "#009E73", "topo": "#D55E00", "AFM": "#000000"}
PHASE_NAME = {1: "triv", 2: "topo", 3: "AFM"}
LINES = [("dm2", 0, "D09a", -2.0), ("d085", 1, "D09b", 0.85)]


def phase_colors():
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap("RdBu_r")
    # Same convention as D04d: Z̃_R>0 (trivial) red, ~0 (AFM) white, <0 (topo) blue.
    return {"triv": cmap(1.0), "AFM": cmap(0.5), "topo": cmap(0.0)}


def bands(phase):
    """Contiguous runs of equal phase -> (start, stop, name)."""
    out = []
    i = 0
    while i < len(phase):
        j = i
        while j + 1 < len(phase) and phase[j + 1] == phase[i]:
            j += 1
        out.append((i, j, PHASE_NAME[int(phase[i])]))
        i = j + 1
    return out


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from figure_style import apply_figure_style, finalize_figure, DEFAULT_PALETTE

    palette = apply_figure_style()
    colors = phase_colors()

    d = np.load(os.path.join(DATA, "exp04_S06.npz"))
    d09 = np.load(os.path.join(DATA, "exp04_D09.npz"))
    s = d["s_grid"]
    assert s.shape == (99,)
    assert np.allclose(d09["s_grid"], s)
    assert list(d["deltas"]) == [-2.0, 0.85]
    assert np.array_equal(np.asarray(d09["deltas"], float), np.array([-2.0, 0.85]))
    phase = d09["phase"]
    E0 = d09["E0"]
    assert phase.shape == (99, 2) and E0.shape == (99, 2)
    assert np.isfinite(E0).all()

    os.makedirs(FIGDIR, exist_ok=True)
    # Combined 1x2 (paper FIG.4): each panel keeps the original 3.6x2.8
    # geometry with its own y axis (ticks + label, as in the standalone
    # figures), (a)(b) below labels.
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6))
    for (tag, di, _fid, delta), ax, letter in zip(
            LINES, axes, ("(a)", "(b)")):
        leg_E = d[f"{tag}_leg_E"][:, :, P_LAYER - 1]
        E_star = d[f"{tag}_E_star"][:, P_LAYER - 1]
        assert leg_E.shape == (99, 3)
        assert np.array_equal(E_star, leg_E.min(axis=1))

        runs = bands(phase[:, di])
        for i0, i1, name in runs:
            ax.axvspan(s[i0] - 0.005, s[i1] + 0.005, color=colors[name],
                       alpha=0.22, linewidth=0, zorder=0)

        ax.plot(s, E0[:, di], color="#0072B2", linewidth=2.0, linestyle="-",
                zorder=2, label=r"$E_0$ (exact)")
        for leg in LEGS:
            li = LEGS.index(leg)
            ax.plot(s, leg_E[:, li], color=LEG_COLOR[leg], linewidth=1.6,
                    linestyle=LEG_STYLE[leg], zorder=3, label=LEG_DISPLAY[leg])

        # Cheapest initial state inside each phase band.
        for i0, i1, name in runs:
            li = int(np.argmin(leg_E[i0:i1 + 1].mean(axis=0)))
            mid = (i0 + i1) // 2
            ax.plot(s[mid], leg_E[mid, li], marker="o", color=LEG_COLOR[LEGS[li]],
                    markeredgecolor="black", markeredgewidth=1.1,
                    markersize=6, linestyle="None", zorder=4)

        ax.set_xlim(0.0, 1.0)
        ax.set_xlabel(r"$s$")
        ax.set_ylabel(r"$C$")
        ax.set_title(rf"$\delta={delta:g}$, $p={P_LAYER}$")
        ax.legend(frameon=False, fontsize=9, loc="best", ncol=2)
        ax.text(0.5, -0.35, letter, transform=ax.transAxes,
                fontsize=12, va="top", ha="center", clip_on=False)
        print(f"panel {letter}: δ={delta:g} "
              f"(bands: {[(n, i1 - i0 + 1) for i0, i1, n in runs]})")

    fig.tight_layout(w_pad=2.0)
    finalize_figure(fig, os.path.join(FIGDIR, "exp04_D09.pdf"))
    finalize_figure(fig, os.path.join(FIGDIR, "exp04_D09.png"))
    plt.close(fig)
    print("wrote: figs/exp04/exp04_D09.pdf + .png")


if __name__ == "__main__":
    main()
