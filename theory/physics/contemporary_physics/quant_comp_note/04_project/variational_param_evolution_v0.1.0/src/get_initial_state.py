from qiskit import QuantumCircuit


def get_initial_state(N, phase_idx=1):
    qc = QuantumCircuit(N, N)
    # δ ≠ 0, s = 0
    if phase_idx == 1:
        for i in range(0, N, 1):
            qc.x(i)
        for i in range(0, N, 2):
            qc.h(i)
        for i in range(0, N - 1, 2):
            qc.cx(i, i + 1)
    # δ ≠ 0, s = 1
    elif phase_idx == -1:
        for i in range(0, N, 1):
            qc.x(i)
        for i in range(1, N - 1, 2):
            qc.h(i)
        for i in range(1, N - 2, 2):
            qc.cx(i, i + 1)
        qc.h(0)
        qc.cx(0, N - 1)
    # δ = 0, s ≠ ± 1
    elif phase_idx == 0:
        qc.h([0])
        qc.cx([i for i in range(N - 1)], [i for i in range(1, N)])
        qc.x([2 * i + 1 for i in range(N // 2)])
        qc.h([i for i in range(N)])
    else:
        raise ValueError("The value of phase_idx must be 1, -1, 0.")
    return qc
