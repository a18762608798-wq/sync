#!/usr/bin/env python
"""VQE 五线对照图：解析 E0/E1 + 三初态 VQE 最优，只读 CSV 做渲染。

用法：
    python shared/viz/plot_vqe.py [--vqe-csv PATH] [--spectra-csv PATH]
        [--delta D] [--png PATH] [--no-pdf] [--title T]

输入缺失/表头不符时以非零退出码失败并打印可读错误，且不产生残缺图片
（先写临时文件再原子 rename，与 plot_heatmap.py 同约定）。
"""

import argparse
import os
import sys
import tempfile
from typing import NoReturn

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def fail(msg: str) -> NoReturn:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(2)


def atomic_save(fig: plt.Figure, path: str) -> None:
    d = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp_vqe_", suffix=os.path.splitext(path)[1], dir=d)
    os.close(fd)
    try:
        fig.savefig(tmp, dpi=150)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def main() -> None:
    ap = argparse.ArgumentParser(description="Plot VQE-vs-analytic 5-line comparison.")
    ap.add_argument("--vqe-csv", default="task3_vqe/data/interim/vqe_L8_OBC.csv")
    ap.add_argument("--spectra-csv", default="task1_baseline/data/interim/spectra_L8_OBC.csv")
    ap.add_argument("--delta", type=float, default=1.0)
    ap.add_argument("--png", default="task3_vqe/data/figures/vqe_comparison_deltap1.png")
    ap.add_argument("--no-pdf", action="store_true", help="skip same-name PDF output")
    ap.add_argument("--title", default="VQE vs analytic (L=8)")
    ap.add_argument("--mode", choices=("full", "min", "q", "zr"), default="full",
                    help="full: 5 lines (E0/E1 + 3 inits); min: 3 lines (E0/E1 + min(VQE)); "
                         "q: 2 lines (analytic Q + Q_vqe); zr: 2 lines (analytic tilde_ZR + ZR_vqe)")
    ap.add_argument("--q-vqe-csv", default="task3_vqe/data/interim/vqe_Q_L8_OBC.csv")
    ap.add_argument("--q-csv", default="task1_baseline/data/interim/Q_L8_OBC.csv")
    ap.add_argument("--zr-vqe-csv", default="task3_vqe/data/interim/vqe_ZR_L8_OBC.csv")
    ap.add_argument("--zr-csv", default="task1_baseline/data/interim/tilde_ZR_L8_OBC.csv")
    args = ap.parse_args()

    for p in (args.vqe_csv, args.spectra_csv):
        if not os.path.isfile(p):
            fail(f"input CSV not found: {p}")
    try:
        v = pd.read_csv(args.vqe_csv)
        a = pd.read_csv(args.spectra_csv)
    except Exception as e:  # noqa: BLE001
        fail(f"cannot parse CSV: {e}")
    for col in ("s", "delta", "E_triv", "E_topo", "E_afm"):
        if col not in v.columns:
            fail(f"{args.vqe_csv} missing column: {col}")
    for col in ("s", "delta", "E0", "E1"):
        if col not in a.columns:
            fail(f"{args.spectra_csv} missing column: {col}")

    if args.mode == "q":
        for p in (args.q_vqe_csv, args.q_csv):
            if not os.path.isfile(p):
                fail(f"input CSV not found: {p}")
        try:
            qv = pd.read_csv(args.q_vqe_csv)
            qa = pd.read_csv(args.q_csv)
        except Exception as e:  # noqa: BLE001
            fail(f"cannot parse CSV: {e}")
        for col in ("s", "delta", "Q_vqe"):
            if col not in qv.columns:
                fail(f"{args.q_vqe_csv} missing column: {col}")
        if "Q" not in qa.columns:
            fail(f"{args.q_csv} missing column: Q")
        vv = qv[abs(qv["delta"] - args.delta) < 1e-12].sort_values("s")
        aa = qa[abs(qa["delta"] - args.delta) < 1e-12].sort_values("s")
        if len(vv) == 0 or len(aa) == 0:
            fail(f"no rows for delta={args.delta}")
        fig, ax = plt.subplots(figsize=(8, 5.2), dpi=150)
        ax.plot(aa["s"], aa["Q"], label=r"$Q$ analytic", color="black")
        ax.plot(vv["s"], vv["Q_vqe"], label=r"$Q_{\mathrm{VQE}}$", marker="D",
                markersize=3, linestyle="-", color="C3")
        ax.set_xlabel("s")
        ax.set_ylabel("Q")
        ax.set_ylim(-1.1, 1.1)
        ax.set_title(args.title)
        ax.legend(loc="best")
        fig.tight_layout()
        atomic_save(fig, args.png)
        print(f"wrote {args.png}")
        if not args.no_pdf:
            pdf = os.path.splitext(args.png)[0] + ".pdf"
            atomic_save(fig, pdf)
            print(f"wrote {pdf}")
        return

    if args.mode == "zr":
        for p in (args.zr_vqe_csv, args.zr_csv):
            if not os.path.isfile(p):
                fail(f"input CSV not found: {p}")
        try:
            zv = pd.read_csv(args.zr_vqe_csv)
            za = pd.read_csv(args.zr_csv)
        except Exception as e:  # noqa: BLE001
            fail(f"cannot parse CSV: {e}")
        for col in ("s", "delta", "ZR_vqe"):
            if col not in zv.columns:
                fail(f"{args.zr_vqe_csv} missing column: {col}")
        if "tilde_ZR" not in za.columns:
            fail(f"{args.zr_csv} missing column: tilde_ZR")
        vv = zv[abs(zv["delta"] - args.delta) < 1e-12].sort_values("s")
        aa = za[abs(za["delta"] - args.delta) < 1e-12].sort_values("s")
        if len(vv) == 0 or len(aa) == 0:
            fail(f"no rows for delta={args.delta}")
        fig, ax = plt.subplots(figsize=(8, 5.2), dpi=150)
        ax.plot(aa["s"], aa["tilde_ZR"], label=r"$\tilde{Z}_\mathcal{R}$ analytic", color="black")
        ax.plot(vv["s"], vv["ZR_vqe"], label=r"$\tilde{Z}_{\mathcal{R},\mathrm{VQE}}$", marker="D",
                markersize=3, linestyle="-", color="C3")
        ax.set_xlabel("s")
        ax.set_ylabel(r"$\tilde{Z}_\mathcal{R}$")
        ax.set_ylim(-1.2, 1.2)
        ax.set_title(args.title)
        ax.legend(loc="best")
        fig.tight_layout()
        atomic_save(fig, args.png)
        print(f"wrote {args.png}")
        if not args.no_pdf:
            pdf = os.path.splitext(args.png)[0] + ".pdf"
            atomic_save(fig, pdf)
            print(f"wrote {pdf}")
        return

    vv = v[abs(v["delta"] - args.delta) < 1e-12].sort_values("s")
    aa = a[abs(a["delta"] - args.delta) < 1e-12].sort_values("s")
    if len(vv) == 0 or len(aa) == 0:
        fail(f"no rows for delta={args.delta}")

    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=150)
    ax.plot(aa["s"], aa["E0"], label=r"$E_0$ analytic", color="black")
    ax.plot(aa["s"], aa["E1"], label=r"$E_1$ analytic", color="gray", linestyle="--")
    if args.mode == "min":
        vmin = vv[["E_triv", "E_topo", "E_afm"]].min(axis=1)
        ax.plot(vv["s"], vmin, label="min(VQE)", marker="D", markersize=3, linestyle="-", color="C3")
    else:
        ax.plot(vv["s"], vv["E_triv"], label="VQE triv", marker="o", markersize=3, linestyle="-", color="C0")
        ax.plot(vv["s"], vv["E_topo"], label="VQE topo", marker="s", markersize=3, linestyle="-", color="C1")
        ax.plot(vv["s"], vv["E_afm"], label="VQE afm", marker="^", markersize=3, linestyle="-", color="C2")
    ax.set_xlabel("s")
    ax.set_ylabel("energy")
    ax.set_title(args.title)
    ax.legend(loc="best")
    fig.tight_layout()

    atomic_save(fig, args.png)
    print(f"wrote {args.png}")
    if not args.no_pdf:
        pdf = os.path.splitext(args.png)[0] + ".pdf"
        atomic_save(fig, pdf)
        print(f"wrote {pdf}")


if __name__ == "__main__":
    main()
