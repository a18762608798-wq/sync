"""D02 appendix plots (exp03 T015/T020): one combined 1x3 figure exp03_D02.pdf.

Reads data/exp03/exp03_D02.npz only; no physics recomputed.
(a) Delta_sec vs s (four paper sizes),
(b) the same curves zoomed to s in [0.52, 0.65], minima marked,
(c) Delta_sec vs 1/L with the a+b/L+c/L^2 fit and the intercept a marked.
Style via the vendored scripts/figure_style.py. Self-checks grids and shapes.
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.environ.get("EXP03_DATA_DIR", os.path.join(HERE, "..", "data", "exp03"))
FIGDIR = os.environ.get("EXP03_FIG_DIR", os.path.join(HERE, "..", "figs", "exp03"))

LS = [8, 16, 24, 32]
LINESTYLES = ["-", "--", ":", "-.", (0, (3, 1, 1, 1))]
WINDOW = (0.52, 0.65)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from figure_style import (apply_figure_style, finalize_figure,
                               effective_min_text_pt, font_pt_for, uniform_text,
                               PRINT_TEXT_PT)

    palette = apply_figure_style()
    d = np.load(os.path.join(DATA, "exp03_D02.npz"))

    assert list(d["Ls"]) == LS
    s = d["s_grid"]
    D = d["Delta"]
    assert s.shape == (99,) and D.shape == (len(LS), 99)
    assert abs(s[49] - 0.5) < 1e-12, "grid must contain s=0.5 at i=50"
    assert np.isfinite(D).all()

    a, b, c = float(d["fit_a"]), float(d["fit_b"]), float(d["fit_c"])
    xs = np.array(d["fit_x"])
    ys = np.array(d["fit_y"])
    assert xs.shape == (len(LS),) and ys.shape == (len(LS),)
    for r in range(len(LS)):
        assert abs(ys[r] - D[r, 49]) < 1e-12, "D02c must reuse the s=0.5 point"

    os.makedirs(FIGDIR, exist_ok=True)

    # 1x3 combined: equal-size subplots, panel labels inside the lower right.
    fig123, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(10.5, 3.4))
    # (a) full range: gap vs s for the four paper sizes.
    ax = ax_a
    for r, L in enumerate(LS):
        ax.plot(s, D[r], color=palette[r], linestyle=LINESTYLES[r],
                linewidth=1.8, label=rf"$L={L}$")
    ax.set_xlabel(r"$s$", fontsize=16)
    ax.set_ylabel(r"$\Delta_{\mathrm{sec}}$", fontsize=16)
    ax.tick_params(axis="both", labelsize=14)
    ax.text(0.965, 0.06, "(a)", transform=ax.transAxes,
            va="bottom", ha="right", zorder=5)
    ax.legend(frameon=False, fontsize=14, loc="upper right")

    # (b) zoom on the closing window, minima marked when they fall inside it.
    ax = ax_b
    win = (s >= WINDOW[0] - 1e-12) & (s <= WINDOW[1] + 1e-12)
    for r, L in enumerate(LS):
        ax.plot(s, D[r], color=palette[r], linestyle=LINESTYLES[r],
                linewidth=1.8)
        m = D[r].argmin()
        if WINDOW[0] <= s[m] <= WINDOW[1]:
            ax.plot(s[m], D[r, m], marker="o", color=palette[r],
                    markeredgecolor="black", markeredgewidth=1.2,
                    markersize=6, linestyle="None", zorder=3)
    ax.set_xlim(*WINDOW)
    lo, hi = D[:, win].min(), D[:, win].max()
    pad = 0.06 * (hi - lo)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_xlabel(r"$s$", fontsize=16)
    ax.set_ylabel(r"$\Delta_{\mathrm{sec}}$", fontsize=16)
    ax.tick_params(axis="both", labelsize=14)
    ax.text(0.965, 0.06, "(b)", transform=ax.transAxes,
            va="bottom", ha="right", zorder=5)

    # (c) gap vs 1/L at s=0.5 + quadratic fit; intercept a marked.
    ax = ax_c
    xline = np.linspace(0.0, xs.max() * 1.08, 200)
    ax.plot(xline, a + b * xline + c * xline ** 2,
            color="black", linewidth=1.2, linestyle="--", zorder=2)
    for r, L in enumerate(LS):
        ax.plot(xs[r], ys[r], marker="o", color=palette[r],
                markeredgecolor="black", markersize=6, linestyle="None",
                zorder=3)
    ax.plot(0.0, a, marker="s", color="black", markersize=5, zorder=4,
            linestyle="None")
    ax.set_xlim(-0.004, xs.max() * 1.12)
    ax.set_ylim(min(0.0, a) - 0.4, ys.max() * 1.10)
    ax.set_xlabel(r"$1/L$", fontsize=16)
    ax.set_ylabel(r"$\Delta_{\mathrm{sec}}$", fontsize=16)
    ax.tick_params(axis="both", labelsize=14)
    ax.text(0.965, 0.06, "(c)", transform=ax.transAxes,
            va="bottom", ha="right", zorder=5)

    fig123.tight_layout()
    uniform_text(fig123, font_pt_for(fig123, PRINT_TEXT_PT))
    eff = effective_min_text_pt(fig123, 165.0)
    assert eff >= 8.0, f"D02 1x3 smallest text is {eff:.1f} pt at 165 mm (< 8 pt)"
    print(f"D02 1x3 smallest effective text at 165 mm: {eff:.1f} pt")
    finalize_figure(fig123, os.path.join(FIGDIR, "exp03_D02.pdf"))
    finalize_figure(fig123, os.path.join(FIGDIR, "exp03_D02.png"))
    plt.close(fig123)
    print("wrote: figs/exp03/exp03_D02.pdf + .png")


if __name__ == "__main__":
    main()
