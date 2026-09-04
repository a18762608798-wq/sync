import asyncio
import os
from dataclasses import dataclass

import numpy as np
from qiskit import QuantumCircuit, qasm2, transpile
from qiskit.circuit import CircuitInstruction, Clbit
from qiskit.circuit.library import RZGate
from qiskit_aer import AerSimulator
from quark import Task

from .config import AerOptions, QuarkOptions, RandomMeasConfig
from .ensemble import create_parameter_generator
from .io import save_npz, write_summary

Counts = dict[str, int]


@dataclass
class RunResult:
    counts: list[Counts]
    trivial_counts: list[Counts] | None = None


async def run_random(config: RandomMeasConfig) -> dict:
    """随机测量管线: 采样角度、加旋转门、按 setting 执行, 落盘为 npz + 轻量 json。"""
    qc_meas = add_meas(config.qc.copy(), config.params, config.meas_indices)

    # 每个 SettingRun 一个独立子流: 各自可复现, 互不干扰
    param_gens = [
        create_parameter_generator(config.ensemble, seed=c)
        for c in np.random.SeedSequence(config.seed).spawn(len(config.setting_runs))
    ]
    bind_groups = [
        gen.generate(config.params, sr.num_settings)
        for gen, sr in zip(param_gens, config.setting_runs)
    ]
    trivial_qc = _prepare_trivial_qc(config)

    run_results = []
    for run_idx, setting_run in enumerate(config.setting_runs):
        run_results.append(
            await _run_one(
                config.runner_opts,
                qc_meas,
                bind_groups[run_idx],
                setting_run,
                name=f"{config.name}_setting{run_idx}",
                trivial_qc=trivial_qc,
            )
        )

    npz_paths = [
        save_npz(
            config,
            run_idx,
            setting_run,
            bind_groups[run_idx],
            run_results[run_idx].counts,
            trivial_binds=(bind_groups[run_idx] if trivial_qc is not None else None),
            trivial_counts=run_results[run_idx].trivial_counts,
            trivial_num_shots=setting_run.num_shots if trivial_qc is not None else None,
        )
        for run_idx, setting_run in enumerate(config.setting_runs)
    ]

    return write_summary(config, npz_paths)


async def _run_one(opts, qc, binds, setting_run, *, name, trivial_qc):
    if isinstance(opts, AerOptions):
        return await _run_aer(
            opts, qc, binds, setting_run, name=name, trivial_qc=trivial_qc
        )
    return await _run_quark(opts, qc, binds, setting_run, name, trivial_qc)


# ── Aer ────────────────────────────────────────────────────────────


async def _run_aer(opts, qc, binds, setting_run, *, name, trivial_qc):
    simulator = AerSimulator(
        method=opts.method,
        device=opts.device,
        precision=opts.precision,
    )
    job = simulator.run(
        transpile(qc, simulator),
        shots=setting_run.num_shots,
        parameter_binds=[binds],
    )
    counts = [job.result().get_counts(i) for i in range(setting_run.num_settings)]
    if trivial_qc is None:
        return RunResult(counts=counts)

    trivial_job = simulator.run(
        transpile(trivial_qc, simulator),
        shots=setting_run.num_shots,
        parameter_binds=[binds],
    )
    trivial_counts = [
        trivial_job.result().get_counts(i) for i in range(setting_run.num_settings)
    ]
    return RunResult(counts=counts, trivial_counts=trivial_counts)


# ── Quark ──────────────────────────────────────────────────────────


async def _run_quark(opts, qc, binds, setting_run, *, name, trivial_qc):
    qasm_ls = _to_qasm2(qc, setting_run.num_settings, binds, opts)
    trivial_qasm_ls = None
    if trivial_qc is not None:
        trivial_qasm_ls = _to_qasm2(trivial_qc, setting_run.num_settings, binds, opts)

    tmgr = Task(opts.token or os.environ["QUARK_TOKEN"])
    tids = []
    for i, qasm_str in enumerate(qasm_ls):
        tids.append(
            _submit_quark(tmgr, opts, qasm_str, setting_run.num_shots, f"{name}_U{i}")
        )
        if trivial_qasm_ls is not None:
            tids.append(
                _submit_quark(
                    tmgr,
                    opts,
                    trivial_qasm_ls[i],
                    setting_run.num_shots,
                    f"{name}_calib_U{i}",
                )
            )

    awaiters = [asyncio.create_task(_await_quark(tmgr, tid)) for tid in tids]
    try:
        counts = await asyncio.gather(*awaiters)
    except Exception:
        for a in awaiters:
            a.cancel()
        raise

    if trivial_qasm_ls is None:
        return RunResult(counts=counts)
    return RunResult(counts=counts[0::2], trivial_counts=counts[1::2])


