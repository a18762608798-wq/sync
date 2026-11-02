"""exp06 v3 联测真机提交（烧机时）：转译 → 单轮提交 → 对账补跑。

必须用 qmeas env python 运行。bill.json confirmed=true 才可提交。
每单位任务 = 30 点 VQE + 2 标定（同批，同 S05；两线交错共漂移；
串行交替直发：SUBMIT_CONCURRENCY=1，按 (uid, g序)逐个提交）；
correct=False 参数留存。
转译用逻辑 coupling_map（开链 7 边 / 环 8 边含 0–7），qasm qubit i ↔
target_qubits[i]；转译后 CZ 边集随 unit 落盘，供 verify 验路断言。
中断续跑只补缺失：已有 tid 只轮询不重提，已收回永不重提。
v2 分线提交已归档，不再使用。
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

from exp06_circuits import (  # noqa: E402
    L,
    build_calib_circuits,
    build_estimator_circuit,
)
from exp06_common import (  # noqa: E402
    JOINT_LINE,
    P_LEVEL,
    SHOTS,
    line_dir,
    read_json,
    unit_state_path,
    write_json,
)

BASIS_GATES = ["rz", "rx", "ry", "cz"]
OPT_LEVEL = 3
MAX_AUDIT_ROUNDS = 2
NPL = L  # δ≠0：每层 L 参数（p=1 → 8 参数；δ=0 减半已退役）
_TCACHE: dict = {}  # 同一逻辑电路全单位共用一次转译结果（单位是时间重复，转译一致更干净）


def cached_transpile(qc, a_star: int):
    key = (qasm2.dumps(qc), a_star)
    t = _TCACHE.get(key)
    if t is None:
        t = transpile(qc, basis_gates=BASIS_GATES,
                      optimization_level=OPT_LEVEL,
                      coupling_map=logical_edges(a_star))
        _TCACHE[key] = t
    return t

# 串行交替提交（spec 同批自然时间相邻）：SUBMIT_CONCURRENCY=1，
# 提交按 (uid, g序) 逐个直接 await，直发顺序即平台排队顺序；
# g序 = groups.json 既定交替（每 s 先 δ=0.85 后 δ=−2）+ 2 标定殿后。
# 注意：await_quark 整个生命周期占一个 poll 槽（排队中也占），并发过低会让
# 绝大多数任务干等，因此 poll 并发按任务数取大值；真正请求速率由
# poll_interval（10s/任务）约束。轮询只收数，不影响芯片侧执行序。
SUBMIT_CONCURRENCY = 1
POLL_CONCURRENCY = 300


def logical_edges(a_star: int) -> list:
    edges = [[i, i + 1] for i in range(L - 1)]
    if a_star == 2:  # topo：0–7 闭合边（link 语义，spec INV-003）
        edges.append([0, L - 1])
    return edges


def allowed_edges(a_star: int) -> set:
    base = {(i, i + 1) for i in range(L - 1)}
    if a_star == 2:
        base.add((0, L - 1))
    return base


def cz_edges(tqc) -> set:
    out = set()
    for inst in tqc.data:
        if inst.operation.name == "cz":
            qs = sorted(tqc.find_bit(q).index for q in inst.qubits)
            out.add(tuple(qs))
    return out


def build_unit_tasks(groups, theta_map, phys_map) -> dict[str, QuantumCircuit]:
    """一个单位的全部逻辑电路：{task_key: circuit}（不转译）。"""
    circuits: dict[str, QuantumCircuit] = {}
    for gi, g in enumerate(groups):
        key = (g["delta_idx"], g["s_idx"], g["p"])
        th, a = theta_map[key]
        circuits[f"g{gi}"] = build_estimator_circuit(
            th, a, g["p"], g["delta"])
    circuits.update(build_calib_circuits())
    return circuits


def unit_task_meta(groups, phys_map) -> tuple[dict, dict]:
    task_phys: dict[str, list[int]] = {}
    task_a: dict[str, int] = {}
    for gi, g in enumerate(groups):
        task_phys[f"g{gi}"] = phys_map[g["a_star"]]
        task_a[f"g{gi}"] = g["a_star"]
    first_a = groups[0]["a_star"]
    for k in ("cal_zero", "cal_one"):
        task_phys[k] = phys_map[first_a]
        task_a[k] = first_a
    return task_phys, task_a


def prepare_unit(line: str, uid: int, groups: list[dict], theta_map: dict,
                 phys_map: dict, pilot: bool = False) -> dict:
    """构建单位全部电路 + 转译审计记录（同步；缺失才做，可先于提交全量做完）。"""
    state_path = unit_state_path(line, uid, pilot)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    circuits = build_unit_tasks(groups, theta_map, phys_map)
    task_phys, task_a = unit_task_meta(groups, phys_map)
    state = (read_json(state_path) if state_path.is_file()
             else {"tids": {}, "tids_history": {}, "counts": {},
                   "transpile": {}, "submit_params": {}})
    state.setdefault("tids_history", {})
    qasm_cache = {}
    for key, qc in circuits.items():
        if key not in state["transpile"]:
            t = cached_transpile(qc, task_a[key])
            edges = sorted(cz_edges(t))
            state["transpile"][key] = {
                "cz_edges": edges, "a_star": task_a[key],
                "in_allowed": all(tuple(e) in allowed_edges(task_a[key])
                                  for e in edges)}
            state["submit_params"][key] = {
                "shots": SHOTS, "correct": False,
                "optimization_level": OPT_LEVEL,
                "basis_gates": BASIS_GATES,
                "target_qubits": task_phys[key]}
            write_json(state_path, state)
        qasm_cache[key] = qasm2.dumps(cached_transpile(qc, task_a[key]))
    return {"uid": uid, "circuits": circuits, "task_phys": task_phys,
            "task_a": task_a, "qasm": qasm_cache,
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
                    continue  # 提交异常，下轮补提（tid 未落盘）
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
                continue  # 轮询异常，下轮重查（tid 留存）
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, default=1)
    args = ap.parse_args()
    ldir = line_dir(JOINT_LINE, False)
    bill = read_json(ldir / "rounds" / f"r{args.round:03d}" / "bill.json")
    if not bill.get("confirmed", False):
        raise RuntimeError("bill.json confirmed=false：须人工确认账单后才可提交")
    chip = "Baihua"
    tag = f"exp06_joint_r{args.round:03d}"
    info = read_json(ldir / "groups.json")
    groups = info["groups"]
    assert len(groups) == 30, len(groups)
    uids = list(range(int(bill["unit_start"]),
                      int(bill["unit_start"]) + int(bill["n_units"])))
    s03 = np.load(line_dir(JOINT_LINE).parent.parent / "exp04"
                  / "exp04_S03.npz")
    meta, th = s03["meta"], s03["theta"]
    theta_map: dict = {}
    for r in range(len(meta)):
        di, si, p, a = (int(v) for v in meta[r])
        assert len(th[r]) >= NPL * p
        theta_map[(di, si, p)] = (th[r][:NPL * p], a)
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
    jobs = [prepare_unit(JOINT_LINE, uid, groups, theta_map, phys_map,
                         False) for uid in uids]
    asyncio.run(submit_poll_all(jobs, base_opts, tmgr, chip, tag))


if __name__ == "__main__":
    main()
