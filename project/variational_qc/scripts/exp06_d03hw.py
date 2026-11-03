"""exp06 D03 真机三点（烧机时，9 电路）：S02 三代表点 p=1 相匹配态 Z 基测量。

- 点位：trivial (di=1,si=1)、topo (di=1,si=99)、afm (di=2,si=59)；
  初态 = S03 同点 p=1 行的 a_star（须为该相获胜分支 1/2/3，否则 abort），
  theta = S03 同点 p=1 行前 8 参数。
- 每点：1 estimator（Z 基，1024 shots）+ 2 S05 标定（同批，correct=False）。
- 复用 exp06_circuits 构造器 + exp06_submit 转译/提交/轮询原语；
  物理比特映射照抄 submit（triv/afm 用 chain_top1，topo 用 subchain_top1，
  取自 joint/groups.json）。
- 缓解：逐比特 2x2 Kronecker 求逆（同 assemble 口径）；C_ij 按 assemble
  位约定（b>>q ↔ qubit q，|0>=Z+1）；S(q) 同 Exp02 公式，Ŝ=S/8；
  q 网格直接读 data/exp02/exp02_D03.npz（只读）。
- 落盘 data/exp06/d03hw/{state.json, exp06_D03hw.npz, manifest.json}。
- 必须用 qmeas env python 运行。用户已确认（T027 序列授权）：直接提交。
"""

from __future__ import annotations

import argparse
import asyncio
import math
import sys
import time
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, qasm2

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp06_circuits import (  # noqa: E402
    L,
    build_calib_circuits,
    build_estimator_circuit,
)
from exp06_common import (  # noqa: E402
    SHOTS,
    line_dir,
    read_json,
    write_json,
)
from exp06_assemble import (  # noqa: E402
    READOUT_MITIGATION,
    group_Ms,
    mitigate_counts,
)
from exp06_submit import (  # noqa: E402
    BASIS_GATES,
    OPT_LEVEL,
    allowed_edges,
    cached_transpile,
    cz_edges,
    logical_edges,
)

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "exp06" / "d03hw"
NPL = L  # δ≠0：每层 L 参数；p=1 → 8 参数
P = 1
POINTS = [("triv", 1, 1, 1), ("topo", 1, 99, 2), ("afm", 2, 59, 3)]

SUBMIT_CONCURRENCY = 5
POLL_CONCURRENCY = 9


def z_of(bits: int, q: int) -> float:
    return 1.0 - 2.0 * float((bits >> q) & 1)


def s_hat_of(probs: np.ndarray, q_grid: np.ndarray):
    n = 1 << L
    z = np.array([[z_of(b, q) for q in range(L)] for b in range(n)])
    C = (probs[:, None, None] * z[:, :, None] * z[:, None, :]).sum(axis=0)
    S = np.array([float((np.cos(q * (np.arange(L)[:, None]
                                    - np.arange(L)[None, :])) * C).sum() / L)
                  for q in q_grid])
    Shat = S / L
    F = np.zeros((len(q_grid), n))
    ii = np.arange(L)[:, None] - np.arange(L)[None, :]
    for k, q in enumerate(q_grid):
        W = np.cos(q * ii) / (L * L)
        for b in range(n):
            F[k, b] = float((W * np.outer(z[b], z[b])).sum())
    mu = F @ probs
    var = np.maximum(F * F @ probs - mu * mu, 0.0)
    return Shat, np.sqrt(var / SHOTS)


def build_jobs(groups_info: dict):
    s03 = np.load(BASE / "data" / "exp04" / "exp04_S03.npz")
    meta, th = s03["meta"], s03["theta"]
    s_map = {}
    for r in range(len(meta)):
        di, si, p, a = (int(v) for v in meta[r])
        if p == P:
            s_map[(di, si)] = (th[r][:NPL * P], int(a))
    phys_map = {1: groups_info["chain_top1"], 3: groups_info["chain_top1"],
                2: groups_info["subchain_top1"]}
    jobs = {}
    for label, di, si, a_exp in POINTS:
        assert (di, si) in s_map, f"S03 缺点 {(di, si, P)}"
        theta, a = s_map[(di, si)]
        assert a == a_exp, f"{label} 获胜分支 {a} != 期望 {a_exp}，abort"
        delta = float(s03["deltas"][di - 1])
        qc = build_estimator_circuit(np.asarray(theta, dtype=float),
                                     a, P, delta)
        circs = {"est": qc}
        circs.update(build_calib_circuits())
        trans = {}
        for key, c in circs.items():
            t = cached_transpile(c, a)
            edges = cz_edges(t)
            assert all(tuple(e) in allowed_edges(a) for e in edges), \
                f"{label}/{key} 转译越界 {edges}"
            trans[key] = {"edges": sorted(edges), "qasm": qasm2.dumps(t)}
        jobs[label] = {"circuits": circs, "trans": trans, "a_star": a,
                       "theta": [float(v) for v in theta],
                       "di": di, "si": si, "delta": delta,
                       "phys": phys_map[a]}
    return jobs


