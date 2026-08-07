import asyncio
import os


from qiskit import qasm2
from quark import Task


from assign_quark_task import (
    get_commute_group,
    add_meas,
    get_meas_params,
    get_pauli_expval_map,
    get_op_vals,
)


async def submit_quark_task(
    qc,
    *,
    shot_num=1024,
    token=None,
    chip="Baihua",
    correct=True,
    name="my_job",
    target_qubits=None,
):
    if token == None:
        token = os.getenv("QUARK_TOKEN")
    if target_qubits == None:
        target_qubits = []
    qasm2_string = qasm2.dumps(qc)
    tmgr = Task(token)
    task = {
        "chip": chip,  # the quantum computer choice,
        "name": name,
        "circuit": qasm2_string,
        "shots": shot_num,
        "options": {
            "compiler": "qiskit",
            "correct": correct,
            "target_qubits": target_qubits,  # 具体bit而非范围, [] is automatic choice.
        },
    }
    tid = tmgr.run(task)  # shot_num = repeat*1024
    res = {}
    while res == {}:
        await asyncio.sleep(10)
        res = tmgr.result(tid)
    return res["count"]


async def submit_ops_task(
    qc,
    obs,
    *,
    shot_num=1024,
    token=None,
    chip="Baihua",
    correct=True,
    name="my_job",
    target_qubits=None,
):
    groups, meas_pauli_ls = get_commute_group(obs)
    group_num = len(groups)

    qc, theta, phi = add_meas(qc)
    binds = get_meas_params(meas_pauli_ls, theta, phi)
    hists = []
    for group_idx in range(group_num):
        bind = {param: vals[group_idx] for param, vals in binds.items()}
        group_qc = qc.assign_parameters(bind)
        hist = await submit_quark_task(
            group_qc,
            shot_num=shot_num,
            token=token,
            chip=chip,
            correct=correct,
            name=name,
            target_qubits=target_qubits,
        )
        hists.append(hist)
    expval_map = get_pauli_expval_map(groups, hists, shot_num)
    op_vals = get_op_vals(obs, expval_map)
    result = {
        "ops": obs,
        "pauli_groups": groups,
        "meas_pauli_ls": meas_pauli_ls,
        "op_vals": op_vals,
    }
    return result
