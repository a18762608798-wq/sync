"""exp07 组装（零机时）：joint units → S05 缓解 → hat 组装 →
窗口内 90 点共用端点冻结 → 分支 Q 组合 → mean(r_a) 最优偶数窗口搜索 →
D10 + manifest。

纯函数（mitigate/obs/端点/窗口/manifest）可被 test_exp07_local.py 直接
import（零真机调用）；Q 定义与缓解数学只读复刻 exp06_assemble（同 Exp02）。
qiskit counts 键约定：左起最高位 = qubit L-1（大端字符串）。

分支窗口规则（spec POST-002）：候选窗口为 500 单位序列的连续子段，偶数长度；
端点为候选窗口内 90 点 pooled 逐点均值的 top-1 最大（S_max、O_max，随窗口记）；
每分支在其 30 点（15 s × 2δ）上算 r_a/d_raw,a（相对 S06 p=2 获胜分支灰线，
同 (δ,s) 取值）；最优窗口取 mean(r_a) 最大，并列取 pooled d_raw（=mean(d_a)）
最小，再并列更长，再并列更早；report-only。
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp06_assemble import (  # noqa: E402
    L,
    READOUT_MITIGATION,
    calibration_mapping_record,
    build_manifest as _build_manifest,
    combine_Q,
    d_raw_r,
    group_Ms,
    mitigate_counts,
    obs_basis_arrays,
    obs_from_probs,
    q_hat_basis,
    unit_q_se_qb,
)
from exp07_circuits import (  # noqa: E402
    P,
    TAG_OF_DI,
    branch_theta,
)
from exp07_common import (  # noqa: E402
    BRANCHES,
    N_POINTS,
    ROUND_UNITS,
    S04_REF,
    S06_REF,
    SHOTS,
    line_dir,
    read_json,
    unit_state_path,
    write_json,
)

SCHEMA = "exp07/v2"

MANIFEST_KEYS = {"schema", "line", "d10", "s06_ref", "s04_ref", "provenance",
                 "points", "shots", "p_level", "chip", "n_units",
                 "endpoints", "window", "branch_stats", "report", "stderr_def",
                 "toolchain", "python", "readout_mitigation", "calibration_mapping"}

O_SPI, O_OSTR = obs_basis_arrays()

S06_PATH = Path(__file__).resolve().parent.parent / S06_REF


def pair_sim_q() -> tuple[np.ndarray, list[dict]]:
    """30 个 (δ,s) 对的 S06 p=2 获胜分支 Q 灰线 + 点位表。

    返回 (q_sim[30], pairs)：pairs[i] = {delta_idx, s_idx, s, delta}，
    顺序与 groups 一致（每 s 先 δ=0.85 后 δ=-2）。
    """
    from exp07_preview import SPARSE as _SP  # 延迟导入防循环
    s06 = np.load(S06_PATH)
    s_grid = np.asarray(s06["s_grid"])
    deltas = np.asarray(s06["deltas"])
    q_sim, pairs = [], []
    for si in _SP:
        for di in (2, 1):
            tag = TAG_OF_DI[di]
            spi = float(np.asarray(s06[f"{tag}_spi"])[si - 1, P - 1])
            ostr = float(np.asarray(s06[f"{tag}_ostr"])[si - 1, P - 1])
            q = 4.0 / 3.0 + 2.0 * ostr - spi / 6.0
            q_sim.append(q)
            pairs.append({"delta_idx": di, "s_idx": int(si),
                          "s": float(s_grid[int(si) - 1]),
                          "delta": float(deltas[di - 1])})
    return np.array(q_sim), pairs


def branch_point_index(groups: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """每点分支与 (δ,s) 对序号：返回 (branch_idx[90], pair_idx[90])。"""
    pair_of = {}
    for gi, g in enumerate(groups):
        key = (g["delta_idx"], g["s_idx"])
        pair_of.setdefault(key, len(pair_of))
    return (np.array([g["branch"] for g in groups]),
            np.array([pair_of[(g["delta_idx"], g["s_idx"])] for g in groups]))


def branch_window_stats(q_hw: np.ndarray, q_sim30: np.ndarray,
                        branch_idx: np.ndarray, pair_idx: np.ndarray
                        ) -> tuple[dict, dict, dict]:
    """分支统计：每分支在其 30 点上相对灰线算 r_a/d_raw,a。

    q_hw[90] 为窗口 pooled 均值经共用端点组合后的 Q；q_sim30[30] 为灰线。
    返回 (r_a, d_a, pooled)。
    """
    r_a, d_a = {}, {}
    for a in sorted(set(int(v) for v in branch_idx)):
        m = branch_idx == a
        pairs = pair_idx[m]
        assert len(np.unique(pairs)) == 30, (a, len(np.unique(pairs)))
        d, r = d_raw_r(np.asarray(q_hw)[m], np.asarray(q_sim30)[pairs])
        r_a[str(a)] = float(r)
        d_a[str(a)] = float(d)
    mean_r = float(np.mean([r_a[k] for k in sorted(r_a)]))
    pooled_d = float(np.mean([d_a[k] for k in sorted(d_a)]))
    return r_a, d_a, {"mean_r": mean_r, "pooled_d_raw": pooled_d}


def window_endpoints90(s_mean: np.ndarray, o_mean: np.ndarray) -> dict:
    """窗口内 90 点共用端点：pooled 逐点均值的 top-1 最大值。"""
    S_max = float(np.max(np.asarray(s_mean, dtype=float)))
    O_max = float(np.max(-np.asarray(o_mean, dtype=float)))
    if not O_max > 0:
        O_max = 1e-12
    return {"S_max": S_max, "O_max": O_max,
            "method": "top1-max-pooled-window-90"}


def search_best_branch_window(S_units: np.ndarray, O_units: np.ndarray,
                              q_sim30: np.ndarray, branch_idx: np.ndarray,
                              pair_idx: np.ndarray,
                              min_len: int = 10) -> dict:
    """mean(r_a) 最优偶数窗口（并列 pooled d_raw 最小 → 更长 → 更早）。"""
    S_units = np.asarray(S_units, dtype=float)
    O_units = np.asarray(O_units, dtype=float)
    U, npt = S_units.shape
    assert O_units.shape == (U, npt) and npt == N_POINTS
    assert U >= min_len
    csum_s = np.vstack([np.zeros((1, npt)), np.cumsum(S_units, axis=0)])
    csum_o = np.vstack([np.zeros((1, npt)), np.cumsum(O_units, axis=0)])
    best = {"start": 0, "length": min_len if min_len % 2 == 0 else min_len + 1,
            "N": U, "mean_r": float("-inf"), "pooled_d_raw": float("inf"),
            "S_max": float("nan"), "O_max": float("nan"),
            "r_a": {}, "d_raw_a": {}}
    max_len = U if U % 2 == 0 else U - 1
    first = min_len if min_len % 2 == 0 else min_len + 1
    for len_ in range(first, max_len + 1, 2):
        sm = (csum_s[len_:] - csum_s[:U - len_ + 1]) / len_
        om = (csum_o[len_:] - csum_o[:U - len_ + 1]) / len_
        for i in range(sm.shape[0]):
            ep = window_endpoints90(sm[i], om[i])
            qh, _ = combine_Q(sm[i], om[i], ep["S_max"], ep["O_max"],
                              np.zeros(npt), np.zeros(npt))
            r_a, d_a, pooled = branch_window_stats(
                qh, q_sim30, branch_idx, pair_idx)
            if (pooled["mean_r"] > best["mean_r"] + 1e-12
                    or (abs(pooled["mean_r"] - best["mean_r"]) <= 1e-12
                        and (pooled["pooled_d_raw"] < best["pooled_d_raw"] - 1e-12
                             or (abs(pooled["pooled_d_raw"]
                                     - best["pooled_d_raw"]) <= 1e-12
                                 and (len_ > best["length"]
                                      or (len_ == best["length"]
                                          and i < best["start"])))))):
                best = {"start": int(i), "length": int(len_), "N": U,
                        "mean_r": pooled["mean_r"],
                        "pooled_d_raw": pooled["pooled_d_raw"],
                        "S_max": ep["S_max"], "O_max": ep["O_max"],
                        "r_a": r_a, "d_raw_a": d_a}
    best["pass"] = None
    return best


def build_manifest(**kw) -> dict:
    m = {"schema": SCHEMA}
    m.update(kw)
    missing = MANIFEST_KEYS - set(m)
    if missing:
        raise ValueError(f"manifest 缺字段 {missing}")
    return m


def main() -> None:
    import argparse as _ap
    ap = _ap.ArgumentParser()
    ap.add_argument("--root", default=None,
                    help="joint 目录覆盖（缺省 data/exp07/joint）")
    a = ap.parse_args()
    from pathlib import Path as _P
    ldir = _P(a.root) if a.root else line_dir()
    repo = _P(__file__).resolve().parent.parent
    info = read_json(ldir / "groups.json")
    from exp07_common import validate_batch
    from optimization_source import require_same_provenance
    provenance = validate_batch(info)
    groups = info["groups"]
    G = len(groups)
    assert G == N_POINTS, G
    phys_of = {1: info["chain_top1"], 3: info["chain_top1"],
               2: info["subchain_top1"]}
    branch_idx, pair_idx = branch_point_index(groups)
    q_sim30, pairs = pair_sim_q()
    assert len(pairs) == 30 and len(q_sim30) == 30

    from exp07_submit import build_theta_map  # 延迟导入（提交脚本已就绪）
    theta_map = build_theta_map(groups)
    theta_rows = [theta_map[(g["delta_idx"], g["s_idx"], g["branch"])]
                  for g in groups]
    theta_arr = np.array(theta_rows)

    unit_dirs = sorted((ldir / "units").glob("[0-9]" * 5)) \
        if (ldir / "units").is_dir() else []
    s05_all, s_post, o_post, s_pre, o_pre, pmit_all, uids = \
        [], [], [], [], [], [], []
    for udir in unit_dirs:
        st = read_json(udir / "state.json")
        require_same_provenance(st.get("provenance"), provenance, str(udir))
        if any(f"g{gi}" not in st.get("counts", {}) for gi in range(G)):
            continue
        if any(x not in st.get("counts", {})
               for x in ("cal_zero", "cal_one")):
            continue
        Ms = group_Ms({k: st["counts"][k]
                      for k in ("cal_zero", "cal_one")},
                      phys_of[groups[0]["branch"]])
        s05_all.append(Ms)
        rs_post, ro_post, rs_pre, ro_pre, rp = [], [], [], [], []
        for gi in range(G):
            counts = st["counts"][f"g{gi}"]
            p_raw = np.zeros(1 << L)
            for key, c in counts.items():
                p_raw[int(key, 2)] += c
            s = p_raw.sum()
            p_raw = p_raw / s if s > 0 else p_raw
            spi0, ostr0 = obs_from_probs(p_raw)
            p_mit = mitigate_counts(counts, Ms)
            rs_pre.append(spi0)
            ro_pre.append(ostr0)
            rs_post.append(float(p_mit @ O_SPI))
            ro_post.append(float(p_mit @ O_OSTR))
            rp.append(p_mit)
        s_post.append(rs_post)
        o_post.append(ro_post)
        s_pre.append(rs_pre)
        o_pre.append(ro_pre)
        pmit_all.append(rp)
        uids.append(int(udir.name))
    U = len(uids)
    assert U == ROUND_UNITS, f"完整单位不足：{U}/{ROUND_UNITS}"
    s_post = np.array(s_post).reshape(-1, G)
    o_post = np.array(o_post).reshape(-1, G)
    s05_arr = np.array(s05_all).reshape(-1, L, 2, 2)

    win = search_best_branch_window(s_post, o_post, q_sim30,
                                    branch_idx, pair_idx)
    ws, wl = int(win["start"]), int(win["length"])
    S_max, O_max = win["S_max"], win["O_max"]
    print(f"最优窗口端点：S_max={S_max:.4f} O_max={O_max:.4f}"
          "（top1-max-pooled-window-90）")

    qb = q_hat_basis(S_max, O_max)
    q_post = np.array([[float(p @ qb) for p in rp] for rp in pmit_all])
    q_se = np.array([[unit_q_se_qb(p, qb, SHOTS) for p in rp]
                     for rp in pmit_all])
    wmean = q_post[ws:ws + wl].mean(axis=0)
    wse = q_post[ws:ws + wl].std(axis=0, ddof=1) / math.sqrt(wl) \
        if wl > 1 else np.full(G, np.nan)

    np.savez(ldir / "exp07_D10_joint.npz",
             s_idx=np.array([g["s_idx"] for g in groups]),
             s_grid=np.array([g["s"] for g in groups]),
             deltas=np.array([g["delta"] for g in groups]),
             branch=np.array([g["branch"] for g in groups]),
             pair_idx=pair_idx,
             theta=theta_arr,
             unit_ids=np.array(uids, dtype=np.int64),
             s_post=s_post, o_post=o_post, s_pre=s_pre, o_pre=o_pre,
             q_post=q_post, q_se_unit=q_se,
             s05=s05_arr,
             q_sim30=q_sim30,
             pairs=np.array([(p["delta_idx"], p["s_idx"]) for p in pairs]),
             win_mean=wmean, win_se=wse)
    manifest = build_manifest(
        line="joint", d10="D10a+b", provenance=provenance,
        s06_ref=S06_REF, s04_ref=S04_REF,
        points={"n_points": G, "sparse": "s_idx=1,8,…,99 x {0.85,-2} x 3分支",
                "order": "每 s 先 δ=0.85 后 δ=-2，每 (s,δ) 内 triv→topo→AFM"},
        shots=SHOTS, p_level=P, chip=info.get("chip", "Baihua"),
        n_units=U,
        endpoints={"S_max": S_max, "O_max": O_max,
                   "method": "top1-max-pooled-window-90"},
        window={"start": ws, "length": wl, "N": U,
                "mean_r": win["mean_r"], "pooled_d_raw": win["pooled_d_raw"],
                "S_max": S_max, "O_max": O_max},
        branch_stats={"r_a": win["r_a"], "d_raw_a": win["d_raw_a"]},
        report={"mode": "report-only", "no_threshold": True},
        stderr_def="unit-multinomial-plugin + window-inter-unit-SE",
        readout_mitigation=dict(READOUT_MITIGATION),
        calibration_mapping=calibration_mapping_record(groups, phys_of, "branch"),
        toolchain=_toolchain(), python=sys.executable)
    write_json(ldir / "exp07_manifest_joint.json", manifest)
    print(f"joint：{U} 完整单位，窗口 start={ws} len={wl} "
          f"mean_r={win['mean_r']:.4f} pooled_d={win['pooled_d_raw']:.4f}"
          "（report-only）")


def _toolchain() -> dict:
    import importlib.metadata as md

    def ver(pkg: str) -> str:
        try:
            return md.version(pkg)
        except Exception:
            return "unknown"
    return {"qiskit": ver("qiskit"), "qiskit_aer": ver("qiskit-aer"),
            "quarkstudio": ver("quarkstudio"),
            "quarkcircuit": ver("quarkcircuit"),
            "numpy": ver("numpy")}


if __name__ == "__main__":
    main()
