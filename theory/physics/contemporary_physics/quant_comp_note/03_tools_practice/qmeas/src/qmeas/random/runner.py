import asyncio
import json
import os
from dataclasses import dataclass

from qiskit import QuantumCircuit, qasm2, transpile
from qiskit_aer import AerSimulator
from quark import Task

from .config import AerOptions, CorrectionInput, QuarkOptions, RandomMeasConfig
from .ensemble import create_parameter_generator

Counts = dict[str, int]


@dataclass
class RunResult:
    counts: list[Counts]
    trivial_counts: list[Counts] | None = None


async def run_random(config: RandomMeasConfig) -> dict:
    """随机测量管线: 采样角度、加旋转门、按 setting 执行并落盘。"""
    assert config.params is not None

    param_gen = create_parameter_generator(config.ensemble)
    qc_meas = add_meas(config.qc.copy(), config.params, config.meas_indices)

    # 先全部主 setting, 再全部 trivial 参数, 保持 RNG 序列稳定
    bind_groups = [
        param_gen.generate(config.params, sr.setting_num)
        for sr in config.setting_runs
    ]
    correction = _prepare_correction(config)
    trivial_bind_groups = (
        [
            param_gen.generate(config.params, sr.setting_num)
            for sr in config.setting_runs
        ]
        if correction is not None
        else []
    )

    run_results = []
    for run_idx, setting_run in enumerate(config.setting_runs):
        correction_input = None
        if correction is not None:
            correction_input = CorrectionInput(
                trivial_qc=correction.trivial_qc,
                trivial_parameter_binds=trivial_bind_groups[run_idx],
                trivial_shot_num=correction.trivial_shot_num,
            )

        run_results.append(
            await _run_one(
                config.runner_opts,
                qc_meas,
                bind_groups[run_idx],
                setting_run,
                name=f"{config.name}_setting{run_idx}",
                correction_input=correction_input,
            )
        )

    result = _build_result(config, bind_groups, trivial_bind_groups, run_results)
    _write_result(config.output_dir, config.name, result)
    return result


async def _run_one(opts, qc, binds, setting_run, *, name, correction_input):
    if isinstance(opts, AerOptions):
        return await _run_aer(opts, qc, binds, setting_run, name)
    return await _run_quark(opts, qc, binds, setting_run, name, correction_input)


# ── Aer ────────────────────────────────────────────────────────────


async def _run_aer(opts, qc, binds, setting_run, name):
    simulator = AerSimulator(
        method=opts.method,
        device=opts.device,
        precision=opts.precision,
    )
    job = simulator.run(
        transpile(qc, simulator),
        shots=setting_run.shot_num,
        parameter_binds=[binds],
    )
    counts = [
        {bits[::-1]: v for bits, v in job.result().get_counts(i).items()}
        for i in range(setting_run.setting_num)
    ]
    return RunResult(counts=counts)


# ── Quark ──────────────────────────────────────────────────────────


async def _run_quark(opts, qc, binds, setting_run, *, name, correction_input):
    qasm_ls = _bind_to_qasm2(qc, setting_run.setting_num, binds)
    trivial_qasm_ls = None
    if correction_input is not None:
        trivial_qasm_ls = _bind_to_qasm2(
            correction_input.trivial_qc,
            setting_run.setting_num,
            correction_input.trivial_parameter_binds,
        )

    tmgr = Task(opts.token or os.environ["QUARK_TOKEN"])
    tids = []
    for i, qasm_str in enumerate(qasm_ls):
        tids.append(
            _submit_quark(tmgr, opts, qasm_str, setting_run.shot_num, f"{name}_U{i}")
        )
        if trivial_qasm_ls is not None:
            tids.append(
                _submit_quark(
                    tmgr,
                    opts,
                    trivial_qasm_ls[i],
                    correction_input.trivial_shot_num,
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
            "correct": True,
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
    """按分组加随机测量旋转门与测量指令。"""
    theta, phi = params
    flat_indices = []
    for group_idx, group in enumerate(meas_indices):
        for qubit_idx in group:
            qc.u(-theta[group_idx], 0, -phi[group_idx], qubit_idx)
        flat_indices.extend(group)
    qc.measure(flat_indices, range(len(flat_indices)))
    return qc


def _bind_to_qasm2(qc, setting_num, binds):
    return [
        qasm2.dumps(
            qc.assign_parameters({p: vals[i] for p, vals in binds.items()})
        )
        for i in range(setting_num)
    ]


def _prepare_correction(config):
    """Quark 且开启 correction 时准备 trivial 电路, 否则返回 None。"""
    if not isinstance(config.runner_opts, QuarkOptions):
        return None

    correction = config.runner_opts.correction_input
    if correction is None or correction.trivial_qc is not None:
        return correction

    trivial_qc = add_meas(
        QuantumCircuit(config.qc.num_qubits, config.qc.num_clbits),
        config.params,
        config.meas_indices,
    )
    return CorrectionInput(
        trivial_qc=trivial_qc,
        trivial_shot_num=correction.trivial_shot_num,
    )


# ── Result ─────────────────────────────────────────────────────────


def _build_result(config, bind_groups, trivial_bind_groups, run_results):
    opts = config.runner_opts

    result = {
        "runner": "aer" if isinstance(opts, AerOptions) else "quark",
        "ensemble": config.ensemble,
        "setting_runs": [(sr.setting_num, sr.shot_num) for sr in config.setting_runs],
        "qc_num_qubits": config.qc.num_qubits,
        "qc_num_clbits": config.qc.num_clbits,
        "meas_indices": config.meas_indices,
        "params": [_binds_to_vec_dict(b, config.params) for b in bind_groups],
        "count_group": [r.counts for r in run_results],
    }
    if isinstance(opts, QuarkOptions):
        result["chip"] = opts.chip
        result["target_qubits"] = opts.target_qubits

    if trivial_bind_groups:
        result["trivial_params"] = [
            _binds_to_vec_dict(b, config.params) for b in trivial_bind_groups
        ]
        result["trivial_count_group"] = [r.trivial_counts for r in run_results]

    return result


def _binds_to_vec_dict(binds, params):
    """按 ParameterVector 把绑定点转置成 {name: [[setting 0], [setting 1], ...]}。"""
    return {
        pvec.name: [list(col) for col in zip(*[binds[p] for p in pvec])]
        for pvec in params
    }


def _write_result(output_dir, name, result):
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / f"{name}.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
