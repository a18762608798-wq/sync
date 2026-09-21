import math


from qiskit.quantum_info import SparsePauliOp


def _xx(qubit_num, i):
    return SparsePauliOp.from_sparse_list(
        [
            ("XX", [i, i + 1], 1.0),
        ],
        num_qubits=qubit_num,
    )


def _zz(qubit_num, i):
    return SparsePauliOp.from_sparse_list(
        [
            ("ZZ", [i, i + 1], 1.0),
        ],
        num_qubits=qubit_num,
    )


def _link(qubit_num, i, δ):
    return _xx(qubit_num, i) + δ * _zz(qubit_num, i)


def get_ssh_H(qubit_num, s, δ):
    assert math.isclose(qubit_num / 4 - qubit_num // 4, 0) or math.isclose(
        qubit_num, 0
    ), "The number of qbits must in 4N^+."
    # Params settings
    J1 = 1 - s
    J2 = s
    pair_num = qubit_num // 2
    H1 = 0.0 * _xx(qubit_num, 0)
    H2 = 0.0 * _xx(qubit_num, 0)
    for pair_idx in range(pair_num - 1):
        i = 2 * pair_idx
        j = 2 * pair_idx + 1
        H1 += _link(qubit_num, i, δ)
        H2 += _link(qubit_num, j, δ)
    H1 += _link(qubit_num, 2 * pair_num - 2, δ)
    ssh_op = J1 * H1 + J2 * H2

    return ssh_op.simplify()


def get_Ui(qubit_num, op):
    if op == "X":
        Ui = SparsePauliOp.from_sparse_list(
            [
                ("X" * qubit_num, [i for i in range(qubit_num)], 1.0),
            ],
            num_qubits=qubit_num,
        )
    elif op == "Z":
        Ui = SparsePauliOp.from_sparse_list(
            [
                ("Z" * qubit_num, [i for i in range(qubit_num)], 1.0),
            ],
            num_qubits=qubit_num,
        )
    else:
        raise ValueError("The op must be X or Z")
    return Ui


def get_ssh_constrained_H(qubit_num, s, δ, ϵ=1):
    H_c = get_ssh_H(qubit_num, s, δ)
    H_c -= ϵ * (get_Ui(qubit_num, "X") + 2 * get_Ui(qubit_num, "Z"))
    return H_c.simplify()
