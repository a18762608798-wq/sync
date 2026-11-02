"""D06 combined 1x3 per-phase schematics (exp04 T009/T020): zero data input, pure drawing.

Circuit-leaning hybrid (not a literal qiskit circuit):
- 8 horizontal qubit wires (site 1 top = logical 0), time flows left to right;
- left column: init-state two-qubit links (gray bars; GHZ links follow
  qmeas.models.xxz pidx=0 middle-out CNOT fan-out, X/H omitted);
- then two layer blocks U^(1) and U^(k) joined by vertical dots;
- U^(1): F then S sublayer gate boxes (one rounded box per bond,
  orbit colors; same color + number = shared (theta, phi)).
- U^(k): empty frame with a big U^(k) label (same layout as U^(1),
  per-layer independent parameters; mapping in paper caption).
Faithful to docs/theory/psi0.md + docs/theory/ansatz.md for L = 8 only:
- D06a trivial: odd-bond singlet pairs; F = even (U_o U_e).
- D06b topo: |s>_{1,8} link + even-bond singlet pairs; F = odd (U_e U_o).
- D06c AFM: GHZ adjacent-link chain; F = even (U_o U_e).
Orbit colors/groups (same color = shared parameters):
group 1 = odd-outer pair bonds (1,2)&(7,8), group 2 = odd-inner pair
(3,4)&(5,6), group 3 = even-outer pair (2,3)&(6,7), group 4 = even-central
bond (4,5) self-mirror. Box text carries only the group index: same
color + number = one shared (theta, phi) pair, whose (theta_g, phi_g)
mapping is defined once in the paper caption, not per box.
No gate types beyond ansatz.md are drawn.

Project Python: .CondaPkg/.pixi/envs/default/bin/python.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FIGDIR = os.path.join(HERE, "..", "figs", "exp04")

GRAY = "0.45"
N = 8


def y_of(site):
    """Site 1..8 top-down (site 1 = logical 0, qiskit-style top)."""
    return N - site


GAP_L, GAP_R = 5.65, 7.15  # 与两侧 layer_frame 内边对齐


def draw_wires(ax, x0=0.0):
    xs = np.arange(N)
    for i in range(N):
        y = y_of(i + 1)
        ax.plot([x0, GAP_L], [y] * 2, color="black", linewidth=1.8,
                zorder=1)
        # 间隙内每线一根横虚线（省略的中间层），代替竖省略号。
        # U^(k) 框内不画线；框右留一小段引出线。
        ax.plot([GAP_L, GAP_R], [y] * 2, color="black", linewidth=1.8,
                linestyle=(0, (2, 2)), zorder=1)
        xr = X_SK + 0.75
        ax.plot([xr + 0.08, xr + 0.6], [y] * 2, color="black", linewidth=1.8,
                zorder=1)
        ax.scatter([x0], [y], s=36, color="white",
                   edgecolors="black", linewidths=1.2, zorder=3)
        ax.text(x0 - 0.25, y, rf"${i + 1}$", ha="right",
                va="center", fontsize=10)


def link_bar(ax, a, b, x, width=4.5, color=GRAY):
    """Gray vertical bar linking two wires = one two-qubit init link."""
    ya, yb = y_of(a), y_of(b)
    ax.plot([x, x], [yb, ya], color=color, linewidth=width, solid_capstyle="round")


def gate_box(ax, a, b, x, color, group, layer):
    """One orbit bond gate box spanning two wires."""
    ya, yb = y_of(a), y_of(b)
    box = FancyBboxPatch((x - 0.5, yb - 0.32), 1.0, ya - yb + 0.64,
                         boxstyle="round,pad=0.02", facecolor="white",
                         edgecolor=color, linewidth=2.4)
    ax.add_patch(box)
    ax.text(x, (ya + yb) / 2, f"${group}$", ha="center",
            va="center", fontsize=12, color=color)


def layer_frame(ax, x0, x1):
    frame = FancyBboxPatch((x0, -0.45), x1 - x0, 8.0,
                           boxstyle="round,pad=0.05", facecolor="none",
                           edgecolor="black", linewidth=1.8,
                           linestyle="-")
    ax.add_patch(frame)


def layer_frame_abbrev(ax, x0, x1):
    """Empty repeated-layer frame with a big U^(k) label.

    Later layers share U^(1)'s layout with independent (theta, phi);
    the frame stays empty, details in the paper caption.
    """
    layer_frame(ax, x0, x1)
    ax.text((x0 + x1) / 2, 3.55, r"$U^{(k)}$", ha="center",
            va="center", fontsize=22,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4))


def init_frame(ax):
    """Black box around the initial-state block (bonds + qubit dots).

    Same vertical extent and line style as the layer frames so the three
    boxes read as one family and their gaps stay even.
    """
    frame = FancyBboxPatch((X_INIT - 0.87, -0.45), INIT_W, 8.0,
                           boxstyle="round,pad=0.05", facecolor="none",
                           edgecolor="black", linewidth=1.8,
                           linestyle="-", zorder=1.5)
    ax.add_patch(frame)


def draw_sublayer(ax, bonds, x, layer):
    for (a, b), g in bonds:
        gate_box(ax, a, b, x, GROUP_COLORS[g], g, layer)


def finish(ax):
    ax.set_xlim(-1.05, 10.75)
    ax.set_ylim(-0.75, 8.9)
    ax.set_aspect("equal")
    ax.axis("off")


# Orbit groups: same group + color = one shared (theta, phi).
ODD_BONDS = [((1, 2), 1), ((7, 8), 1),
             ((3, 4), 2), ((5, 6), 2)]
EVEN_BONDS = [((2, 3), 3), ((6, 7), 3),
              ((4, 5), 4)]
# Init-link colors by initial state (phase identity is NOT reused here):
# trivial red / topo blue / Neel black.
INIT_RED = "#D62728"
INIT_BLUE = "#0072B2"
INIT_BLACK = "#000000"
# Orbit group colors avoid red/blue/black: green / purple / orange / brown.
GROUP_COLORS: dict = {1: "#009E73", 2: "#CC79A7",
                      3: "#E69F00", 4: "#8C564B"}

# Column x positions: init | U^(1): F, S | dots | U^(k): F, S.
# Gaps are kept equal: init box -> U^(1) frame -> U^(k) frame (0.75 each).
X_INIT, X_F1, X_S1, X_FK, X_SK = 0.75, 3.03, 4.83, 7.08, 8.88
INIT_W = 1.65         # init box width (left edge X_INIT-0.87, right -0.87+1.65)


def draw_panel(ax, phase):
    """Draw one phase schematic (init links + U^(1) + empty U^(k) frame)."""
    draw_wires(ax)
    init_frame(ax)
    if phase == "triv":
        # D06a trivial: odd-bond singlet pairs; F = even.
        for a, b in [(1, 2), (3, 4), (5, 6), (7, 8)]:
            link_bar(ax, a, b, X_INIT, color=INIT_RED)
        ax.text(X_INIT, 8.0, r"$|\psi_{\rm triv}\rangle$", ha="center",
                va="bottom", fontsize=11)
        draw_sublayer(ax, EVEN_BONDS, X_F1, "1")
        draw_sublayer(ax, ODD_BONDS, X_S1, "1")
    elif phase == "topo":
        # D06b topo: (1,8) link + even-bond pairs; F = odd.
        for a, b in [(2, 3), (4, 5), (6, 7)]:
            link_bar(ax, a, b, X_INIT, color=INIT_BLUE)
        link_bar(ax, 1, 8, X_INIT + 0.55, color=INIT_BLUE)
        ax.text(X_INIT + 0.25, 8.0, r"$|\psi_{\rm topo}\rangle$", ha="center",
                va="bottom", fontsize=11)
        draw_sublayer(ax, ODD_BONDS, X_F1, "1")
        draw_sublayer(ax, EVEN_BONDS, X_S1, "1")
    else:
        # D06c AFM: adjacent-link GHZ chain (qmeas xxz pidx=0 links);
        # F = even.
        for step, pairs in enumerate([[(4, 5), (5, 6)],
                                      [(3, 4), (6, 7)],
                                      [(2, 3), (7, 8)],
                                      [(1, 2)]]):
            x0 = 0.40 + 0.28 * step
            xs = [x0 - 0.11, x0 + 0.11] if len(pairs) == 2 else [x0]
            for (a, b), x in zip(pairs, xs):
                link_bar(ax, a, b, x, width=3.0, color=INIT_BLACK)
        ax.text(X_INIT, 8.0, r"$|\psi_{\rm N\acute{e}el}\rangle$", ha="center",
                va="bottom", fontsize=11)
        draw_sublayer(ax, EVEN_BONDS, X_F1, "1")
        draw_sublayer(ax, ODD_BONDS, X_S1, "1")
    layer_frame(ax, X_F1 - 0.75, X_S1 + 0.75)
    ax.text((X_F1 + X_S1) / 2, 8.0, r"$U^{(1)}$", ha="center",
            va="bottom", fontsize=10)
    layer_frame_abbrev(ax, X_FK - 0.75, X_SK + 0.75)
    finish(ax)


def main():
    from figure_style import apply_figure_style, finalize_figure, font_pt_for, uniform_text, PRINT_TEXT_PT

    palette = apply_figure_style()

    os.makedirs(FIGDIR, exist_ok=True)

    # Combined 1x3 (paper FIG.3): equal-size panels, (a)(b)(c) below labels.
    fig, axs = plt.subplots(1, 3, figsize=(13.2, 4.4))
    for ax, phase in zip(axs, ("triv", "topo", "neel")):
        draw_panel(ax, phase)
    for ax, letter in zip(axs, ("(a)", "(b)", "(c)")):
        ax.text(0.5, -0.045, letter, transform=ax.transAxes,
                fontsize=14, va="top", ha="center", clip_on=False)
    fig.tight_layout(w_pad=3.0)
    uniform_text(fig, font_pt_for(fig, PRINT_TEXT_PT))
    finalize_figure(fig, os.path.join(FIGDIR, "exp04_D06.pdf"))
    finalize_figure(fig, os.path.join(FIGDIR, "exp04_D06.png"))
    plt.close(fig)
    print("wrote: figs/exp04/exp04_D06.pdf + .png")


if __name__ == "__main__":
    main()
