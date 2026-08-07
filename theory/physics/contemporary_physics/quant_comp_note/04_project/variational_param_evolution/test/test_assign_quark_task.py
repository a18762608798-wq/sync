import os
import sys

from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from assign_quark_task import (
    _get_pauli_list_expects,
    add_meas,
    get_commute_group,
    get_meas_params,
    get_op_vals,
    get_pauli_expval_map,
)


def test_get_meas_params_shape_and_value():
    obs = SparsePauliOp.from_list([("XX", 1.0), ("ZZ", 1.0), ("YZ", 1.0)])
    _, meas_pauli_ls = get_commute_group(obs)

    num_qubits = obs.num_qubits
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc, theta, phi = add_meas(qc)

    binds = get_meas_params(meas_pauli_ls, theta, phi)
    print(binds)


def test_get_pauli_list_expects():
    pauli_list = PauliList([Pauli("II"), Pauli("ZZ"), Pauli("XX")])

    # Bell 态 |00>+|11> 在 ZZ 基测量应全落在 00/11，
    # 构造一个在 ZZ 基下近乎确定的直方图。
    hist = {"00": 400, "11": 400, "01": 100, "10": 100}
    shots = sum(hist.values())

    expects = _get_pauli_list_expects(pauli_list, hist, shots)

    print("pauli_list:", pauli_list.to_labels())
    print("hist:", hist, "shots:", shots)
    for pauli in pauli_list:
        print(f"<{pauli.to_label()}> = {expects[pauli]:.4f}")


def test_get_pauli_expval_map():
    groups = [
        PauliList([Pauli("II"), Pauli("ZZ")]),
        PauliList([Pauli("XX")]),
    ]
    # 每个测量基对应一个 histogram，shots 为对应次数之和。
    hists = [
        {"00": 400, "11": 400, "01": 100, "10": 100},
        {"00": 250, "11": 250, "01": 250, "10": 250},
    ]
    shots = sum(hists[0].values())

    expval_map = get_pauli_expval_map(groups, hists, shots)
    print(expval_map)


def test_get_op_vals():
    obs = [
        SparsePauliOp.from_list([("II", 0.5), ("ZZ", 0.3)]),
        SparsePauliOp.from_list([("XX", 0.4)]),
    ]
    # 与 get_op_val 的查表方式一致，用 Pauli 对象作为键。
    expval_map = {Pauli("II"): 1.0, Pauli("ZZ"): 0.6, Pauli("XX"): 0.0}

    res = get_op_vals(obs, expval_map)
    print(res)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_get_op"):
            fn()
            print(f"PASS {name}")
