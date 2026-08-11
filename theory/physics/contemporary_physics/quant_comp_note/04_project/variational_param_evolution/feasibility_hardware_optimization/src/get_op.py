from qiskit.quantum_info import SparsePauliOp


LOOPNUM = 10
QUBITNUM = 8


def _xx(loop_num, i):
    return SparsePauliOp.from_sparse_list(
        [
            ("XX", [i, i + 1], 1.0),
        ],
        num_qubits=loop_num,
    )


def _zz(loop_num, i):
    return SparsePauliOp.from_sparse_list(
        [
            ("ZZ", [i, i + 1], 1.0),
        ],
        num_qubits=loop_num,
    )


def _link(loop_num, i, δ):
    return _xx(loop_num, i) + δ * _zz(loop_num, i)


def get_ssh_H(s, δ):
    # Params settings
    J1 = 1 - s
    J2 = s
    pair_num = QUBITNUM // 2
    H1 = 0.0 * _xx(LOOPNUM, 0)
    H2 = 0.0 * _xx(LOOPNUM, 0)
    for pair_idx in range(pair_num - 1):
        i = 2 * pair_idx
        j = 2 * pair_idx + 1
        H1 += _link(LOOPNUM, i, δ)
        H2 += _link(LOOPNUM, j, δ)
    H1 += _link(LOOPNUM, 2 * pair_num - 2, δ)
    ssh_op = J1 * H1 + J2 * H2

    return ssh_op.simplify()


def get_Ui(op):
    if op == "X":
        Ui = SparsePauliOp.from_sparse_list(
            [
                ("X" * QUBITNUM, [i for i in range(QUBITNUM)], 1.0),
            ],
            num_qubits=LOOPNUM,
        )
    elif op == "Z":
        Ui = SparsePauliOp.from_sparse_list(
            [
                ("Z" * QUBITNUM, [i for i in range(QUBITNUM)], 1.0),
            ],
            num_qubits=LOOPNUM,
        )
    else:
        raise ValueError("The op must be X or Z")
    return Ui


def get_ssh_constrained_H(s, δ, ϵ=1):
    H_c = get_ssh_H(s, δ)
    H_c -= ϵ * (get_Ui("X") + 2 * get_Ui("Z"))
    return H_c.simplify()