async def submit_poll(jobs: dict, base_opts, tmgr, chip: str,
                      state: dict) -> dict:
    from qmeas.random.quark_client import await_quark, submit_quark
    sem_sub = asyncio.Semaphore(SUBMIT_CONCURRENCY)
    sem_poll = asyncio.Semaphore(POLL_CONCURRENCY)

    async def submit_one(label, key, qasm, phys):
        async with sem_sub:
            if key in state["tids"].get(label, {}):
                return
            opts = replace_opts(base_opts, chip, phys)
            tid = await asyncio.to_thread(
                submit_quark, tmgr, opts, qasm, SHOTS,
                f"exp06_d03hw_{label}_{key}")
            state["tids"].setdefault(label, {})[key] = int(tid)
            write_json(OUT / "state.json", state)

    for label, job in jobs.items():
        for key in job["circuits"]:
            await submit_one(label, key, job["trans"][key]["qasm"],
                             job["phys"])
    for rnd in range(12):
        missing = [(l, k) for l, j in jobs.items() for k in j["circuits"]
                   if k not in state["counts"].get(l, {})
                   and k in state["tids"].get(l, {})]
        if not missing:
            print("对账通过：9 任务全收回", flush=True)
            return state
        print(f"第 {rnd} 轮轮询 {len(missing)} 任务", flush=True)

        async def poll_one(label, key):
            async with sem_poll:
                opts = replace_opts(base_opts, chip,
                                    jobs[label]["phys"])
                hist = await await_quark(
                    tmgr, state["tids"][label][key], opts, sem_sub,
                    jobs[label]["trans"][key]["qasm"], SHOTS,
                    f"exp06_d03hw_{label}_{key}",
                    attempt_tag=label)
                state["counts"].setdefault(label, {})[key] = hist
                write_json(OUT / "state.json", state)

        await asyncio.gather(*(poll_one(l, k) for l, k in missing))
    bad = [(l, k) for l, j in jobs.items() for k in j["circuits"]
           if k not in state["counts"].get(l, {})]
    raise RuntimeError(f"补跑后仍缺失 {bad} → 判 invalid")


def replace_opts(base_opts, chip, phys):
    from dataclasses import replace
    return replace(base_opts, chip=chip, target_qubits=phys,
                   coupling_map=None)


def assemble(jobs: dict, chip: str, state: dict,
             output_dir: Path = OUT) -> None:
    """Rebuild D03 from complete archived counts without hardware access."""
    d03 = np.load(BASE / "data" / "exp02" / "exp02_D03.npz")
    q_grid = np.asarray(d03["q_grid"], dtype=float)
    out = {"labels": [], "S_hat": [], "S_hat_se": [], "meta": []}
    for label, di, si, a_exp in POINTS:
        job = jobs[label]
        cal = state.get("counts", {}).get(label, {})
        if any(not cal.get(key) for key in ("est", "cal_zero", "cal_one")):
            raise ValueError(f"D03 archived counts incomplete: {label}")
        Ms = group_Ms(cal, job["phys"])
        probs = mitigate_counts(cal["est"], Ms)
        Shat, se = s_hat_of(probs, q_grid)
        out["labels"].append(label)
        out["S_hat"].append(Shat.tolist())
        out["S_hat_se"].append(se.tolist())
        out["meta"].append({"di": di, "si": si, "a_star": job["a_star"],
                            "theta": job["theta"], "delta": job["delta"],
                            "shots": SHOTS, "target_qubits": job["phys"],
                            "s05": Ms})
    output_dir.mkdir(parents=True, exist_ok=True)
    np.savez(output_dir / "exp06_D03hw.npz",
             labels=np.array(out["labels"]),
             S_hat=np.array(out["S_hat"]), S_hat_se=np.array(out["S_hat_se"]),
             q_grid=q_grid)
    write_json(output_dir / "manifest.json",
               {"schema": "exp06/d03hw/v1", "p": P, "shots": SHOTS,
                "points": out["meta"], "s03_ref": "data/exp04/exp04_S03.npz",
                "s04_ref": "data/exp05/exp05_S04.npz",
                "sim_ref": "data/exp02/exp02_D03.npz",
                "chip": chip, "confirmed_by": "用户 2026-10-30（T027 序列授权）",
                "readout_mitigation": dict(READOUT_MITIGATION),
                "stderr_def": "multinomial-plugin; excludes calibration/inversion/projection uncertainty",
                "created_utc": time.strftime("%Y-%m-%dT%H:%M:%S",
                                             time.gmtime()) + "Z"})
    print(f"wrote {output_dir}/exp06_D03hw.npz + manifest.json", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry", action="store_true",
                    help="只转译审计不提交")
    mode.add_argument("--assemble-only", action="store_true",
                      help="仅读取已有 counts 重建 D03，不提交或轮询真机")
    args = ap.parse_args()
    groups_info = read_json(line_dir("joint", False) / "groups.json")
    chip = groups_info["chip"]
    jobs = build_jobs(groups_info)
    if args.assemble_only:
        assemble(jobs, chip, read_json(OUT / "state.json"))
        return
    print("mini-bill：3 点 ×（1 estimator + 2 标定）= 9 任务 × "
          f"{SHOTS} shots，芯片 {chip}，p=1", flush=True)
    for label, job in jobs.items():
        print(f"  {label} (di={job['di']},si={job['si']},"
              f"a*={job['a_star']}): "
              + ", ".join(f"{k}:{len(v['edges'])}CZ"
                          for k, v in job["trans"].items()
                          if k == "est"),
              flush=True)
    state_path = OUT / "state.json"
    state = (read_json(state_path) if state_path.is_file()
             else {"tids": {}, "counts": {}})
    if args.dry:
        print("dry-run：转译审计通过，未提交", flush=True)
        return
    from qmeas.random.quark_client import make_quark_task, quark_token
    from qmeas.random.config import QuarkOptions
    base_opts = QuarkOptions(chip=chip, mitigation=False, correct=False,
                             optimization_level=OPT_LEVEL,
                             basis_gates=list(BASIS_GATES))
    assert base_opts.correct is False
    token = quark_token(base_opts)
    tmgr = make_quark_task(token, base_opts.submit_retries)
    asyncio.run(submit_poll(jobs, base_opts, tmgr, chip, state))

    assemble(jobs, chip, state)


if __name__ == "__main__":
    main()
