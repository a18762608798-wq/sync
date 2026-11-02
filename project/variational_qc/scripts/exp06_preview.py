"""exp06 v3 联测离线预览（零机时）：S03 点位映射 → 30 点联合单位 → 打印账单。

两线同窗口 30 点（15 个 s × δ∈{0.85,−2}，每 s 先 0.85 后 −2）× 只 p=1；
测量单位 = 30 点 + 2 标定（32 电路）。
产物：data/exp06/joint/groups.json + rounds/r001/bill.json
（confirmed=false；人工确认后才可 submit）。
S04 冠军链 top1 + D07c Rank1 子链由 S04/D07c 落盘值读取，不再硬编码。
v2 分线 preview 已归档，不再使用。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp06_common import (  # noqa: E402
    JOINT_LINE,
    JOINT_N_POINTS,
    JOINT_UNIT_CIRCUITS,
    SHOTS,
    SPARSE,
    V3_ROUND_UNITS,
    line_dir,
    root_of,
    write_json,
)


def load_qubits(chain_arg: str | None,
                sub_arg: str | None) -> tuple[list[int], list[int], str]:
    if chain_arg and sub_arg:
        chain = [int(v) for v in chain_arg.split(",")]
        sub = [int(v) for v in sub_arg.split(",")]
        assert len(chain) == 8 and len(sub) == 8
        return chain, sub, "override"
    s04 = np.load(root_of(False).parent / "exp05" / "exp05_S04.npz")
    chain = [int(v) for v in np.asarray(s04["champion_chain"][0])]
    chip = str(np.asarray(s04["champion_chain_chip"][0]))
    d07c = np.load(root_of(False).parent / "exp05" / "exp05_D07c.npz")
    sub = [int(v) for v in np.asarray(d07c["subchain"]).reshape(-1, 8)[0]]
    assert len(chain) == 8 and len(sub) == 8
    return chain, sub, chip


def build_joint_groups(chain_arg: str | None = None,
                       sub_arg: str | None = None
                       ) -> tuple[list[dict], list[int], list[int], str]:
    """30 点联合组：每 s 先 δ=0.85 后 δ=−2；返回 (groups, chain, sub, chip)。"""
    s03 = np.load(root_of(False).parent / "exp04" / "exp04_S03.npz")
    meta = s03["meta"]
    s_grid = s03["s_grid"]
    deltas = s03["deltas"]
    th_by_key = {}
    for r in range(len(meta)):
        ddi, si, p, a = (int(v) for v in meta[r])
        if p == 1:
            th_by_key[(ddi, int(si))] = a
    groups = []
    for si in SPARSE:
        for di in (2, 1):  # 每个 s 先 δ=0.85 后 δ=−2（spec Q12）
            key = (di, int(si))
            assert key in th_by_key, f"S03 缺点 {(di, si, 1)} 判 invalid"
            groups.append({"delta_idx": di, "s_idx": int(si), "p": 1,
                           "a_star": int(th_by_key[key]),
                           "s": float(s_grid[int(si) - 1]),
                           "delta": float(deltas[di - 1])})
    assert len(groups) == JOINT_N_POINTS, len(groups)
    chain, sub, chip = load_qubits(chain_arg, sub_arg)
    return groups, chain, sub, chip


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", type=int, default=V3_ROUND_UNITS)
    ap.add_argument("--chain", type=str, default=None,
                    help="8 比特链覆盖（逗号分隔）")
    ap.add_argument("--sub", type=str, default=None,
                    help="8 比特 topo 子链覆盖（逗号分隔）")
    args = ap.parse_args()
    n_units = args.units
    assert n_units >= 1

    groups, chain, sub, chip = build_joint_groups(args.chain, args.sub)
    ldir = line_dir(JOINT_LINE, False)
    write_json(ldir / "groups.json",
               {"line": JOINT_LINE, "groups": groups,
                "chain_top1": chain, "subchain_top1": sub, "chip": chip,
                "s03_ref": "data/exp04/exp04_S03.npz",
                "s04_ref": "data/exp05/exp05_S04.npz"})
    rdir = ldir / "rounds"
    rdir.mkdir(parents=True, exist_ok=True)
    n_vqe = n_units * JOINT_N_POINTS
    n_cal = n_units * 2
    total = n_units * JOINT_UNIT_CIRCUITS
    bill = {"line": JOINT_LINE, "round": 1, "unit_start": 0,
            "n_units": n_units, "vqe_tasks": n_vqe, "calib_tasks": n_cal,
            "total_tasks": total, "shots_per_task": SHOTS,
            "total_shots": total * SHOTS, "chip": chip,
            "s03_ref": "data/exp04/exp04_S03.npz",
            "s04_ref": "data/exp05/exp05_S04.npz",
            "confirmed": False,
            "note": "v3 联测单轮 500；人工确认后置 confirmed=true 才可 submit"}
    write_json(rdir / "r001" / "bill.json", bill)
    n_triv = sum(1 for g in groups if g["a_star"] in (1, 3))
    n_topo = sum(1 for g in groups if g["a_star"] == 2)
    print(f"组：30（开链 {n_triv} / 环 {n_topo}）× p=1；{n_units} 单位")
    print("---- 账单 ----")
    print(f"VQE：{n_vqe} 任务 × {SHOTS} shots")
    print(f"标定：{n_cal} 任务 × {SHOTS} shots")
    print(f"合计：{total} 任务，{total * SHOTS} shots")
    print(f"链 top1：{chain}；环内最优 8 子链：{sub}（{bill['chip']}）")
    print(f"账单已落盘 {rdir / 'r001'}/bill.json"
          f"（confirmed={bill['confirmed']}）")


if __name__ == "__main__":
    main()
