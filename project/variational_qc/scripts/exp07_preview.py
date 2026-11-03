"""exp07 离线预览（零机时）：S06 p=2 分支参数 → 90 点联合单位 → 打印账单。

每个 s 先 δ=0.85 后 δ=-2（时间交错共漂移），每个 (s,δ) 内按 triv→topo→AFM 顺序；
三分支各取各自 p=2 最优参数（a* 获胜标签仅记录）。分支有效性过滤：
S06 同点同分支 p=2 conv 与 stagn 皆假标 invalid（不进账单计数，单独列出）。
产物：data/exp07/joint/groups.json + rounds/r001/bill.json
（confirmed=false；人工确认后才可 submit）。
S04 冠军链 top1 + D07c Rank1 子链由 S04/D07c 落盘值读取，不再硬编码。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp07_circuits import (  # noqa: E402
    P,
    SPARSE,
    TAG_OF_DI,
    branch_invalid,
)
from exp07_common import (  # noqa: E402
    BRANCHES,
    LINE,
    N_POINTS,
    ROUND_UNITS,
    S04_REF,
    S06_REF,
    SHOTS,
    UNIT_CIRCUITS,
    line_dir,
    write_json,
)

S06_PATH = Path(__file__).resolve().parent.parent / S06_REF


def load_qubits(chain_arg: str | None,
                sub_arg: str | None) -> tuple[list[int], list[int], str]:
    if chain_arg and sub_arg:
        chain = [int(v) for v in chain_arg.split(",")]
        sub = [int(v) for v in sub_arg.split(",")]
        assert len(chain) == 8 and len(sub) == 8
        return chain, sub, "override"
    s04 = np.load(Path(__file__).resolve().parent.parent / S04_REF)
    chain = [int(v) for v in np.asarray(s04["champion_chain"][0])]
    chip = str(np.asarray(s04["champion_chain_chip"][0]))
    d07c = np.load(Path(__file__).resolve().parent.parent
                   / "data/exp05/exp05_D07c.npz")
    sub = [int(v) for v in np.asarray(d07c["subchain"]).reshape(-1, 8)[0]]
    assert len(chain) == 8 and len(sub) == 8
    return chain, sub, chip


def build_joint_groups(chain_arg: str | None = None,
                       sub_arg: str | None = None
                       ) -> tuple[list[dict], list[dict], list[int], list[int], str]:
    """90 点联合组 + invalid 清单。返回 (groups, invalid, chain, sub, chip)。"""
    s06 = np.load(S06_PATH)
    s_grid = np.asarray(s06["s_grid"])
    deltas = np.asarray(s06["deltas"])
    assert abs(float(deltas[0]) + 2.0) < 1e-12 and abs(float(deltas[1]) - 0.85) < 1e-12
    groups, invalid = [], []
    for si in SPARSE:
        for di in (2, 1):  # 每个 s 先 δ=0.85 后 δ=-2（spec PRE-006）
            for a in BRANCHES:
                rec = {"delta_idx": di, "s_idx": int(si), "p": P,
                       "branch": int(a),
                       "s": float(s_grid[int(si) - 1]),
                       "delta": float(deltas[di - 1])}
                if branch_invalid(S06_PATH, di, int(si), int(a)):
                    rec["invalid_reason"] = "unconverged"
                    invalid.append(rec)
                else:
                    groups.append(rec)
    assert len(groups) + len(invalid) == N_POINTS, (len(groups), len(invalid))
    chain, sub, chip = load_qubits(chain_arg, sub_arg)
    return groups, invalid, chain, sub, chip


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", type=int, default=ROUND_UNITS)
    ap.add_argument("--chain", type=str, default=None,
                    help="8 比特链覆盖（逗号分隔）")
    ap.add_argument("--sub", type=str, default=None,
                    help="8 比特 topo 子链覆盖（逗号分隔）")
    args = ap.parse_args()
    n_units = args.units
    assert n_units >= 1

    groups, invalid, chain, sub, chip = build_joint_groups(args.chain, args.sub)
    ldir = line_dir()
    write_json(ldir / "groups.json",
               {"line": LINE, "groups": groups, "invalid": invalid,
                "chain_top1": chain, "subchain_top1": sub, "chip": chip,
                "s06_ref": S06_REF, "s04_ref": S04_REF})
    rdir = ldir / "rounds"
    rdir.mkdir(parents=True, exist_ok=True)
    n_vqe = n_units * len(groups)
    n_cal = n_units * 2
    total = n_units * (len(groups) + 2)
    bill = {"line": LINE, "round": 1, "unit_start": 0,
            "n_units": n_units, "vqe_tasks": n_vqe, "calib_tasks": n_cal,
            "total_tasks": total, "shots_per_task": SHOTS,
            "total_shots": total * SHOTS, "chip": chip,
            "s06_ref": S06_REF, "s04_ref": S04_REF,
            "n_invalid_points": len(invalid),
            "confirmed": False,
            "note": "exp07 单轮 500；人工确认后置 confirmed=true 才可 submit"}
    write_json(rdir / "r001" / "bill.json", bill)
    print(f"组：{len(groups)} 有效 + {len(invalid)} invalid（90 点三分支）× p=2；{n_units} 单位")
    print("---- 账单 ----")
    print(f"VQE：{n_vqe} 任务 × {SHOTS} shots")
    print(f"标定：{n_cal} 任务 × {SHOTS} shots")
    print(f"合计：{total} 任务，{total * SHOTS} shots")
    print(f"链 top1：{chain}；环内最优 8 子链：{sub}（{bill['chip']}）")
    if invalid:
        print(f"invalid 点：{len(invalid)}（详见 groups.json，无账单）")
    print(f"账单已落盘 {rdir / 'r001'}/bill.json"
          f"（confirmed={bill['confirmed']}）")


if __name__ == "__main__":
    main()
