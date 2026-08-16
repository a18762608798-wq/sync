import asyncio
import os

import numpy as np
from qiskit import QuantumCircuit, qasm2, transpile
from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp
from qiskit.circuit import ParameterVector
from qiskit_aer.primitives import EstimatorV2
from quark import Task

from .basis import QubitwiseBasis
from .config import AerEstimatorOptions, EstimatorConfig, QuarkEstimatorOptions

PAULI_ROTATIONS = np.array(
    [
        [np.pi / 2, 0],  # X
        [np.pi / 2, np.pi / 2],  # Y
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
    qc_with_params, theta, phi = _add_meas(config.qc.copy(), config.qc.num_qubits)

    basis = QubitwiseBasis()
    expval_map = {}

    for group_idx in range(len(groups)):
        be_meas = _prepare_notbound(
            qc_with_params, group_idx, meas_pauli_ls, theta, phi
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
    theta = ParameterVector("θ", num_qubits)
    phi = ParameterVector("φ", num_qubits)
    for i in range(num_qubits):
        qc.u(-theta[i], 0, -phi[i], i)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc, theta, phi


def _prepare_notbound(qc, group_idx, meas_pauli_ls, theta, phi):
    binds = _group_params(group_idx, meas_pauli_ls, theta, phi)
    return qc.assign_parameters(binds)


def _group_params(group_idx, meas_pauli_ls, theta, phi):
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
        binds[theta[i]] = PAULI_ROTATIONS[idx, 0]
        binds[phi[i]] = PAULI_ROTATIONS[idx, 1]
    return binds


# ── Quark submit ───────────────────────────────────────────────────


async def _submit_quark(qc, token, opts, name):
    basic_qc = transpile(
        qc,
        basis_gates=["rz", "rx", "ry", "cz"],
        optimization_level=3,  # 优化等级
        coupling_map=opts.coupling_map,
        routing_method="sabre",
    )
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
