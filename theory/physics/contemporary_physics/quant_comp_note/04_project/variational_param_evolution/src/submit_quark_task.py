import asyncio
import os


from qiskit import qasm2
from quark import Task


async def submit_quark_task(
    qc,
    shot_num,
    *,
    token=None,
    chip="Baihua",
    correct=False,
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
