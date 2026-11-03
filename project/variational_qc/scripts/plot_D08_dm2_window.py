"""Plot the delta=-2 best-window diagnostic or its fixed-window companion.

First run scripts/diag_exp06_dm2_window.jl, then:
    julia --project=. scripts/run_py.jl scripts/plot_D08_dm2_window.py
For delta=0.85 on that same window, first run the Julia script with
--companion, then this plotter with --delta 0.85. No re-selection occurs.
No formal D08 products or paper files are written.
"""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from figure_style import (
    PRINT_COL_PT,
    apply_figure_style,
    effective_min_text_pt,
    finalize_figure,
    font_pt_for,
    uniform_text,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delta", type=float, choices=(-2.0, 0.85), default=-2.0)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    data_dir = repo / "data" / "exp06" / "diagnostics" / "dm2_window"
    companion = args.delta == 0.85
    manifest_file = "d085_same_window_manifest.json" if companion else "manifest.json"
    data_file = "d085_same_window.npz" if companion else "dm2_window.npz"
    with (data_dir / manifest_file).open(encoding="utf-8") as stream:
        manifest = json.load(stream)
    data = np.load(data_dir / data_file)
    assert manifest["diagnostic_only"] and manifest["reference_p"] == 1
    assert manifest["delta"] == args.delta
    assert manifest["endpoint_points"] == 30 and manifest["scored_points"] == 15
    for relative, expected in manifest["sources_sha256"].items():
        assert hashlib.sha256((repo / relative).read_bytes()).hexdigest() == expected, \
            f"diagnostic source changed: {relative}"
    if companion:
        assert manifest["window_selected_on_delta"] == -2.0
        assert manifest["window_reselected"] is False
    win = manifest["window"]
    assert data["q_units"].shape == (win["length"], 15)

    apply_figure_style()
    fig, ax = plt.subplots(figsize=(5.2, 6.4))
    ax.set_box_aspect(1)
    s = data["s_grid"]
    # Preserve the formal D08 colors; linestyle also distinguishes the depths.
    ax.plot(s, data["q_sim_p1"], color="#7f7f7f", linewidth=1.8,
            linestyle="-", label=r"sim $p=1$")
    ax.plot(s, data["q_sim_p2"], color="#1a1a1a", linewidth=1.8,
            linestyle="--", label=r"sim $p=2$")
    for phase, color, marker, label in (
        (1, "#D62728", "o", "hw triv"),
        (2, "#0072B2", "s", "hw topo"),
        (3, "#000000", "^", "hw Néel"),
    ):
        mask = data["phase"] == phase
        if np.any(mask):
            ax.errorbar(s[mask], data["win_mean"][mask],
                        yerr=data["win_se"][mask], fmt=marker, color=color,
                        markersize=6, markeredgecolor="black", markeredgewidth=0.8,
                        capsize=3, elinewidth=1.5, label=label, zorder=3)
    ax.set_xlim(0.0, 1.025)
    ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel(r"$s$")
    ax.set_ylabel(r"$Q$")
    ax.set_title(rf"$\delta={args.delta:g}$; hardware $p=1$")
    fig.text(0.55, 0.175,
             rf"Window $[{win['start']},{manifest['window_stop']})$, "
             rf"$n={win['length']}$; $r={win['r']:.4f}$, "
             rf"$d_{{\rm raw}}={win['d_raw']:.4f}$",
             ha="center", va="center")
    # Keep the data unobstructed and use the agreed single-row lower legend.
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.52, 0.025),
               ncol=len(labels), frameon=False,
               columnspacing=0.55 if companion else 0.85,
               handlelength=1.1 if companion else 1.6,
               handletextpad=0.3 if companion else 0.4)
    fig.subplots_adjust(left=0.16, right=0.97, bottom=0.29, top=0.94)
    uniform_text(fig, font_pt_for(fig, PRINT_COL_PT))
    fig.canvas.draw()
    bbox = ax.get_window_extent()
    assert np.isclose(bbox.width, bbox.height, rtol=1e-8)
    eff = effective_min_text_pt(fig, PRINT_COL_PT / 72.0 * 25.4)
    assert np.isclose(eff, 9.0)

    name = "exp06_D08_d085_dm2_window" if companion else "exp06_D08_dm2_window"
    out = repo / "figs" / "exp06" / "diagnostics" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    finalize_figure(fig, out.with_suffix(".pdf"))
    finalize_figure(fig, out.with_suffix(".png"))
    plt.close(fig)
    print(f"wrote {out.relative_to(repo)}.pdf + .png")
    print(f"square axes; uniform effective text {eff:.1f} pt; diagnostic only")


if __name__ == "__main__":
    main()
