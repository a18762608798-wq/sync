"""D03 three-curve plot + D04 combined 2x2 (exp02 T006).

Reads data/exp02/exp02_D03.npz and exp02_D04.npz only; no physics recomputed.
Style via the vendored scripts/figure_style.py. Self-checks grids, shapes,
and the D03<->D04 pi-point agreement before plotting.

Project Python: .CondaPkg/.pixi/envs/default/bin/python.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "..", "data", "exp02")
FIGDIR = os.path.join(HERE, "..", "figs", "exp02")

REP_LABELS = ["trivial", "topological", "afm"]
DISPLAY_LABELS = {"trivial": "trivial", "topological": "topo", "afm": "Néel"}
# D03: three solid lines, color-only distinction by phase identity,
# same convention as D09 initial states
# (trivial bluish-green / topo vermillion / AFM black; Okabe-Ito).
D03_COLORS = {"trivial": "#009E73", "topological": "#D55E00", "afm": "#000000"}
D03_LINESTYLE = "-"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--d03-only", action="store_true",
                        help="只更新含真机后处理结果的 D03 图")
    args = parser.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from figure_style import (apply_figure_style, finalize_figure, cell_edges,
                              effective_min_text_pt, font_pt_for, uniform_text,
                              PRINT_COL_PT)

    apply_figure_style()
    d03 = np.load(os.path.join(DATA, "exp02_D03.npz"))
    d04 = np.load(os.path.join(DATA, "exp02_D04.npz"))

    q = d03["q_grid"]
    curves = d03["curves"]
    assert q.shape == (99,) and curves.shape == (3, 99)
    assert abs(q[49] - np.pi) < 1e-12, "q grid must contain pi at k=50"
    with open(os.path.join(DATA, "exp02_D03_meta.json")) as f:
        assert json.load(f)["rep_labels"] == REP_LABELS

    s = d04["s_grid"]
    d = d04["delta_grid"]
    panels = {k: d04[k] for k in ("s_hat_pi", "o_hat_str", "q_val", "z_tilde")}
    s_edges = cell_edges(s, lo=0.0, hi=1.0)
    d_edges = cell_edges(d, lo=-3.0, hi=3.0)
    for k, v in panels.items():
        assert v.shape == (99, 121) and np.isfinite(v).all(), f"panel {k} incomplete"
    # D03<->D04 pi-point agreement at rep coords (k=50 -> q=pi).
    # 0-based numpy indices; representative points come from the S01 manifest.
    with open(os.path.join(DATA, "exp02_manifest.json")) as f:
        rep_pts = json.load(f)["rep_points"]
    s_index = {round(float(v), 10): i for i, v in enumerate(s)}
    d_index = {round(float(v), 10): j for j, v in enumerate(d)}
    rep_idx = {label: (s_index[round(rep_pts[label][0], 10)],
                       d_index[round(rep_pts[label][1], 10)])
               for label in REP_LABELS}
    for r, label in enumerate(REP_LABELS):
        i, j = rep_idx[label]
        assert abs(curves[r, 49] - panels["s_hat_pi"][i, j]) < 1e-9, f"D03/D04 pi mismatch {label}"

    os.makedirs(FIGDIR, exist_ok=True)

    # D03: three normalised Ŝ(q) curves sharing axes.
    # Drawn at single-column width (~107 mm); the 163 mm default would shrink
    # to ~0.53 in LaTeX and drop ticks/legend below the 8 pt floor.
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6.8, 4.5),
                                   sharex=True, sharey=True)
    for ax in (ax0, ax1):
        ax.set_box_aspect(1)
        ax.set_xlim(0.0, 2.0 * np.pi)
        ax.set_xticks([0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2.0 * np.pi])
        ax.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$",
                            r"$2\pi$"])
        ax.set_xlabel(r"$q$")
    for r, label in enumerate(REP_LABELS):
        ax0.plot(q, curves[r], color=D03_COLORS[label],
                 linestyle=D03_LINESTYLE, linewidth=2.0,
                 label=DISPLAY_LABELS[label])
    peak = curves[2].max()
    for ax in (ax0, ax1):
        ax.set_ylim(0.0, peak * 1.05)
    ax0.plot([np.pi, np.pi], [0.0, peak], color="black", linewidth=1.0,
             linestyle=":", zorder=2)
    ax0.plot(np.pi, peak, marker="o", color=D03_COLORS["afm"],
             markeredgecolor="black", markersize=6, linestyle="None",
             zorder=5)
    ax0.set_ylabel(r"$\hat S(q)$")
    ax0.set_title("simulator")
    ax1.set_title(r"hardware ($p=1$)")
    for ax, letter in ((ax0, "(a)"), (ax1, "(b)")):
        ax.text(0.035, 0.93, letter, transform=ax.transAxes,
                fontsize=13, va="top", ha="left", color="black")
    handles, leg_labels = ax0.get_legend_handles_labels()
    fig.legend(handles, leg_labels, frameon=False, loc="lower center",
               bbox_to_anchor=(0.5, 0.03), ncol=3, fontsize=11)
    fig.subplots_adjust(bottom=0.28, top=0.88, wspace=0.25)
    # D03 hardware panel (exp06 T027/T028): p=1 phase-matched states,
    # full 99-point continuous lines, same colors as simulator.
    hw_path = os.path.join(HERE, "..", "data", "exp06", "d03hw",
                           "exp06_D03hw.npz")
    if os.path.exists(hw_path):
        hw = np.load(hw_path)
        hw_labels = [str(x) for x in hw["labels"]]
        hcurves = hw["S_hat"]
        assert hw["q_grid"].shape == q.shape and np.allclose(hw["q_grid"], q)
        hmap = {"triv": 0, "topo": 1, "afm": 2}
        for hl in hw_labels:
            r = hmap[hl]
            ax1.plot(q, hcurves[r], color=D03_COLORS[REP_LABELS[r]],
                     linestyle="-", linewidth=2.0)
        print("D03 hardware panel: 3 lines x 99 q")
    uniform_text(fig, font_pt_for(fig, PRINT_COL_PT))
    eff = effective_min_text_pt(fig, 86.0)
    assert eff >= 8.0, f"D03 smallest text is {eff:.1f} pt after scaling to 86 mm"
    print(f"D03 smallest effective text at 86 mm: {eff:.1f} pt")
    finalize_figure(fig, os.path.join(FIGDIR, "exp02_D03.pdf"))
    finalize_figure(fig, os.path.join(FIGDIR, "exp02_D03.png"))
    plt.close(fig)
    print("wrote: figs/exp02/exp02_D03.pdf + .png")
    if args.d03_only:
        return

    # D04 combined 2x2 (paper FIG.1): each subplot box is forced square
    # (set_box_aspect(1)); (a)-(d) sit in the lower-left corner, black on the
    # light (a)/(b) maps and white on the dark red/blue (c)/(d) maps.
    # Colours: signed/centred quantities use a red-blue diverging map centred at 0;
    # non-negative quantities use a white-based single-hue sequential map, so the
    # whole 2x2 shares one red/blue/white family.
    from matplotlib.colors import TwoSlopeNorm

    panels4 = [(r"$\hat S(\pi)$", "s_hat_pi", "Reds",
                dict(vmin=0.2, vmax=1.0), [0.2, 0.6, 1.0]),
               (r"$\hat O_{\rm str}$", "o_hat_str", "Blues",
                dict(vmin=0.0, vmax=1.0), [0.0, 0.5, 1.0]),
               (r"$Q$", "q_val", "RdBu_r",
                dict(norm=TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=1.0)),
                [-1.0, 0.0, 1.0]),
               (r"$\tilde{Z}_R$", "z_tilde", "RdBu_r",
                dict(norm=TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=1.0)),
                [-1.0, 0.0, 1.0])]
    # Shared axes: s labels only on the bottom row, delta only on the
    # left column. Square boxes keep all four panels identical in shape.
    fig2, axs = plt.subplots(2, 2, figsize=(6.6, 6.6),
                             sharex=True, sharey=True)
    for idx, (ax, (title, key, cmap, kw, cb_ticks, letter)) in enumerate(zip(
            axs.flat,
            [(t, k, c, w, cb, L)
             for (t, k, c, w, cb), L in
             zip(panels4, ("(a)", "(b)", "(c)", "(d)"))])):
        mesh = ax.pcolormesh(s_edges, d_edges, panels[key].T,
                             shading="flat", cmap=cmap, **kw)
        cbar = fig2.colorbar(mesh, ax=ax, shrink=0.9,
                             anchor=(1.0, 0.0), pad=0.02)
        cbar.set_ticks(cb_ticks)
        cbar.ax.set_title(title, fontsize=22, pad=12, loc="left")
        cbar.ax.tick_params(labelsize=17)
        ax.set_xticks([0.0, 0.5, 1.0])
        ax.set_yticks([-3.0, 0.0, 3.0])
        ax.tick_params(axis="both", labelsize=17)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(-3.0, 3.0)
        ax.set_box_aspect(1)
        ax.text(0.035, 0.035, letter, transform=ax.transAxes,
                fontsize=17, va="bottom", ha="left",
                color="black" if idx < 2 else "white")
    for ax in (axs[1, 0], axs[1, 1]):
        ax.set_xlabel(r"$s$", fontsize=18)
    for ax in (axs[0, 0], axs[1, 0]):
        ax.set_ylabel(r"$\delta$", fontsize=18)
    fig2.tight_layout()
    uniform_text(fig2, font_pt_for(fig2, PRINT_COL_PT))
    eff2 = effective_min_text_pt(fig2, 86.0)
    assert eff2 >= 8.0, f"exp02_D04: {eff2:.1f} pt at 86 mm (< 8 pt)"
    print(f"exp02_D04 2x2 smallest effective text at 86 mm: {eff2:.1f} pt")
    finalize_figure(fig2, os.path.join(FIGDIR, "exp02_D04.pdf"))
    finalize_figure(fig2, os.path.join(FIGDIR, "exp02_D04.png"))
    plt.close(fig2)
    print("wrote: figs/exp02/exp02_D04.pdf + .png")

    meta = {"rep_labels": REP_LABELS, "linestyle": D03_LINESTYLE,
            "colors": D03_COLORS,
            "figures": ["figs/exp02/exp02_D03.png",
                        "figs/exp02/exp02_D04.png"],
            "python": {"executable": sys.executable, "version": sys.version.split()[0],
                       "numpy": np.__version__, "matplotlib": matplotlib.__version__}}
    with open(os.path.join(FIGDIR, "exp02_D034_meta.json"), "w") as f:
        json.dump(meta, f, indent=1)


if __name__ == "__main__":
    main()
