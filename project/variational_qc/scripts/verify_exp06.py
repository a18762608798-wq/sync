"""exp06 v3 联测生产断言（零机时）：对正式输出全量执行，逐条映射 spec VAL-001..VAL-008。

任一硬门失败即非零退出并指明单位；诊断只记录。
用法：python scripts/verify_exp06.py（固定 joint，无参数）。
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
    SHOTS,
    line_dir,
    read_json,
)
from exp06_submit import allowed_edges  # noqa: E402

FAIL: list[str] = []


def hard(cond: bool, msg: str) -> None:
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    if not cond:
        FAIL.append(msg)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None,
                    help="joint 目录覆盖（缺省 data/exp06/joint；synth 沙箱用）")
    args = ap.parse_args()
    repo = Path(__file__).resolve().parent.parent
    ldir = Path(args.root) if args.root else line_dir(JOINT_LINE, False)

    manifest = read_json(ldir / "exp06_manifest_joint.json")
    hard(manifest.get("schema") == "exp06/v3", "manifest schema exp06/v3")
    ep = manifest.get("endpoints", {})
    hard(ep.get("S_max", 0) > 0 and ep.get("O_max", 0) > 0
         and ep.get("method") == "top1-max-pooled-window",
         "manifest 窗口内共用端点为正且方法一致")
    hard(manifest.get("report", {}).get("mode") == "report-only",
         "manifest report-only 声明")
    rdir = ldir / "rounds" / "r001" / "bill.json"
    hard(read_json(rdir).get("confirmed", False), "r001 账单已人工确认")

    d08 = np.load(ldir / "exp06_D08_joint.npz", allow_pickle=True)
    G = len(d08["s_idx"])
    hard(G == JOINT_N_POINTS, f"D08 真机图层点数 {G} == 30")
    from collections import Counter
    hard(Counter(int(v) for v in d08["s_idx"])
         == Counter(list(range(1, 100, 7)) * 2), "点位：15 s × 2δ")
    U = int(manifest.get("n_units", -1))
    hard(d08["q_post"].shape == (U, G),
         f"全量单位矩阵 {d08['q_post'].shape} == ({U}, 30)")
    hard(manifest.get("d08") == "D08a+b", "d08 标识一致")

    # VAL-001/005：θ 与 S03 p=1 逐元一致；30 点齐全。
    s03 = np.load(repo / "data" / "exp04" / "exp04_S03.npz")
    meta, th = s03["meta"], s03["theta"]
    th_map = {}
    for r in range(len(meta)):
        di, si, p, a = (int(v) for v in meta[r])
        if p == 1:
            th_map[(di, si)] = th[r]
    info = read_json(ldir / "groups.json")
    groups = info["groups"]
    ok_th = True
    if d08["theta"].shape[0] != G:
        ok_th = False
        print("  θ 存档行数与点数不一致", flush=True)
    else:
        for i in range(G):
            g = groups[i]
            ref = th_map.get((g["delta_idx"], int(d08["s_idx"][i])))
            if ref is None or not np.allclose(
                    d08["theta"][i][:len(ref)], ref, equal_nan=True):
                ok_th = False
                print(f"  θ 不一致 g{i}", flush=True)
    hard(ok_th, "θ 与 S03 p=1 同点逐元一致")

    # 三件套 + S05 同单位 + correct + 转译验路（VAL-001/002/005/008）。
    from exp06_assemble import (  # noqa: E402
        MANIFEST_KEYS,
        READOUT_MITIGATION,
        calibration_mapping_record,
        group_Ms,
        mitigate_counts,
        obs_from_probs,
        q_hat_basis,
        search_best_even_window,
        unit_q_se_qb,
    )
    phys_of = {1: info["chain_top1"], 3: info["chain_top1"],
               2: info["subchain_top1"]}
    hard(manifest.get("readout_mitigation") == READOUT_MITIGATION,
         "manifest 欧氏概率投影、归一化及逻辑位序记录一致")
    mapping = calibration_mapping_record(groups, phys_of, "a_star")
    hard(manifest.get("calibration_mapping") == mapping,
         "manifest 如实记录标定物理映射覆盖范围")
    qb = q_hat_basis(float(ep["S_max"]), float(ep["O_max"]))
    uids = [int(v) for v in d08["unit_ids"]]
    three_ok, se_ok, s05_ok, route_ok, acct_ok = True, True, True, True, True
    mapping_ok = True
    for k, uid in enumerate(uids):
        st = read_json(ldir / "units" / f"{uid:05d}" / "state.json")
        for key in ("cal_zero", "cal_one"):
            if st["submit_params"].get(key, {}).get("target_qubits") != mapping["calibration_target_qubits"]:
                mapping_ok = False
        if any(f"g{gi}" not in st.get("counts", {}) for gi in range(G)):
            three_ok = False
        if any(x not in st.get("counts", {})
               for x in ("cal_zero", "cal_one")):
            three_ok = False
        Ms = group_Ms({x: st["counts"][x]
                      for x in ("cal_zero", "cal_one")},
                      phys_of[groups[0]["a_star"]])
        if np.array(Ms).shape != d08["s05"][k].shape or not np.allclose(
                np.array(Ms), d08["s05"][k]):
            s05_ok = False
        for gi, g in enumerate(groups):
            counts = st["counts"][f"g{gi}"]
            if not counts or sum(counts.values()) == 0:
                three_ok = False
                continue
            p_raw = np.zeros(256)
            for kk, c in counts.items():
                p_raw[int(kk, 2)] += c
            p_raw = p_raw / p_raw.sum()
            s0, o0 = obs_from_probs(p_raw)
            if not (np.isclose(s0, d08["s_pre"][k, gi])
                    and np.isclose(o0, d08["o_pre"][k, gi])):
                three_ok = False
            p_mit = mitigate_counts(counts, Ms)
            s1, o1 = obs_from_probs(p_mit)
            if not (np.all(p_mit >= 0) and np.isclose(p_mit.sum(), 1)
                    and np.isclose(s1, d08["s_post"][k, gi])
                    and np.isclose(o1, d08["o_post"][k, gi])):
                three_ok = False
            if not (np.isclose(float(p_mit @ qb), d08["q_post"][k, gi],
                               rtol=1e-9, atol=1e-12)
                    and np.isclose(unit_q_se_qb(p_mit, qb, SHOTS),
                                   d08["q_se_unit"][k, gi], rtol=1e-9,
                                   atol=1e-12)):
                se_ok = False
            sp = st["submit_params"].get(f"g{gi}", {})
            if sp.get("target_qubits") != phys_of[g["a_star"]]:
                mapping_ok = False
            if sp.get("correct") is not False:
                acct_ok = False
            tr = st["transpile"].get(f"g{gi}", {})
            if not tr.get("in_allowed", False):
                route_ok = False
                print(f"  转译验路失败 unit {uid} g{gi}", flush=True)
            edges = {tuple(e) for e in tr.get("cz_edges", [])}
            if not edges <= allowed_edges(int(d08["a_star"][gi])):
                route_ok = False
                print(f"  边集越界 unit {uid} g{gi}", flush=True)
    hard(three_ok, "三件套：原始 counts + 缓解前 + 缓解后全存档")
    hard(se_ok, "单位内组合 Q 与传播 SE 重算一致")
    hard(s05_ok, "S05 与 VQE 同单位")
    hard(mapping_ok, "实际提交的测量与标定物理映射符合披露记录")
    hard(acct_ok, "提交参数 correct=False 留存可查")
    hard(route_ok, "转译验路断言：CZ 边集落入允许集")

    # VAL-004/006：窗口内端点 + 窗口复算 + 披露（Q14）。
    s06 = np.load(repo / "data" / "exp04" / "exp04_S06.npz")
    tag_of = {1: "dm2", 2: "d085"}
    s_rows = np.array([int(v) - 1 for v in d08["s_idx"]])
    tags = [tag_of[g["delta_idx"]] for g in groups]
    s_sim_hat = np.array([s06[f"{tags[i]}_spi"][s_rows[i], 0] / 8.0
                          for i in range(G)])
    o_sim_hat = np.array([-s06[f"{tags[i]}_ostr"][s_rows[i], 0]
                          for i in range(G)])
    win = search_best_even_window(np.asarray(d08["s_post"]),
                                  np.asarray(d08["o_post"]),
                                  s_sim_hat, o_sim_hat)
    mw = manifest.get("window", {})
    win_ok = (int(win["start"]) == int(mw.get("start", -1))
              and int(win["length"]) == int(mw.get("length", -2))
              and np.isclose(win["d_raw"], mw.get("d_raw", float("nan")))
              and np.isclose(win["r"], mw.get("r", float("nan")))
              and np.isclose(win["S_max"], mw.get("S_max", float("nan")))
              and np.isclose(win["O_max"], mw.get("O_max", float("nan"))))
    hard(win_ok, "展示窗口复算一致（起止/偶数长度/d_raw/r/窗口端点）")
    hard(int(mw.get("length", 0)) % 2 == 0
         and int(mw.get("length", 0)) >= 10
         and int(mw.get("N", -1)) == U, "窗口偶数长度≥10，N 一致")
    hard(all(k in mw for k in ("start", "length", "N", "d_raw", "r",
                              "S_max", "O_max")),
         "披露字段齐全（起止/长度/N/d_raw/r/端点）")
    hard(not (set(MANIFEST_KEYS) - set(manifest)), "manifest 必填字段齐全")

    # 对账：无 invalid 残留。
    import glob as _glob
    inv = _glob.glob(str(ldir / "units" / "*" / "invalid.json"))
    hard(not inv, "无 invalid 残留标记")

    # 诊断（只记录）。
    print(f"诊断：N={U}，窗口 start={win['start']} len={win['length']} "
          f"d_raw={win['d_raw']:.4f} r={win['r']:.4f}（report-only）")
    print("诊断：D08 真机–模拟机趋势一致性请目检出图")
    if mapping["mismatched_keys"]:
        print(f"诊断：每单位 {len(mapping['mismatched_keys'])} 个测点缺少匹配物理映射的标定；"
              "当前数值核验不证明跨映射标定外推有效", flush=True)

    if FAIL:
        print(f"VERIFY-EXP06-FAIL：{len(FAIL)} 项", flush=True)
        raise SystemExit(1)
    print("VERIFY-EXP06-OK", flush=True)


if __name__ == "__main__":
    main()
