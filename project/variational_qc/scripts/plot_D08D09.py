"""Paper-layer 2x2 composite of D09 (exp04) and D08 (exp06 v3).

Top row: D09 cost functions at p=1 (panels a,b: delta=-2, 0.85) from
data/exp04/exp04_S06.npz + exp04_D09.npz.
Bottom row: D08 hardware-vs-simulator Q (panels c,d) from
data/exp06/joint/exp06_D08_joint.npz + manifest (window/endpoints).

Read-only: nothing is recomputed and neither exp04_D09.* nor exp06_D08.*
is overwritten (both remain the spec-level products).
Style: figure_style.py; vector PDF + 300 dpi PNG -> figs/exp06/.
Run through scripts/run_py.jl (CondaPkg env).
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE)
E4 = os.path.join(REPO, "data", "exp04")
E6 = os.path.join(REPO, "data", "exp06", "joint")
FIGDIR = os.path.join(REPO, "figs", "exp06")

P_LAYER = 1
LEGS = ["triv", "topo", "AFM"]
LEG_DISPLAY = {"triv": "triv", "topo": "topo", "AFM": "Néel"}
LEG_STYLE = {"triv": "--", "topo": ":", "AFM": "-."}
LEG_COLOR = {"triv": "#009E73", "topo": "#D55E00", "AFM": "#000000"}
PHASE_NAME = {1: "triv", 2: "topo", 3: "AFM"}
BAND_LABEL = {1: "triv", 2: "topo", 3: "Néel"}
D09_LINES = [("dm2", 0, -2.0), ("d085", 1, 0.85)]

SIM_COLORS = ["#000000", "#7f7f7f"]  # p=1 black; p=2 gray
BAND_COLOR = {1: "#D62728", 2: "#0072B2", 3: "#000000"}
LINE_OF_DELTA = {-2.0: ("dm2", 1), 0.85: ("d085", 2)}


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


def draw_d09(ax, d, d09, colors, palette, tag, di, delta):
    s = d["s_grid"]
    leg_E = d[f"{tag}_leg_E"][:, :, P_LAYER - 1]
    assert np.array_equal(d[f"{tag}_E_star"][:, P_LAYER - 1],
                          leg_E.min(axis=1))
    phase = d09["phase"]
    runs = bands(phase[:, di])
    for i0, i1, name in runs:
        ax.axvspan(s[i0] - 0.005, s[i1] + 0.005, color=colors[name],
                   alpha=0.22, linewidth=0, zorder=0)
    ax.plot(s, d09["E0"][:, di], color="#0072B2", linewidth=2.0,
            linestyle="-", zorder=2, label=r"$E_0$ (exact)")
    for leg in LEGS:
        li = LEGS.index(leg)
        ax.plot(s, leg_E[:, li], color=LEG_COLOR[leg], linewidth=1.6,
                linestyle=LEG_STYLE[leg], zorder=3, label=LEG_DISPLAY[leg])
    for i0, i1, name in runs:
        li = int(np.argmin(leg_E[i0:i1 + 1].mean(axis=0)))
        mid = (i0 + i1) // 2
        ax.plot(s[mid], leg_E[mid, li], marker="o",
                color=LEG_COLOR[LEGS[li]], markeredgecolor="black",
                markeredgewidth=1.1, markersize=6, linestyle="None", zorder=4)
    ax.set_xlim(0.0, 1.0)
    if di == 0:
        ax.set_ylabel(r"$C$")
    ax.set_title(rf"$\delta={delta:g}$", fontsize=13)
    ax.legend(frameon=False, fontsize=8, loc="best", ncol=2)


def draw_d08(ax, d, d09, manifest, delta):
    d09_phase = d09["phase"]
    sg = np.asarray(d09["s_grid"])
    s15 = np.asarray(d["s_idx"])
    deltas = np.asarray(d["deltas"])
    m = np.asarray([abs(float(x) - delta) < 1e-9 for x in deltas])
    assert int(m.sum()) == 15, (delta, int(m.sum()))
    for p, color in zip((1, 2), SIM_COLORS):
        ax.plot(s15[m] / 100.0, np.asarray(d[f"q_sim_p{p}"])[m], "-",
                color=color, linewidth=1.5, label=f"sim p={p}")
    y = np.asarray(d["win_mean"])[m]
    ye = np.asarray(d["win_se"])[m]
    _line, di = LINE_OF_DELTA[delta]
    band = np.asarray(d09_phase[:, di - 1]).astype(int)
    b15 = np.array([band[int(np.argmin(np.abs(sg - s / 100.0)))]
                    for s in s15[m]])
    for b in (1, 2, 3):
        mb = b15 == b
        if not np.any(mb):
            continue
        ax.errorbar(s15[m][mb] / 100.0, y[mb], yerr=ye[mb], fmt="o",
                    color=BAND_COLOR[b], markersize=4, capsize=2.5,
                    markeredgecolor="black", markeredgewidth=0.6,
                    label=f"exp p=1 ({BAND_LABEL[b]})")
    ax.set_xlim(0.0, 1.025)
    if delta == -2.0:
        ax.set_ylabel("$Q$")


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from figure_style import apply_figure_style, finalize_figure, font_pt_for, uniform_text, PRINT_TEXT_PT

    palette = apply_figure_style()
    cmap = plt.get_cmap("RdBu_r")
    colors = {"triv": cmap(1.0), "AFM": cmap(0.5), "topo": cmap(0.0)}

    d = np.load(os.path.join(E4, "exp04_S06.npz"))
    d09 = np.load(os.path.join(E4, "exp04_D09.npz"))
    dj = np.load(os.path.join(E6, "exp06_D08_joint.npz"))
    with open(os.path.join(E6, "exp06_manifest_joint.json"),
              encoding="utf-8") as f:
        manifest = json.load(f)

    assert d["s_grid"].shape == (99,)
    assert np.allclose(d09["s_grid"], d["s_grid"])
    assert np.array_equal(np.asarray(d09["deltas"], float),
                          np.array([-2.0, 0.85]))

    fig, axes = plt.subplots(2, 2, figsize=(8.6, 7.2))
    for ax, (tag, di, delta) in zip(axes[0], D09_LINES):
        draw_d09(ax, d, d09, colors, palette, tag, di, delta)
    for ax, delta in zip(axes[1], (-2.0, 0.85)):
        draw_d08(ax, dj, d09, manifest, delta)

    letters = ("(a)", "(b)", "(c)", "(d)")
    for ax, letter in zip(axes.flat, letters):
        ax.text(0.0, -0.155, letter, transform=ax.transAxes,
                fontsize=12, va="top", ha="left", clip_on=False)

    seen = {}
    for ax in axes[1]:
        h, lab = ax.get_legend_handles_labels()
        for hi, li in zip(h, lab):
            seen.setdefault(li, hi)
    fig.supxlabel(r"$s$", y=0.055)
    fig.legend(list(seen.values()), list(seen.keys()), loc="lower center",
               bbox_to_anchor=(0.5, 0.0), ncol=5, fontsize=9,
               frameon=False)
    fig.tight_layout(rect=(0, 0.075, 1, 1), h_pad=2.6, w_pad=1.6)
    uniform_text(fig, font_pt_for(fig, PRINT_TEXT_PT))
    out = os.path.join(FIGDIR, "exp06_D08D09")
    finalize_figure(fig, out + ".pdf")
    finalize_figure(fig, out + ".png")
    plt.close(fig)
    win = manifest["window"]
    print(f"wrote figs/exp06/exp06_D08D09.pdf + .png "
          f"(N={win['N']} win=[{win['start']},{win['start'] + win['length']}) "
          f"d_raw={win['d_raw']:.4f} r={win['r']:.4f})")


if __name__ == "__main__":
    main()
