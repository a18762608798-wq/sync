import numpy as np
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import PauliList, Pauli, SparsePauliOp
from qiskit.circuit import ParameterVector


PAULI_ROTATIONS = np.array(
    [
        [np.pi / 2, 0],
        [np.pi / 2, np.pi / 2],
        [0, 0],
    ],
    dtype=float,
)


# get the pauli list form obs
def get_pauli_list_from_obs(obs):
    pauli_list = {
        label
        for ob in obs
        for label in ob.paulis.to_labels()  # 它把Qiskit 内部的 PauliList 转成普通字符串列表。
    }

    pauli_list = PauliList(sorted(pauli_list))  # 重新转换成 Qiskit 的 PauliList 对象

    return pauli_list


# 给电路加测量门.
def add_meas(qc, meas_indices=None):
    if meas_indices == None:
        meas_indices = range(qc.num_qubits)
    num_clbits = len(meas_indices)
    theta = ParameterVector("θ", num_clbits)
    phi = ParameterVector("phi", num_clbits)
    for meas_idx in meas_indices:
        qc.u(-theta[meas_idx], 0, -phi[meas_idx], meas_idx)
    qc.measure(meas_indices, range(len(meas_indices)))
    return qc, theta, phi


# 获得测量参数
def get_meas_params(pauli_list, theta, phi):
    assert len(pauli_list[0]) == len(theta) and len(theta) == len(phi), (
        "the length of pauli op and params must be equal."
    )
    theta_vals, phi_vals = _get_params_arr(pauli_list)
    return _get_params_bind(theta, phi, theta_vals, phi_vals)


# 根据测量算符设置参数
def _get_params_arr(pauli_list):
    pauli_num = len(pauli_list)
    pauli_len = len(pauli_list[0])
    theta_vals = np.zeros((pauli_len, pauli_num))
    phi_vals = np.zeros((pauli_len, pauli_num))
    for pauli_idx, pauli in enumerate(pauli_list):
        for base_idx, base in enumerate(pauli):
            if base == Pauli("X"):
                theta_vals[base_idx, pauli_idx] = PAULI_ROTATIONS[0, 0]
                phi_vals[base_idx, pauli_idx] = PAULI_ROTATIONS[0, 1]
            elif base == Pauli("Y"):
                theta_vals[base_idx, pauli_idx] = PAULI_ROTATIONS[1, 0]
                phi_vals[base_idx, pauli_idx] = PAULI_ROTATIONS[1, 1]
            else:
                theta_vals[base_idx, pauli_idx] = PAULI_ROTATIONS[2, 0]
                phi_vals[base_idx, pauli_idx] = PAULI_ROTATIONS[2, 1]

    return theta_vals, phi_vals


# 整理参数bind格式
def _get_params_bind(theta, phi, theta_vals, phi_vals):
    pauli_len, _ = np.shape(theta_vals)
    binds = {theta[i]: theta_vals[i, :].tolist() for i in range(pauli_len)}
    binds.update({phi[i]: phi_vals[i, :].tolist() for i in range(pauli_len)})
    return binds
