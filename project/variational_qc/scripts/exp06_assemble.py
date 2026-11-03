"""exp06 v3 联测组装（零机时）：joint units → S05 缓解 → hat 组装 →
共用端点冻结 → Q 组合 → 最优偶数窗口搜索 + 报告 → D08 + manifest。

mitigate_counts / obs_from_probs / obs_basis_arrays /
window_endpoints / combine_Q / d_raw_r /
search_best_even_window / build_manifest 可被
test_exp06_local.py 直接 import（零真机调用）。
qiskit counts 键约定：左起最高位 = qubit L-1（大端字符串），整数值按小端解。
hat 定义（L=8）：Ŝ=S(π)（raw，真机侧除以冻结 S_max），Ô=−O_str
（真机侧除以冻结 O_max）；模拟机固定尺度 Ŝ_sim=S_sim/8、Ô_sim=−O_sim。
Q=4/3−2Ô−(4/3)Ŝ 两边同公式组合，组合后不做二次归一化。
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from optimization_source import validate_s06, protocol_of, file_sha256

from exp06_common import (  # noqa: E402
    EVEN_LEN_MIN,
    JOINT_LINE,
    JOINT_N_POINTS,
    P_LEVEL,
    SHOTS,
    line_dir,
    read_json,
    write_json,
)

L = 8
SCHEMA = "exp06/v3"
READOUT_MITIGATION = {
    "version": 1,
    "model": "tensor-product",
    "normalize_counts_before_inversion": True,
    "probability_repair": "euclidean-simplex-projection",
    "matrix_order": "logical-qubit-ascending; q0-is-rightmost-counts-bit",
    "reference_doi": "10.22331/q-2020-04-24-257",
}


def project_probability_simplex(values: np.ndarray) -> np.ndarray:
    """Euclidean projection onto nonnegative vectors of unit sum."""
    v = np.asarray(values, dtype=float)
    if v.ndim != 1 or v.size == 0 or not np.isfinite(v).all():
        raise ValueError("simplex projection requires a finite nonempty vector")
    ordered = np.sort(v)[::-1]
    thresholds = (np.cumsum(ordered) - 1.0) / np.arange(1, v.size + 1)
    active = np.flatnonzero(ordered > thresholds)
    if active.size == 0:
        raise FloatingPointError("could not determine simplex projection threshold")
    projected = np.maximum(v - thresholds[active[-1]], 0.0)
    if not np.isclose(projected.sum(), 1.0, rtol=0, atol=1e-12):
        raise FloatingPointError("simplex projection lost unit normalization")
    return projected


def mitigate_counts(counts: dict[str, int], Ms: list, n: int = L) -> np.ndarray:
    """Normalize counts, invert the tensor model, then project onto the simplex."""
    if len(Ms) != n:
        raise ValueError("one calibration matrix is required per logical qubit")
    if any(np.asarray(M).shape != (2, 2)
           or not np.isfinite(np.asarray(M, dtype=float)).all() for M in Ms):
        raise ValueError("calibration matrices must be finite 2-by-2 arrays")
    Minvs = [np.linalg.inv(np.asarray(M, dtype=float)) for M in Ms]
    K = Minvs[n - 1]
    for q in range(n - 2, -1, -1):
        K = np.kron(K, Minvs[q])
    p = np.zeros(1 << n)
    for key, c in counts.items():
        if not np.isfinite(c) or c < 0:
            raise ValueError("counts must be finite and nonnegative")
        p[int(key, 2)] += c
    total = p.sum()
    if not np.isfinite(total) or total <= 0:
        raise ValueError("counts must have a positive finite total")
    return project_probability_simplex(K @ (p / total))


def obs_basis_arrays() -> tuple[np.ndarray, np.ndarray]:
    """每基矢观测量值 o_spi[b]、o_ostr[b]（L=8，256 态；定义同 Exp02）。"""
    o_spi = np.zeros(1 << L)
    o_ostr = np.zeros(1 << L)
    for b in range(1 << L):
        z = [1 - 2 * ((b >> q) & 1) for q in range(L)]
        s = 0.0
        for i in range(L):
            for j in range(L):
                s += ((-1) ** (i - j)) * z[i] * z[j]
        o_spi[b] = s / L
        o = 0.0
        for a in (0, 1):
            for c in (6, 7):
                o += z[a] * z[2] * z[3] * z[4] * z[5] * z[c]
        o_ostr[b] = o
    return o_spi, o_ostr


def q_basis_array() -> np.ndarray:
    """每基矢 Q 值（线性：q = E[q_b]，SE 有闭式）。"""
    o_spi, o_ostr = obs_basis_arrays()
    return 4.0 / 3.0 + 2.0 * o_ostr - o_spi / 6.0


def obs_from_probs(probs: np.ndarray) -> tuple[float, float]:
    """S(π) 交错和 + string 对角加权（定义同 Exp02，只读复刻）。"""
    o_spi, o_ostr = obs_basis_arrays()
    return float(np.asarray(probs) @ o_spi), float(np.asarray(probs) @ o_ostr)


def q_of(spi: float, ostr: float) -> float:
    """由 S(π)（raw）、O_str（raw）组 Q（L=8）。"""
    return 4.0 / 3.0 + 2.0 * ostr - spi / 6.0


def unit_q_se(probs: np.ndarray, shots: int) -> float:
    """Multinomial plug-in SE; excludes inversion/projection/calibration uncertainty."""
    qb = q_basis_array()
    mu = float(np.asarray(probs) @ qb)
    var = max(float(np.asarray(probs) @ (qb * qb)) - mu * mu, 0.0)
    return math.sqrt(var / shots)


def window_endpoints(s_mean: np.ndarray, o_mean: np.ndarray) -> dict:
    """窗口内共用端点：本窗口 pooled 30 点均值的 top-1 最大值（Q14）。

    S 用 raw 均值；O 先取 hat（Ô=−O）再取最大值。端点随窗口记录，
    各窗口独立；归一化后本窗口内恒 ≤1。
    """
    S_max = float(np.max(np.asarray(s_mean, dtype=float)))
    O_max = float(np.max(-np.asarray(o_mean, dtype=float)))
    if not O_max > 0:
        O_max = 1e-12
    return {"S_max": S_max, "O_max": O_max,
            "method": "top1-max-pooled-window"}


def q_hat_basis(S_max: float, O_max: float) -> np.ndarray:
    """真机侧组合 Q 的每基矢系数（含冻结端点）：线性，可直接算 SE。"""
    o_spi, o_ostr = obs_basis_arrays()
    return 4.0 / 3.0 - 2.0 * (-o_ostr) / O_max - (4.0 / 3.0) * o_spi / S_max


def combine_Q(s_hw: np.ndarray, o_hw: np.ndarray, S_max: float,
              O_max: float, s_sim_hat: np.ndarray,
              o_sim_hat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """两边同公式组 Q：真机除以冻结端点，模拟固定 hat，不二次归一化。"""
    q_hw = 4.0 / 3.0 - 2.0 * (-np.asarray(o_hw) / O_max) \
        - (4.0 / 3.0) * (np.asarray(s_hw) / S_max)
    q_sim = 4.0 / 3.0 - 2.0 * np.asarray(o_sim_hat) \
        - (4.0 / 3.0) * np.asarray(s_sim_hat)
    return q_hw, q_sim


def d_raw_r(q_hw: np.ndarray, q_sim: np.ndarray) -> tuple[float, float]:
    """raw 平均绝对距离 + Pearson r（组合后不做任何归一化）。"""
    q_hw = np.asarray(q_hw, dtype=float)
    q_sim = np.asarray(q_sim, dtype=float)
    return float(np.mean(np.abs(q_hw - q_sim))), \
        float(np.corrcoef(q_hw, q_sim)[0, 1])


def search_best_even_window(S_units: np.ndarray, O_units: np.ndarray,
                            s_sim_hat: np.ndarray, o_sim_hat: np.ndarray,
                            min_len: int = EVEN_LEN_MIN) -> dict:
    """最优偶数长度窗口：r 最大；并列取 d_raw 最小，再并列取更长，再取更早。

    每个候选窗口用自己 pooled 30 点均值的 top-1 最大值做端点（Q14），
    端点随窗口记录，各窗口独立。report-only：无阈值门，pass 恒为 None。
    """
    S_units = np.asarray(S_units, dtype=float)
    O_units = np.asarray(O_units, dtype=float)
    U, npt = S_units.shape
    assert O_units.shape == (U, npt)
    assert s_sim_hat.shape == (npt,) and o_sim_hat.shape == (npt,)
    assert U >= min_len
    q_sim = 4.0 / 3.0 - 2.0 * o_sim_hat - (4.0 / 3.0) * s_sim_hat
    csum_s = np.vstack([np.zeros((1, npt)), np.cumsum(S_units, axis=0)])
    csum_o = np.vstack([np.zeros((1, npt)), np.cumsum(O_units, axis=0)])
    best = {"start": 0, "length": min_len, "N": U,
            "d_raw": float("inf"), "r": float("-inf"),
            "S_max": float("nan"), "O_max": float("nan")}
    max_len = U if U % 2 == 0 else U - 1
    first = min_len if min_len % 2 == 0 else min_len + 1
    for len_ in range(first, max_len + 1, 2):
        sm = (csum_s[len_:] - csum_s[:U - len_ + 1]) / len_
        om = (csum_o[len_:] - csum_o[:U - len_ + 1]) / len_
        for i in range(sm.shape[0]):
            ep = window_endpoints(sm[i], om[i])
            qh, _ = combine_Q(sm[i], om[i], ep["S_max"], ep["O_max"],
                              s_sim_hat, o_sim_hat)
            d, r = d_raw_r(qh, q_sim)
            if (r > best["r"] + 1e-12
                    or (abs(r - best["r"]) <= 1e-12
                        and (d < best["d_raw"] - 1e-12
                             or (abs(d - best["d_raw"]) <= 1e-12
                                 and (len_ > best["length"]
                                      or (len_ == best["length"]
                                          and i < best["start"])))))):
                best = {"start": int(i), "length": int(len_), "N": U,
                        "d_raw": d, "r": r,
                        "S_max": ep["S_max"], "O_max": ep["O_max"]}
    best["pass"] = None
    return best


MANIFEST_KEYS = {"schema", "line", "d08", "s03_ref", "s04_ref", "s06_ref",
                 "points", "shots", "p_level", "chip", "n_units",
                 "endpoints", "window", "report", "stderr_def",
                 "toolchain", "python", "readout_mitigation", "calibration_mapping"}


def build_manifest(**kw) -> dict:
    m = {"schema": SCHEMA}
    m.update(kw)
    missing = MANIFEST_KEYS - set(m)
    if missing:
        raise ValueError(f"manifest 缺字段 {missing}")
    return m


def pkg_versions() -> dict:
    import importlib.metadata as md

    def ver(pkg: str) -> str:
        try:
            return md.version(pkg)
        except Exception:
            return "unknown"

    import qmeas as _qmeas
    root = Path(_qmeas.__file__).resolve().parent.parent.parent
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True,
                                cwd=root).stdout.strip() or "unknown"
    except Exception:
        commit = "unknown"
    return {"qmeas": ver("qmeas"), "qmeas_git": commit,
            "quarkstudio": ver("quarkstudio"),
            "quarkcircuit": ver("quarkcircuit"),
            "qiskit": ver("qiskit"), "qiskit_aer": ver("qiskit-aer")}


def group_Ms(cal_counts: dict, phys: list[int]) -> list:
    """一批的 S05：全 0 / 全 X 电路给出 8 比特各自 2×2 矩阵。

    counts 键比特位 ↔ target_qubits 位置对应（qiskit 大端字符串）。
    M[q] = [[P(0|0), P(0|1)], [P(1|0), P(1|1)]]。
    """
    n = len(phys)
    c0, c1 = cal_counts["cal_zero"], cal_counts["cal_one"]
    s0 = sum(c0.values()) or 1
    s1 = sum(c1.values()) or 1
    Ms = []
    for q in range(n):
        i = n - 1 - q  # 字符串位 i ↔ qubit q；列表按逻辑 qubit 升序。
        p0m = sum(c for k, c in c0.items() if k[i] == "0") / s0
        p1m = sum(c for k, c in c1.items() if k[i] == "1") / s1
        Ms.append([[p0m, 1 - p1m], [1 - p0m, p1m]])
    return Ms


def calibration_mapping_record(groups: list[dict], phys_of: dict,
                               branch_key: str) -> dict:
    """Disclose which measurement mappings lack their own unit calibration."""
    calibration_phys = list(phys_of[groups[0][branch_key]])
    unmatched = [f"g{i}" for i, g in enumerate(groups)
                 if list(phys_of[g[branch_key]]) != calibration_phys]
    return {
        "status": "complete" if not unmatched else "incomplete-physical-mapping-coverage",
        "calibration_target_qubits": calibration_phys,
        "measurement_target_qubits": {str(a): list(q) for a, q in phys_of.items()},
        "mismatched_keys": unmatched,
        "interpretation": "cross-mapping calibration transfer is unvalidated" if unmatched
                          else "measurement and calibration mappings match",
    }


def _probs_of_counts(counts: dict) -> np.ndarray:
    p = np.zeros(1 << L)
    for key, c in counts.items():
        p[int(key, 2)] += c
    s = p.sum()
    return p / s if s > 0 else p


def unit_q_se_qb(probs: np.ndarray, qb: np.ndarray,
                   shots: int) -> float:
    """单位内 multinomial plug-in SE，不含反演、投影与标定不确定性。

    qb 为含冻结端点的组合系数（q_hat_basis），shots=1024。
    """
    probs = np.asarray(probs, dtype=float)
    mu = float(probs @ qb)
    var = max(float(probs @ (qb * qb)) - mu * mu, 0.0)
    return math.sqrt(var / shots)


def main() -> None:
    import argparse as _ap
    ap = _ap.ArgumentParser()
    ap.add_argument("--root", default=None,
                    help="joint 目录覆盖（缺省 data/exp06/joint；synth 沙箱用）")
    a = ap.parse_args()
    from pathlib import Path as _P
    ldir = _P(a.root) if a.root else line_dir(JOINT_LINE, False)
    repo = _P(__file__).resolve().parent.parent
    info = read_json(ldir / "groups.json")
    groups = info["groups"]
    assert {int(g["p"]) for g in groups} == {P_LEVEL}, "exp06 groups must use the specified depth"
    G = len(groups)
    assert G == JOINT_N_POINTS, G
    phys_of = {1: info["chain_top1"], 3: info["chain_top1"],
               2: info["subchain_top1"]}

    unit_dirs = sorted((ldir / "units").glob("[0-9]" * 5)) \
        if (ldir / "units").is_dir() else []
    O_SPI, O_OSTR = obs_basis_arrays()
    s_post, o_post, s_pre, o_pre, s05_all, pmit_all = [], [], [], [], [], []
    uids = []
    theta_rows = []
    s03 = np.load(repo / "data" / "exp04" / "exp04_S03.npz")
    meta, th = s03["meta"], s03["theta"]
    th_map = {}
    for r in range(len(meta)):
        di, si, p, aa = (int(v) for v in meta[r])
        th_map[(di, si, p)] = (th[r], aa)
    for udir in unit_dirs:
        st_path = udir / "state.json"
        if not st_path.is_file():
            continue
        st = read_json(st_path)
        if any(f"g{gi}" not in st.get("counts", {}) for gi in range(G)):
            continue
        if any(k not in st.get("counts", {})
               for k in ("cal_zero", "cal_one")):
            continue
        uid = int(udir.name)
        Ms = group_Ms({k: st["counts"][k]
                       for k in ("cal_zero", "cal_one")},
                      phys_of[groups[0]["a_star"]])
        s05_all.append(Ms)
        rs_post, ro_post, rs_pre, ro_pre, rp = [], [], [], [], []
        for gi in range(G):
            counts = st["counts"][f"g{gi}"]
            p_raw = _probs_of_counts(counts)
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
        uids.append(uid)
        if not theta_rows:
            for g in groups:
                trow, _ = th_map[(g["delta_idx"], g["s_idx"], g["p"])]
                theta_rows.append(trow)
    U = len(uids)
    assert U > 0, "无完整单位"
    s_post = np.array(s_post).reshape(-1, G)
    o_post = np.array(o_post).reshape(-1, G)
    s_pre = np.array(s_pre).reshape(-1, G)
    o_pre = np.array(o_pre).reshape(-1, G)
    theta_arr = np.array(theta_rows).reshape(-1, th.shape[1]) \
        if theta_rows else np.zeros((0, th.shape[1]))
    s05_arr = np.array(s05_all).reshape(-1, L, 2, 2) \
        if s05_all else np.zeros((0, L, 2, 2))

    # 模拟机固定 hat 尺度（S06 列 0=p=1、列 1=p=2；p=1 兼作选窗参照层）。
    s06_path = repo / "data" / "exp04" / "exp04_S06.npz"
    s06 = validate_s06(s06_path)
    tag_of = {1: "dm2", 2: "d085"}
    s_rows = np.array([g["s_idx"] - 1 for g in groups])
    tags = [tag_of[g["delta_idx"]] for g in groups]
    s_sim_hat = np.array([s06[f"{tags[i]}_spi"][s_rows[i], 1] / 8.0
                          for i in range(G)])
    o_sim_hat = np.array([-s06[f"{tags[i]}_ostr"][s_rows[i], 1]
                          for i in range(G)])
    s_sim_hat_p1 = np.array([s06[f"{tags[i]}_spi"][s_rows[i], 0] / 8.0
                             for i in range(G)])
    o_sim_hat_p1 = np.array([-s06[f"{tags[i]}_ostr"][s_rows[i], 0]
                             for i in range(G)])
    q_sim_p2 = 4.0 / 3.0 - 2.0 * o_sim_hat - (4.0 / 3.0) * s_sim_hat
    q_sim_p1 = 4.0 / 3.0 - 2.0 * o_sim_hat_p1 - (4.0 / 3.0) * s_sim_hat_p1

    # 最优偶数窗口搜索：每个候选窗口用自己 pooled 30 点均值的
    # top-1 最大值做端点（Q14），端点随窗口记录。
    # 参照层 p=1（2026-11-01）：与真机 p=1 同层比较；p=2 只作图内对照。
    win = search_best_even_window(s_post, o_post,
                                  s_sim_hat_p1, o_sim_hat_p1)
    ws, wl = int(win["start"]), int(win["length"])
    S_max, O_max = win["S_max"], win["O_max"]
    print(f"最优窗口端点：S_max={S_max:.4f} O_max={O_max:.4f}"
          "（top1-max-pooled-window）")

    # 真机侧：用最优窗口端点组 Q（含端点的基矢线性，直接算 SE）。
    qb = q_hat_basis(S_max, O_max)
    q_post = np.array([[float(p @ qb) for p in rp] for rp in pmit_all])
    q_se = np.array([[unit_q_se_qb(p, qb, SHOTS) for p in rp]
                     for rp in pmit_all])
    wmean = q_post[ws:ws + wl].mean(axis=0)
    wse = q_post[ws:ws + wl].std(axis=0, ddof=1) / math.sqrt(wl) \
        if wl > 1 else np.full(G, np.nan)

    np.savez(ldir / "exp06_D08_joint.npz",
             s_idx=np.array([g["s_idx"] for g in groups]),
             s_grid=np.array([g["s"] for g in groups]),
             deltas=np.array([g["delta"] for g in groups]),
             a_star=np.array([g["a_star"] for g in groups]),
             theta=theta_arr,
             unit_ids=np.array(uids, dtype=np.int64),
             s_post=s_post, o_post=o_post, s_pre=s_pre, o_pre=o_pre,
             q_post=q_post, q_se_unit=q_se,
             s05=s05_arr,
             s_sim_hat=s_sim_hat, o_sim_hat=o_sim_hat,
             s_sim_hat_p1=s_sim_hat_p1, o_sim_hat_p1=o_sim_hat_p1,
             q_sim_p1=q_sim_p1, q_sim_p2=q_sim_p2,
             win_mean=wmean, win_se=wse)
    manifest = build_manifest(
        line=JOINT_LINE, d08="D08a+b",
        s03_ref="data/exp04/exp04_S03.npz",
        s04_ref="data/exp05/exp05_S04.npz",
        s06_ref="data/exp04/exp04_S06.npz",
        optimization_source={"protocol": protocol_of(s06), "s06_sha256": file_sha256(s06_path)},
        points={"n_points": G, "sparse": "s_idx=1,8,…,99 x {0.85,-2}",
                "order": "每 s 先 δ=0.85 后 δ=-2"},
        shots=SHOTS, p_level=P_LEVEL, chip=info.get("chip", "Baihua"),
        n_units=U,
        endpoints={"S_max": S_max, "O_max": O_max,
                   "method": "top1-max-pooled-window"},
        window={"start": ws, "length": wl, "N": U,
                "d_raw": win["d_raw"], "r": win["r"],
                "S_max": S_max, "O_max": O_max},
        report={"mode": "report-only", "no_threshold": True},
        stderr_def="unit-multinomial-plugin + window-inter-unit-SE",
        readout_mitigation=dict(READOUT_MITIGATION),
        calibration_mapping=calibration_mapping_record(groups, phys_of, "a_star"),
        toolchain=pkg_versions(), python=sys.executable)
    write_json(ldir / "exp06_manifest_joint.json", manifest)
    print(f"joint：{U} 完整单位，窗口 start={ws} len={wl} "
          f"d_raw={win['d_raw']:.4f} r={win['r']:.4f}（report-only）")


if __name__ == "__main__":
    main()