def _submit_quark(tmgr, opts, qasm_str, shots, name):
    task = {
        "chip": opts.chip,
        "shots": shots,
        "name": name,
        "circuit": qasm_str,
        "options": {
            "compiler": "qiskit",
            "correct": opts.correct,
            "target_qubits": opts.target_qubits,
        },
    }
    return tmgr.run(task)


async def _await_quark(tmgr, tid):
    """轮询任务结果, 返回计数字典。

    排队/运行中平台返回非空 dict 但缺 "count" 键 (error 为空);
    若 "error" 有实际内容表示平台失败, 打印后继续轮询,
    直到拿到含 "count" 的结果。
    """
    res = {}
    while "count" not in res:
        await asyncio.sleep(10)
        res = tmgr.result(tid)
        if res.get("error"):
            print(f"quark 任务 {tid}: {res['error']}")
    return res["count"]


# ── Circuit & params ───────────────────────────────────────────────


def add_meas(qc, params, meas_indices):
    """按分组加随机测量旋转门与测量指令; 所需经典位由 meas 元素个数决定, 自动补齐。"""
    flat_indices = []
    for group_idx, group in enumerate(meas_indices):
        for qubit_idx in group:
            flat_indices.append(qubit_idx)
    if (missing := len(flat_indices) - qc.num_clbits) > 0:
        qc.add_bits([Clbit() for _ in range(missing)])
    theta, phi = params
    for group_idx, group in enumerate(meas_indices):
        for qubit_idx in group:
            qc.u(-theta[group_idx], 0, -phi[group_idx], qubit_idx)
    qc.measure(flat_indices, range(len(flat_indices)))
    return qc


def _to_qasm2(qc, num_settings, binds, opts):
    """绑参数 → 本地 transpile → 防裸测量比特 → QASM2。"""
    qasm_ls = []
    for i in range(num_settings):
        bound = qc.assign_parameters({p: vals[i] for p, vals in binds.items()})
        basic = transpile(
            bound,
            basis_gates=opts.basis_gates,
            optimization_level=opts.optimization_level,
            coupling_map=opts.coupling_map,
        )
        basic = _guard_empty_qubits(basic)
        qasm_ls.append(qasm2.dumps(basic))
    return qasm_ls


def _guard_empty_qubits(qc):
    """Quark 平台缺陷 workaround: 防止"裸测量比特"。

    quark 对"上面没有任何门、只有测量指令"的比特会直接报错。而 transpile
    在高优化级别下会把恒等门优化删除, 例如 Z 基 (θ=φ=0) 的 u(0, 0, 0)。
    这里扫描 transpile 后的电路, 给这类比特在测量前原地插入一个 rz(0):
    允许的基底门、严格物理恒等, 不改变任何测量统计。
    """
    gated = set()
    for inst in qc.data:
        if inst.operation.name != "measure":
            gated.update(qc.find_bit(q).index for q in inst.qubits)

    guarded = set()
    pos = 0
    while pos < len(qc.data):
        inst = qc.data[pos]
        if inst.operation.name == "measure":
            for q in inst.qubits:
                i = qc.find_bit(q).index
                if i not in gated and i not in guarded:
                    qc.data.insert(
                        pos, CircuitInstruction(RZGate(0.0), (qc.qubits[i],), ())
                    )
                    guarded.add(i)
                    pos += 1
        pos += 1
    return qc


def _prepare_trivial_qc(config):
    """开启 mitigation 时构造 |0⟩^⊗n 的 trivial 测量电路, 否则返回 None。

    trivial 电路 = 无态制备 + 与主电路相同的测量旋转与测量指令,
    角度绑定与 shot 数均直接复用主电路的设置。
    """
    if not config.runner_opts.mitigation:
        return None

    return add_meas(
        QuantumCircuit(config.qc.num_qubits),
        config.params,
        config.meas_indices,
    )
