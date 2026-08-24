from qiskit import QuantumCircuit


QUBITNUM = 8


def get_initial_state():
    qc = QuantumCircuit(QUBITNUM, QUBITNUM)
    # Δ = 1 (Heisenberg), s = 0
    for i in range(QUBITNUM):
        qc.x(i)
    for i in range(0, QUBITNUM, 2):
        qc.h(i)
    for i in range(0, QUBITNUM - 1, 2):
        qc.cx(i, i + 1)
    return qc
