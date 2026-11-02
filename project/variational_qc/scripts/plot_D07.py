"""exp05 T005/T022 出图（零机时）：8 链 / 10 环前十排名图 + 冠军环子链排名图，
合为竖排 3×1 单图 exp05_D07.pdf/png（(a)(b)(c) 标签置于各子图下方）。

版式规则（用户 2026-10-04 确认）：
- 图上不写具体比特编号，不写内部 D 编号；
- 芯片（Baihua/Shenglian）用 bar 纹理区分 + 图例，不写在刻度上；
- score 堆叠显示：0.8·S̄ 段 + 0.2·F_ro 段（总长 = score）；
- y 轴只标名次 Rank 1..10。
风格：scripts/figure_style.py，mathtext，矢量 PDF + 300dpi PNG → figs/exp05/。
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figure_style import apply_figure_style, font_pt_for, uniform_text, PRINT_TEXT_PT  # noqa: E402
from exp05_common import DATA_DIR  # noqa: E402

PALETTE = apply_figure_style()
FIGS = Path(__file__).resolve().parent.parent / "figs" / "exp05"
FIGS.mkdir(parents=True, exist_ok=True)

# 芯片 → bar 纹理（刻度上不写芯片名，见图例）。
CHIP_HATCH = {"Baihua": "", "Shenglian": "///"}


def stacked_rank_panel(ax, scores, stabs, fros, chips, title) -> None:
    n = len(scores)
    y = np.arange(n)
    comp_s = 0.8 * stabs
    comp_f = 0.2 * fros
    for i in range(n):
        h = CHIP_HATCH.get(str(chips[i]), "")
        ax.barh(i, comp_s[i], color="C1", edgecolor="black",
                hatch=h, linewidth=0.5)
        ax.barh(i, comp_f[i], left=comp_s[i], color="C2",
                edgecolor="black", hatch=h, linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels([f"Rank {i + 1}" for i in range(n)])
    ax.invert_yaxis()
    ax.set_xlabel("score")
    ax.set_title(title)
    legend = [Patch(facecolor="C1", edgecolor="black", label=r"$0.8\,\bar{S}$"),
              Patch(facecolor="C2", edgecolor="black",
                    label=r"$0.2\,F_{\rm ro}$")]
    # 芯片图例固定列出两家（即使某家未进前十，避免读者误以为漏画）。
    for chip in ("Baihua", "Shenglian"):
        legend.append(Patch(facecolor="0.85", edgecolor="black",
                            hatch=CHIP_HATCH.get(chip, ""), label=chip))
    ax.legend(handles=legend, fontsize=12, loc="center left",
              bbox_to_anchor=(1.0, 0.5))


def main() -> None:
    d07 = np.load(DATA_DIR / "exp05_D07a.npz", allow_pickle=True)
    i7 = np.argsort(-d07["score"])[:10]
    d08 = np.load(DATA_DIR / "exp05_D07b.npz", allow_pickle=True)
    i8 = np.argsort(-d08["score"])[:10]
    d09 = np.load(DATA_DIR / "exp05_D07c.npz", allow_pickle=True)
    i9 = np.argsort(-d09["score"])

    # Combined 3x1 (appendix FIG.7): equal-width panels, (a)(b)(c) below labels.
    fig, axs = plt.subplots(3, 1, figsize=(7.5, 8.3))
    panels = [(d07, i7, r"$8$-chain ranking top 10"),
              (d08, i8, r"$10$-ring ranking top 10"),
              (d09, i9, r"$8$-subchains in champion ring")]
    for ax, (d, idx, title) in zip(axs, panels):
        stacked_rank_panel(ax, d["score"][idx], d["stab_mean"][idx],
                           d["readout_fid"][idx], d["chip"][idx], title)
    for ax, letter in zip(axs, ("(a)", "(b)", "(c)")):
        ax.text(0.5, -0.30, letter, transform=ax.transAxes,
                fontsize=13, va="top", ha="center", clip_on=False)
    fig.tight_layout(h_pad=2.0)
    uniform_text(fig, font_pt_for(fig, PRINT_TEXT_PT))
    fig.savefig(FIGS / "exp05_D07.pdf")
    fig.savefig(FIGS / "exp05_D07.png", dpi=300)
    plt.close(fig)
    print("出图完成 figs/exp05/exp05_D07.pdf + .png")


if __name__ == "__main__":
    main()
