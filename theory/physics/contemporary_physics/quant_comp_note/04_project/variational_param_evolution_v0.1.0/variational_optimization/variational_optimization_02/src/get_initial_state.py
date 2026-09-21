from qiskit import QuantumCircuit

LOOPNUM = 10
QUBITNUM = 8
COUPLING_MAP = [pair for i in range(LOOPNUM - 1) for pair in [[i, i + 1], [i + 1, i]]]
COUPLING_MAP.append([0, LOOPNUM - 1])
COUPLING_MAP.append([LOOPNUM - 1, 0])


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
    # δ = 0, s ≠ ± 1
    elif phase_idx == 0:
        start, _ = divmod(QUBITNUM, 2)
        qc.h([start])
        qc.cx([i for i in range(start, 0, -1)], [i for i in range(start - 1, -1, -1)])
        qc.cx(
            [i for i in range(start, QUBITNUM - 1)],
            [i for i in range(start + 1, QUBITNUM)],
        )
        qc.x([2 * i + 1 for i in range(QUBITNUM // 2)])
        qc.h([i for i in range(QUBITNUM)])
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
    else:
        raise ValueError("The value of phase_idx must be 1, -1, 0.")
    return qc
