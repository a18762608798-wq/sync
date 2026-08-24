from qiskit.quantum_info import SparsePauliOp


QUBITNUM = 8


def _xx(i):
    return SparsePauliOp.from_sparse_list(
        [
            ("XX", [i, i + 1], 1.0),
        ],
        num_qubits=QUBITNUM,
    )


def _yy(i):
    return SparsePauliOp.from_sparse_list(
        [
            ("YY", [i, i + 1], 1.0),
        ],
        num_qubits=QUBITNUM,
    )


def _zz(i):
    return SparsePauliOp.from_sparse_list(
        [
            ("ZZ", [i, i + 1], 1.0),
        ],
        num_qubits=QUBITNUM,
    )


def _link(i):
    # Δ = 1 (Heisenberg)
    return _xx(i) + _yy(i) + _zz(i)


def get_xyz():
    # Δ = 1 (Heisenberg), 区分奇偶键: 返回 (H_odd, H_even)
    pair_num = QUBITNUM // 2
    Ho = 0.0 * _xx(0)
    He = 0.0 * _xx(0)
    for pair_idx in range(pair_num - 1):
        i = 2 * pair_idx
        j = 2 * pair_idx + 1
        Ho += _link(i)
        He += _link(j)
    Ho += _link(2 * pair_num - 2)

    return Ho.simplify(), He.simplify()


def get_ssh_H(s):
    Ho, He = get_xyz()
    ssh_op = Ho + s * He

    return ssh_op.simplify()


def get_Ui(op):
    if op == "X":
        Ui = SparsePauliOp.from_sparse_list(
            [
                ("X" * QUBITNUM, [i for i in range(QUBITNUM)], 1.0),
            ],
            num_qubits=QUBITNUM,
        )
    elif op == "Z":
        Ui = SparsePauliOp.from_sparse_list(
            [
                ("Z" * QUBITNUM, [i for i in range(QUBITNUM)], 1.0),
            ],
            num_qubits=QUBITNUM,
        )
    else:
        raise ValueError("The op must be X or Z")
    return Ui


def get_ssh_constrained_H(s, ϵ=1):
    H_c = get_ssh_H(s)
    H_c -= ϵ * (get_Ui("X") + 2 * get_Ui("Z"))
    return H_c.simplify()
