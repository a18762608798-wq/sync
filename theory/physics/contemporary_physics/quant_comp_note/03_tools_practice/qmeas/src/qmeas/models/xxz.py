from qiskit import QuantumCircuit


def get_initial_state(qubit_num, phase_idx=1):
    """构造 XXZ 模型各相的初态电路。

    phase_idx 取 1 / -1 / 0, 对应 XXZ 相图中的不同相区。
    """
    qc = QuantumCircuit(qubit_num)
    # s = 0, δ = 0
    if phase_idx == 1:
        for i in range(0, qubit_num, 1):
            qc.x(i)
        for i in range(0, qubit_num, 2):
            qc.h(i)
        for i in range(0, qubit_num - 1, 2):
            qc.cx(i, i + 1)
    # δ = +∞
    elif phase_idx == 0:
        start, _ = divmod(qubit_num, 2)
        qc.h([start])
        qc.cx(
            [i for i in range(start, 0, -1)],
            [i for i in range(start - 1, -1, -1)],
        )
        qc.cx(
            [i for i in range(start, qubit_num - 1)],
            [i for i in range(start + 1, qubit_num)],
        )
        qc.x([2 * i + 1 for i in range(qubit_num // 2)])
    # s = 1, δ = 0
    elif phase_idx == -1:
        for i in range(0, qubit_num, 1):
            qc.x(i)
        for i in range(1, qubit_num - 1, 2):
            qc.h(i)
        for i in range(1, qubit_num - 2, 2):
            qc.cx(i, i + 1)
        qc.h(0)
        qc.cx(0, qubit_num - 1)
    else:
        raise ValueError("The value of phase_idx must be 1, -1, 0.")
    return qc
