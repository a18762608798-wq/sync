from qiskit import QuantumCircuit

LOOPNUM = 10
QUBITNUM = 8


def get_initial_state(phase_idx=1):
    qc = QuantumCircuit(LOOPNUM, LOOPNUM)
    # δ ≠ 0, s = 0
    if phase_idx == 1:
        for i in range(0, QUBITNUM, 1):
            qc.x(i)
        for i in range(0, QUBITNUM, 2):
            qc.h(i)
        for i in range(0, QUBITNUM - 1, 2):
            qc.cx(i, i + 1)
    # δ ≠ 0, s = 1
    elif phase_idx == -1:
        for i in range(0, QUBITNUM, 1):
            qc.x(i)
        for i in range(1, QUBITNUM - 1, 2):
            qc.h(i)
        for i in range(1, QUBITNUM - 2, 2):
            qc.cx(i, i + 1)
        qc.h(0)
        qc.cx(0, QUBITNUM - 1)
    # δ = 0, s ≠ ± 1
    elif phase_idx == 0:
        qc.h([0])
        qc.cx([i for i in range(QUBITNUM - 1)], [i for i in range(1, QUBITNUM)])
        qc.x([2 * i + 1 for i in range(QUBITNUM // 2)])
        qc.h([i for i in range(QUBITNUM)])
    else:
        raise ValueError("The value of phase_idx must be 1, -1, 0.")
    return qc
