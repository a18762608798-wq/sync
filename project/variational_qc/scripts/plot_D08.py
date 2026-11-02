"""exp06 v3 联测出图（零机时）：两张独立 D08 图（δ × Q）。

每面板：S06 模拟机 p=1,2 的 Q 曲线（固定 hat 尺度组出）+ 真机 p=1 展示窗口
散点（共用端点归一化后逐点平均 + 单位间标准误，不做二次归一化）；
散点按 D09 获胜分段着色（triv 红 / topo 蓝 / Néel 黑，与初态色语言一致）。
只读 assemble 与 S06 出图，不生产数据；共用端点见 manifest，可复算。
风格：figure_style.py，mathtext，矢量 PDF + 300dpi PNG → figs/exp06/。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from figure_style import apply_figure_style  # noqa: E402
from exp06_common import (  # noqa: E402
    JOINT_LINE,
    line_dir,
    read_json,
)

PALETTE = apply_figure_style()
SIM_COLORS = ["#000000", "#7f7f7f"]  # p=1 black; p=2 gray
BAND_COLOR = {1: "#D62728", 2: "#0072B2", 3: "#000000"}
BAND_LABEL = {1: "triv", 2: "topo", 3: "Néel"}
LINE_OF_DELTA = {-2.0: ("dm2", 1, "D08a"), 0.85: ("d085", 2, "D08b")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None,
                    help="joint 目录覆盖（缺省 data/exp06/joint；synth 沙箱用）")
    ap.add_argument("--suffix", default="",
                    help="出图文件名后缀（synth 用 _synth）")
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent.parent
    figdir = repo / "figs" / "exp06"
    figdir.mkdir(parents=True, exist_ok=True)
    ldir = Path(args.root) if args.root else line_dir(JOINT_LINE, False)
    d = np.load(ldir / "exp06_D08_joint.npz")
    manifest = read_json(ldir / "exp06_manifest_joint.json")
    win = manifest["window"]
    d09 = np.load(repo / "data" / "exp04"
                  / "exp04_D09.npz")
    sg = np.asarray(d09["s_grid"])
    s15 = np.asarray(d["s_idx"])
    deltas = np.asarray(d["deltas"])
    ep = manifest["endpoints"]
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.1), sharey=True)
    for ax, (delta, (line, di, d08)), letter in zip(
            axes, LINE_OF_DELTA.items(), ("(a)", "(b)")):
        m = np.asarray([abs(float(x) - delta) < 1e-9 for x in deltas])
        assert int(m.sum()) == 15, (delta, int(m.sum()))
        # 模拟机 p=1,2 曲线（固定 hat 尺度，不归一化）。
        for p, color in zip((1, 2), SIM_COLORS):
            arr = np.asarray(d[f"q_sim_p{p}"])[m]
            ax.plot(s15[m] / 100.0, arr, "-",
                    color=color, linewidth=1.5, label=f"sim p={p}")
        # 真机窗口散点（共用端点归一化后均值 + 单位间标准误，不二次归一化）。
        y = np.asarray(d["win_mean"])[m]
        ye = np.asarray(d["win_se"])[m]
        band = np.asarray(d09["phase"][:, di - 1]).astype(int)
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
        ax.set_title(f"$\\delta={delta}$")
        ax.set_xlabel("s")
        ax.text(0.5, -0.30, letter, transform=ax.transAxes,
                fontsize=12, va="top", ha="center", clip_on=False)
    axes[0].set_ylabel("$Q$")
    seen = {}
    for _ax in axes:
        _h, _l = _ax.get_legend_handles_labels()
        for _hi, _li in zip(_h, _l):
            seen.setdefault(_li, _hi)
    fig.legend(list(seen.values()), list(seen.keys()), loc="lower center",
               bbox_to_anchor=(0.5, 0.01), ncol=5, fontsize=9,
               frameon=False)
    fig.subplots_adjust(bottom=0.34, wspace=0.12, top=0.90)
    fig.savefig(figdir / f"exp06_D08{args.suffix}.pdf")
    fig.savefig(figdir / f"exp06_D08{args.suffix}.png", dpi=300)
    plt.close(fig)
    print(f"wrote figs/exp06/exp06_D08{args.suffix}.pdf + .png "
          f"(N={win['N']} win=[{win['start']},{win['start'] + win['length']}) "
          f"d_raw={win['d_raw']:.4f} r={win['r']:.4f})")


if __name__ == "__main__":
    main()
