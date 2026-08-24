import asyncio
import os

import numpy as np
from qiskit import QuantumCircuit, qasm2, transpile
from qiskit.circuit import CircuitInstruction, ParameterVector
from qiskit.circuit.library import RZGate
from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp
from qiskit_aer.primitives import EstimatorV2
from quark import Task

from .basis import QubitwiseBasis
from .config import AerEstimatorOptions, EstimatorConfig, QuarkEstimatorOptions

# 测量基旋转角: 每行 [rx 角(绕 x), ry 角(绕 y)], 对应待测 Pauli。
PAULI_ROTATIONS = np.array(
    [
        [0, -np.pi / 2],  # X
        [np.pi / 2, 0],  # Y
        [0, 0],  # Z
    ],
    dtype=float,
)


async def run_estimator(config):
    if isinstance(config.runner_opts, AerEstimatorOptions):
        return await _run_aer(config)
    return await _run_quark(config)


# ── Aer ────────────────────────────────────────────────────────────


async def _run_aer(config):
    estimator = EstimatorV2(
        options={
            "backend_options": {"method": config.runner_opts.method},
        }
    )
    pubs = [(config.qc.decompose(), ob) for ob in config.observables]
    job = estimator.run(pubs)
    result = job.result()
    evs = [r.data.evs for r in result]
    return {"evs": evs}


# ── Quark (qubitwise) ──────────────────────────────────────────────


async def _run_quark(config):
    opts = config.runner_opts
    token = opts.token or os.environ["QUARK_TOKEN"]

    groups, meas_pauli_ls = group_qubitwise(config.observables)
    qc_with_params, theta_x, theta_y = _add_meas(config.qc.copy(), config.qc.num_qubits)

    basis = QubitwiseBasis()
    expval_map = {}

    for group_idx in range(len(groups)):
        be_meas = _prepare_notbound(
            qc_with_params, group_idx, meas_pauli_ls, theta_x, theta_y
        )
        hist = await _submit_quark(be_meas, token, opts, f"{opts.name}_g{group_idx}")
        expects = basis.recover(groups[group_idx], hist, opts.shots)
        expval_map.update(expects)

    evs = _rebuild_op_vals(config.observables, expval_map)
    return {"evs": evs}


# ── Group & rotate ─────────────────────────────────────────────────


def group_qubitwise(observables):
    pauli_set = {label for ob in observables for label in ob.paulis.to_labels()}
    pauli_list = PauliList(sorted(pauli_set))
    groups = pauli_list.group_commuting(qubit_wise=True)
    meas_pauli_ls = []
    for group in groups:
        basis_x = np.logical_or.reduce(group.x, axis=0)
        basis_z = np.logical_or.reduce(group.z, axis=0)
        meas_pauli_ls.append(Pauli((basis_z, basis_x)))
    return groups, meas_pauli_ls


def _add_meas(qc, num_qubits):
    theta_x = ParameterVector("θx", num_qubits)  # rx 角: 绕 x 轴
    theta_y = ParameterVector("θy", num_qubits)  # ry 角: 绕 y 轴
    for i in range(num_qubits):
        qc.rx(theta_x[i], i)
        qc.ry(theta_y[i], i)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc, theta_x, theta_y


def _prepare_notbound(qc, group_idx, meas_pauli_ls, theta_x, theta_y):
    binds = _group_params(group_idx, meas_pauli_ls, theta_x, theta_y)
    return qc.assign_parameters(binds)


def _group_params(group_idx, meas_pauli_ls, theta_x, theta_y):
    num_qubits = len(meas_pauli_ls[0])
    pauli = meas_pauli_ls[group_idx]
    binds = {}
    for i in range(num_qubits):
        if pauli.x[i] and not pauli.z[i]:
            idx = 0  # X
        elif pauli.z[i] and not pauli.x[i]:
            idx = 2  # Z
        elif pauli.x[i] and pauli.z[i]:
            idx = 1  # Y
        else:
            idx = 2  # I → behave as Z (no rotation needed)
        binds[theta_x[i]] = PAULI_ROTATIONS[idx, 0]
        binds[theta_y[i]] = PAULI_ROTATIONS[idx, 1]
    return binds


# ── Quark submit ───────────────────────────────────────────────────


def _guard_empty_qubits(qc):
    """Quark 平台缺陷 workaround: 防止"裸测量比特"。

    quark 对"上面没有任何门、只有测量指令"的比特会直接报错。而上面的 transpile
    在 optimization_level=3 下会把恒等门优化删除, 例如:
      * `_group_params` 对 I/Z 分量绑定 rx=ry=0, 即恒等门;
      * 原电路 `config.qc` 本身未触及的比特。
    一旦某个比特在测量前没有任何门, quark 就会报错。

    这里扫描 transpile 后的电路, 给这类比特在测量前原地插入一个 rz(0):
    rz(0) 是允许的基底门、严格物理恒等, 不改变任何测量统计。
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


async def _submit_quark(qc, token, opts, name):
    basic_qc = transpile(
        qc,
        basis_gates=["rz", "rx", "ry", "cz"],
        optimization_level=3,  # 优化等级
        coupling_map=opts.coupling_map,
        routing_method="sabre",
    )
    basic_qc = _guard_empty_qubits(basic_qc)
    task = {
        "chip": opts.chip,
        "shots": opts.shots,
        "name": name,
        "circuit": qasm2.dumps(basic_qc),
        "options": {
            "compiler": opts.compiler,
            "correct": opts.correct,
            "target_qubits": opts.target_qubits,
        },
    }
    tmgr = Task(token)
    tid = tmgr.run(task)
    res = {}
    while res == {}:
        await asyncio.sleep(10)
        res = tmgr.result(tid)
    return res["count"]


# ── Rebuild ────────────────────────────────────────────────────────


def _rebuild_op_vals(observables, expval_map):
    vals = []
    for ob in observables:
        v = 0.0
        for pauli, coef in zip(ob.paulis, ob.coeffs):
            v += coef * expval_map[pauli]
        vals.append(v)
    return vals
