"""exp07 真机提交：转译 → 单轮提交 → 对账补跑。

必须用项目 CondaPkg env python 运行（PYTHONPATH 含 qmeas src 或装好 qmeas）。
bill.json confirmed=true 才可提交（T002 账单门记录进 bill）。
每单位任务 = 90 点 VQE + 2 标定（同批，同 S05；每 s 先 δ=0.85 后 δ=−2，
每个 (s,δ) 内按 triv→topo→AFM 顺序；串行交替直发：SUBMIT_CONCURRENCY=1）；
correct=False 参数留存。
转译用逻辑 coupling_map（开链 7 边 / 环 8 边含 0–7），qasm qubit i ↔
target_qubits[i]；转译后 CZ 边集随 unit 落盘，供 verify 验路断言。
中断续跑只补缺失：已有 tid 只轮询不重提，已收回永不重提。
三分支各取各自 p=2 最优参数（a* 获胜标签仅记录，不决定执行分支）。
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, qasm2, transpile

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp07_circuits import (  # noqa: E402
    L,
    P,
    TAG_OF_DI,
    branch_theta,
    build_calib_circuits,
    build_estimator_circuit,
)
from exp07_common import (  # noqa: E402
    N_POINTS,
    S06_REF,
    SHOTS,
    line_dir,
    read_json,
    unit_state_path,
    write_json,
)

BASIS_GATES = ["rz", "rx", "ry", "cz"]
OPT_LEVEL = 3
MAX_AUDIT_ROUNDS = 2
S06_PATH = Path(__file__).resolve().parent.parent / S06_REF
_TCACHE: dict = {}

SUBMIT_CONCURRENCY = 1
POLL_CONCURRENCY = 300


def logical_edges(branch: int) -> list:
    edges = [[i, i + 1] for i in range(L - 1)]
    if branch == 2:  # topo：0–7 闭合边（link 语义，spec INV-003）
        edges.append([0, L - 1])
    return edges


def allowed_edges(branch: int) -> set:
    base = {(i, i + 1) for i in range(L - 1)}
    if branch == 2:
        base.add((0, L - 1))
    return base


def cz_edges(tqc) -> set:
    out = set()
    for inst in tqc.data:
        if inst.operation.name == "cz":
            qs = sorted(tqc.find_bit(q).index for q in inst.qubits)
            out.add(tuple(qs))
    return out


def cached_transpile(qc, branch: int):
    key = (qasm2.dumps(qc), branch)
    t = _TCACHE.get(key)
    if t is None:
        t = transpile(qc, basis_gates=BASIS_GATES,
                      optimization_level=OPT_LEVEL,
                      coupling_map=logical_edges(branch))
        _TCACHE[key] = t
    return t


def build_unit_tasks(groups, theta_map, phys_map) -> dict[str, QuantumCircuit]:
    """一个单位的全部逻辑电路：{task_key: circuit}（不转译）。"""
    circuits: dict[str, QuantumCircuit] = {}
    for gi, g in enumerate(groups):
        key = (g["delta_idx"], g["s_idx"], g["branch"])
        th = theta_map[key]
        circuits[f"g{gi}"] = build_estimator_circuit(
            th, g["branch"], P, g["delta"])
    circuits.update(build_calib_circuits())
    return circuits


def unit_task_meta(groups, phys_map) -> tuple[dict, dict]:
    task_phys: dict[str, list[int]] = {}
    task_branch: dict[str, int] = {}
    for gi, g in enumerate(groups):
        task_phys[f"g{gi}"] = phys_map[g["branch"]]
        task_branch[f"g{gi}"] = g["branch"]
    first_b = groups[0]["branch"]
    for k in ("cal_zero", "cal_one"):
        task_phys[k] = phys_map[first_b]
        task_branch[k] = first_b
    return task_phys, task_branch


def prepare_unit(uid: int, groups: list[dict], theta_map: dict,
                 phys_map: dict) -> dict:
    """构建单位全部电路 + 转译审计记录（同步；缺失才做，可先于提交全量做完）。"""
    state_path = unit_state_path(uid)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    circuits = build_unit_tasks(groups, theta_map, phys_map)
    task_phys, task_branch = unit_task_meta(groups, phys_map)
    state = (read_json(state_path) if state_path.is_file()
             else {"tids": {}, "tids_history": {}, "counts": {},
                   "transpile": {}, "submit_params": {}})
    state.setdefault("tids_history", {})
    qasm_cache = {}
    for key, qc in circuits.items():
        if key not in state["transpile"]:
            t = cached_transpile(qc, task_branch[key])
            edges = sorted(cz_edges(t))
            state["transpile"][key] = {
                "cz_edges": edges, "branch": task_branch[key],
                "in_allowed": all(tuple(e) in allowed_edges(task_branch[key])
                                  for e in edges)}
            state["submit_params"][key] = {
                "shots": SHOTS, "correct": False,
                "optimization_level": OPT_LEVEL,
                "basis_gates": BASIS_GATES,
                "target_qubits": task_phys[key]}
            write_json(state_path, state)
        qasm_cache[key] = qasm2.dumps(cached_transpile(qc, task_branch[key]))
    return {"uid": uid, "circuits": circuits, "task_phys": task_phys,
            "task_branch": task_branch, "qasm": qasm_cache,
            "state": state, "state_path": state_path}


async def submit_poll_all(jobs: list[dict], base_opts, tmgr, chip: str,
                          tag: str) -> None:
    """全量一次提交、统一轮询。中断续跑只补缺失：已有 tid 只轮询不重提。"""
    from qmeas.random.quark_client import await_quark, submit_quark

    sem_sub = asyncio.Semaphore(SUBMIT_CONCURRENCY)
    sem_poll = asyncio.Semaphore(POLL_CONCURRENCY)
    for job in jobs:
        job.setdefault("lock", asyncio.Lock())

    async def submit_one(job, key):
        async with sem_sub:
            uid = job["uid"]
            opts = replace(base_opts, chip=chip,
                           target_qubits=job["task_phys"][key],
                           coupling_map=None)
            qasm = job["qasm"][key]
            try:
                tid = await asyncio.to_thread(
                    submit_quark, tmgr, opts, qasm, SHOTS, f"{tag}_u{uid:05d}_{key}")
            except Exception:
                return job, key, None
            async with job["lock"]:
                if key not in job["state"]["tids"]:
                    job["state"]["tids"][key] = int(tid)
                    hist = job["state"].setdefault("tids_history", {})
                    hist.setdefault(key, [])
                    if int(tid) not in hist[key]:
                        hist[key].append(int(tid))
                    write_json(job["state_path"], job["state"])
            return job, key, int(tid)

    async def poll_one(job, key, tid):
        async with sem_poll:
            uid = job["uid"]
            opts = replace(base_opts, chip=chip,
                           target_qubits=job["task_phys"][key])

            async def _on_resubmit(new_tid):
                async with job["lock"]:
                    job["state"]["tids"][key] = int(new_tid)
                    hist = job["state"].setdefault("tids_history", {})
                    hist.setdefault(key, [])
                    if int(new_tid) not in hist[key]:
                        hist[key].append(int(new_tid))
                    write_json(job["state_path"], job["state"])

            try:
                hist = await await_quark(
                    tmgr, tid, opts, sem_sub, job["qasm"][key], SHOTS,
                    f"{tag}_u{uid:05d}_{key}", attempt_tag=f"u{uid:05d}",
                    on_resubmit=_on_resubmit)
            except Exception as e:
                print(f"轮询异常 {tag}_u{uid:05d}_{key}："
                      f"{type(e).__name__}，下轮重查", flush=True)
                return job, key, None
            async with job["lock"]:
                job["state"]["counts"][key] = hist
                write_json(job["state_path"], job["state"])
            return job, key, hist

    for rnd in range(1 + MAX_AUDIT_ROUNDS):
        missing_submit = [(job, k) for job in jobs
                          for k in job["circuits"]
                          if k not in job["state"]["tids"]]
        if missing_submit:
            print(f"第 {rnd} 轮提交 {len(missing_submit)} 任务（串行交替：按 (uid, g序)逐个直发）",
                  flush=True)
            for job, key in missing_submit:
                _, _, tid = await submit_one(job, key)
                if tid is None:
                    continue
            for job in jobs:
                write_json(job["state_path"], job["state"])
        missing_counts = [(job, k) for job in jobs
                          for k in job["circuits"]
                          if k not in job["state"]["counts"]
                          and k in job["state"]["tids"]]
        if not missing_counts:
            print(f"对账通过：{sum(len(j['circuits']) for j in jobs)} 任务全收回",
                  flush=True)
            return
        print(f"第 {rnd} 轮轮询 {len(missing_counts)} 任务（统一等）",
              flush=True)
        for job, key, hist in await asyncio.gather(
                *(poll_one(j, k, j["state"]["tids"][k])
                  for j, k in missing_counts)):
            if hist is None:
                continue
            job["state"]["counts"][key] = hist
        for job in jobs:
            write_json(job["state_path"], job["state"])
    bad = [(job["uid"], k) for job in jobs
           for k in job["circuits"] if k not in job["state"]["counts"]]
    for job in jobs:
        missing = [k for k in job["circuits"]
                   if k not in job["state"]["counts"]]
        if missing:
            write_json(job["state_path"].parent / "invalid.json",
                       {"missing": missing})
    raise RuntimeError(f"补跑后仍缺失 {len(bad)} 任务（例 {bad[:5]}）→ 判 invalid")


def build_theta_map(groups: list[dict]) -> dict:
    """由 groups 反查 S06 theta_leg：key=(delta_idx, s_idx, branch)。"""
    theta_map = {}
    for g in groups:
        key = (g["delta_idx"], g["s_idx"], g["branch"])
        if key not in theta_map:
            theta_map[key] = branch_theta(S06_PATH, *key)
    return theta_map


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--units", type=int, default=None,
                    help="本次提交单位数（默认 bill 全量；调试可用小值）")
    args = ap.parse_args()
    ldir = line_dir()
    bill = read_json(ldir / "rounds" / f"r{args.round:03d}" / "bill.json")
    if not bill.get("confirmed", False):
        raise RuntimeError("bill.json confirmed=false：须人工确认账单后才可提交")
    chip = "Baihua"
    tag = f"exp07_joint_r{args.round:03d}"
    info = read_json(ldir / "groups.json")
    groups = info["groups"]
    assert len(groups) == N_POINTS, len(groups)
    n_units = args.units or int(bill["n_units"])
    uids = list(range(int(bill["unit_start"]),
                      int(bill["unit_start"]) + n_units))
    theta_map = build_theta_map(groups)
    phys_map = {1: info["chain_top1"], 3: info["chain_top1"],
                2: info["subchain_top1"]}

    from qmeas.random.quark_client import make_quark_task, quark_token
    from qmeas.random.config import QuarkOptions
    base_opts = QuarkOptions(chip=chip, mitigation=False, correct=False,
                             optimization_level=OPT_LEVEL,
                             basis_gates=list(BASIS_GATES))
    assert base_opts.correct is False  # 平台矫正确保关闭
    token = quark_token(base_opts)
    tmgr = make_quark_task(token, base_opts.submit_retries)
    jobs = [prepare_unit(uid, groups, theta_map, phys_map) for uid in uids]
    asyncio.run(submit_poll_all(jobs, base_opts, tmgr, chip, tag))


if __name__ == "__main__":
    main()
