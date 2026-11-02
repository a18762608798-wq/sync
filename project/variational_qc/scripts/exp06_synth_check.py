"""exp06 v3 联测合成端到端校验（零真机）：Aer 理想分布 + 读出翻转采样造假单位数据。

前 n_bad 个单位用零参数（坏时段），后 n_good 个用 S03 真参数（好时段）；
跑 assemble → verify（须 VERIFY-EXP06-OK）→ plot；断言窗口落在好段；
跑完删除合成沙箱与合成出图。沙箱：data/exp06_pilot/joint/。
用法：python scripts/exp06_synth_check.py [--bad 12] [--good 12]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp06_circuits import (  # noqa: E402
    L,
    build_calib_circuits,
    build_estimator_circuit,
)
from exp06_common import (  # noqa: E402
    JOINT_LINE,
    PILOT_DIR,
    SHOTS,
    line_dir,
    read_json,
    write_json,
)
from exp06_preview import build_joint_groups  # noqa: E402
from exp06_submit import (  # noqa: E402
    BASIS_GATES,
    OPT_LEVEL,
    allowed_edges,
    cz_edges,
    logical_edges,
)

P00, P11 = 0.95, 0.90  # 合成读出矩阵对角元


def apply_readout(counts: dict[str, int],
                  rng: np.random.Generator) -> dict[str, int]:
    """每串位独立翻转：0→1 概率 1-P00，1→0 概率 1-P11（二项分裂）。"""
    cur = dict(counts)
    for i in range(L):
        nxt: dict[str, int] = {}
        for key, c in cur.items():
            if c <= 0:
                continue
            bit = key[i]
            pf = (1.0 - P00) if bit == "0" else (1.0 - P11)
            nf = int(rng.binomial(c, pf))
            ns = c - nf
            nxt[key] = nxt.get(key, 0) + ns
            if nf:
                fk = key[:i] + ("1" if bit == "0" else "0") + key[i + 1:]
                nxt[fk] = nxt.get(fk, 0) + nf
        cur = nxt
    return {k: v for k, v in cur.items() if v > 0}


def ideal_counts(qc, rng: np.random.Generator, shots: int) -> dict[str, int]:
    from qiskit.quantum_info import Statevector
    qc2 = qc.copy()
    qc2.remove_final_measurements()
    p = np.abs(np.asarray(Statevector.from_instruction(qc2).data)) ** 2
    p = p / p.sum()
    samp = rng.multinomial(shots, p)
    return {format(b, "08b"): int(samp[b]) for b in range(256) if samp[b]}


def synth_joint(n_bad: int, n_good: int, seed: int) -> Path:
    rng = np.random.default_rng(seed)
    ldir = line_dir(JOINT_LINE, True)
    if ldir.is_dir():
        shutil.rmtree(ldir)
    groups, chain, sub, chip = build_joint_groups()
    write_json(ldir / "groups.json",
               {"line": JOINT_LINE, "groups": groups,
                "chain_top1": chain, "subchain_top1": sub, "chip": chip,
                "note": "synth 沙箱，零真机"})
    write_json(ldir / "rounds" / "r001" / "bill.json",
               {"line": JOINT_LINE, "round": 1, "unit_start": 0,
                "n_units": n_bad + n_good, "chip": chip,
                "confirmed": True, "note": "synth 沙箱账单"})
    phys_map = {1: chain, 3: chain, 2: sub}
    s03 = np.load(Path(__file__).resolve().parent.parent / "data"
                  / "exp04" / "exp04_S03.npz")
    meta, th = s03["meta"], s03["theta"]
    th_map = {}
    for r in range(len(meta)):
        ddi, si, p, a = (int(v) for v in meta[r])
        if p == 1:
            th_map[(ddi, si)] = (th[r][:8], a)
    cal = build_calib_circuits()
    from qiskit import transpile as _tp
    for uid in range(n_bad + n_good):
        bad = uid < n_bad
        state = {"tids": {}, "counts": {}, "transpile": {},
                 "submit_params": {}}
        for gi, g in enumerate(groups):
            thv, a = th_map[(g["delta_idx"], g["s_idx"])]
            if bad:
                thv = np.zeros_like(thv)
            qc = build_estimator_circuit(thv, a, 1, g["delta"])
            state["counts"][f"g{gi}"] = apply_readout(
                ideal_counts(qc, rng, SHOTS), rng)
        for k, qc in cal.items():
            state["counts"][k] = apply_readout(
                ideal_counts(qc, rng, SHOTS), rng)
        # 转译审计记录（真实 transpile，零机时）+ 提交参数留存。
        from exp06_submit import build_unit_tasks, unit_task_meta
        circuits = build_unit_tasks(groups,
                                    {(g["delta_idx"], g["s_idx"], 2):
                                     th_map[(g["delta_idx"], g["s_idx"])]
                                     for g in groups}, phys_map)
        tphys, ta = unit_task_meta(groups, phys_map)
        for key, qcc in circuits.items():
            t = _tp(qcc, basis_gates=BASIS_GATES,
                    optimization_level=OPT_LEVEL,
                    coupling_map=logical_edges(ta[key]))
            edges = sorted(cz_edges(t))
            state["transpile"][key] = {
                "cz_edges": edges, "a_star": ta[key],
                "in_allowed": all(tuple(e) in allowed_edges(ta[key])
                                  for e in edges)}
            state["submit_params"][key] = {
                "shots": SHOTS, "correct": False,
                "optimization_level": OPT_LEVEL,
                "basis_gates": BASIS_GATES,
                "target_qubits": tphys[key]}
        sp = ldir / "units" / f"{uid:05d}" / "state.json"
        sp.parent.mkdir(parents=True, exist_ok=True)
        write_json(sp, state)
    print(f"合成 joint：{n_bad} 坏 + {n_good} 好 = {n_bad + n_good} 单位")
    return ldir


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=str(Path(__file__).resolve().parent.parent))
    if r.returncode != 0:
        raise RuntimeError(f"命令失败 rc={r.returncode}: {cmd[0]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bad", type=int, default=12)
    ap.add_argument("--good", type=int, default=12)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    py = sys.executable
    ldir = synth_joint(a.bad, a.good, seed=7)
    run([py, "scripts/exp06_assemble.py", "--root", str(ldir)])
    run([py, "scripts/verify_exp06.py", "--root", str(ldir)])
    man = read_json(ldir / "exp06_manifest_joint.json")
    w = man["window"]
    print(f"joint 窗口：start={w['start']} len={w['length']} "
          f"d_raw={w['d_raw']:.4f} r={w['r']:.4f}")
    nb, ng = a.bad, a.good
    assert w["start"] >= nb and w["start"] + w["length"] <= nb + ng, w
    assert w["length"] >= 10 and w["length"] % 2 == 0, w
    assert w["r"] > 0.9, w
    run([py, "scripts/plot_D08.py", "--root", str(ldir),
         "--suffix", "_synth"])
    print("合成端到端 PASS：窗口落在好段，verify 全过")
    if not a.keep:
        shutil.rmtree(ldir, ignore_errors=True)
        figp = Path(__file__).resolve().parent.parent / "figs" / "exp06"
        for d08 in ("D08a", "D08b"):
            for ext in ("pdf", "png"):
                (figp / f"exp06_{d08}_synth.{ext}").unlink(missing_ok=True)
        print("已清理合成沙箱与合成出图")


if __name__ == "__main__":
    main()
