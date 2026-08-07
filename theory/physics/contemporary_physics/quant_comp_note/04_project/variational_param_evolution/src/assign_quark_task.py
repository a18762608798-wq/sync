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
def get_commute_group(obs):
    # get pauli list
    pauli_list = {
        label
        for ob in obs
        for label in ob.paulis.to_labels()  # 它把Qiskit 内部的 PauliList 转成普通字符串列表。
    }

    pauli_list = PauliList(sorted(pauli_list))  # 重新转换成 Qiskit 的 PauliList 对象
    # get commute group
    meas_pauli_ls = []
    groups = pauli_list.group_commuting(qubit_wise=True)
    for group in groups:
        basis_x = np.logical_or.reduce(
            group.x,
            axis=0,
        )  # 每一个比特是否含x布尔分量
        basis_z = np.logical_or.reduce(
            group.z,
            axis=0,
        )

        measurement_basis = Pauli((basis_z, basis_x))
        meas_pauli_ls.append(measurement_basis)

    return groups, meas_pauli_ls


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
def get_meas_params(meas_pauli_ls, theta, phi):
    assert len(meas_pauli_ls[0]) == len(theta) and len(theta) == len(phi), (
        "the length of pauli op and params must be equal."
    )
    theta_vals, phi_vals = _get_params_arr(meas_pauli_ls)
    return _get_params_bind(theta, phi, theta_vals, phi_vals)


# ----------
# Helper
# ----------


# 根据测量算符设置参数
def _get_params_arr(meas_pauli_ls):
    pauli_num = len(meas_pauli_ls)
    pauli_len = len(meas_pauli_ls[0])
    theta_vals = np.zeros((pauli_len, pauli_num))
    phi_vals = np.zeros((pauli_len, pauli_num))
    for pauli_idx, pauli in enumerate(meas_pauli_ls):
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


# get paulilist masks
def _get_pauli_mask(pauli):
    support = pauli.x | pauli.z  # 非 I 的位置为 True，I 的位置为 False.

    return sum(
        int(bit) << i  # 1 << i == 2 ** i
        for i, bit in enumerate(support)
    )  # 把 support 列表转化为二进制对应的掩码数字


def _get_pauli_masks(pauli_list):
    masks = []
    for pauli in pauli_list:
        mask = _get_pauli_mask(pauli)
        masks.append(mask)
    return masks


# get pauli_list expect
def _get_pauli_list_expects(pauli_list, hist, shots):
    sums = {pauli: 0 for pauli in pauli_list}
    masks = _get_pauli_masks(pauli_list)
    for outcome, frequency in hist.items():
        outcome = int(outcome, 2)

        for pauli, mask in zip(pauli_list, masks):
            parity = (mask & outcome).bit_count() % 2
            value = -1 if parity else 1

            sums[pauli] += frequency * value
    expects = {pauli: value_sum / shots for pauli, value_sum in sums.items()}
    return expects


# get pauli expval map
def get_pauli_expval_map(groups, hists, shots):
    expval_map = {}
    for group_idx, group in enumerate(groups):
        expects = _get_pauli_list_expects(group, hists[group_idx], shots)
        expval_map.update(expects)
    return expval_map


# distribute the pauli expval back to ops
def get_op_val(ob, expval_map):
    ob_val = 0.0
    for pauli, coef in zip(
        ob.paulis,
        ob.coeffs,
    ):
        ob_val += coef * expval_map[pauli]
    return ob_val


def get_op_vals(obs, expval_map):
    if isinstance(obs, list):
        return [get_op_val(ob, expval_map) for ob in obs]
    return [get_op_val(obs, expval_map)]
