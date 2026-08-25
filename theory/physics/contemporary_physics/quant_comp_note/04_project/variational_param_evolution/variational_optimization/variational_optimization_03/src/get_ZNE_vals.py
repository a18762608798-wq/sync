from get_initial_state import get_initial_state
from get_evolution_qc import get_evolution_qc
from get_op import get_ssh_constrained_H
from get_cost_val import get_cost_val


TARGET_QUBITS = [126, 127, 128, 129, 142, 141, 140, 139]

N_LIST = list(range(16))


def get_ZNE_val(s, n, θodd, θeven, chip="qiskit_aer", chip_options=None):
    initial_state = get_initial_state()
    evolution_qc = get_evolution_qc(initial_state, θodd, θeven, n=n)
    cost_op = get_ssh_constrained_H(s)
    cost_val = get_cost_val(evolution_qc, cost_op, chip=chip, chip_options=chip_options)
    return float(cost_val)


def get_ZNE_vals(s, n_list, θodd, θeven, chip="qiskit_aer", chip_options=None):
    op_vals = []
    m_ls = []
    for n in n_list:
        m = 2 * n + 1
        op_vals.append(
            get_ZNE_val(s, n, θodd, θeven, chip=chip, chip_options=chip_options)
        )
        m_ls.append(m)
    return m_ls, op_vals
