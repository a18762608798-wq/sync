import asyncio
import os
import sys

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from submit_quark_task import submit_ops_task


def test_submit_ops_task():
    num_qubits = 2
    qc = QuantumCircuit(num_qubits, num_qubits)

    ob = SparsePauliOp.from_list([("XI", 1.0), ("IZ", 1.0), ("YZ", 1.0)])
    obs = [
        ob,
        SparsePauliOp("IY"),
        SparsePauliOp("ZI"),
    ]

    result = asyncio.run(submit_ops_task(qc, obs, shot_num=1024, correct=True))
    print(result)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
