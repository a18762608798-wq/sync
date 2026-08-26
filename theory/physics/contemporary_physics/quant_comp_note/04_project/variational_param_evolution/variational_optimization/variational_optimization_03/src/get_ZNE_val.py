import asyncio

from get_initial_state import get_initial_state
from get_evolution_qc import get_evolution_qc
from get_op import get_ssh_constrained_H
from get_cost_val import get_cost_val_async
from optimize_branch import optimize_branch


TARGET_QUBITS = [126, 127, 128, 129, 142, 141, 140, 139]

N_LIST = list(range(16))


async def get_ZNE_val(s, n, θodd, θeven, chip="qiskit_aer", chip_options=None):
    initial_state = get_initial_state()
    evolution_qc = get_evolution_qc(initial_state, θodd, θeven, n=n)
    cost_op = get_ssh_constrained_H(s)
    opts = None
    if chip_options is not None:
        opts = dict(chip_options)
        opts["name"] = f"{opts.get('name', 'my_job')}_n{n}"
    cost_val = await get_cost_val_async(
        evolution_qc, cost_op, chip=chip, chip_options=opts
    )
    return float(cost_val)


async def get_ZNE_vals(s, n_list, θodd, θeven, chip="qiskit_aer", chip_options=None):
    vals = await asyncio.gather(
        *(
            get_ZNE_val(s, n, θodd, θeven, chip=chip, chip_options=chip_options)
            for n in n_list
        )
    )
    m_ls = [2 * n + 1 for n in n_list]
    return m_ls, list(vals)


async def get_gs_ZNE(
    s, direct_optimizer, slsqp_optimizer, n_list, chip="qiskit_aer", chip_options=None
):
    # optimize and get the params
    initial_state = get_initial_state()
    direct_res = optimize_branch(initial_state, s=s, optimizer=direct_optimizer)
    slsqp_res = optimize_branch(
        initial_state, t0=direct_res["t"], s=s, optimizer=slsqp_optimizer
    )
    # get ZNE
    θodd, θeven = slsqp_res["t"]
    m_ls, op_vals = await get_ZNE_vals(
        s, n_list, θodd, θeven, chip=chip, chip_options=chip_options
    )
    record = {
        "s": s,
        "chip": chip,
        "m": m_ls,
        "vals": op_vals,
        "slsqp_res": slsqp_res,
    }
    return record


async def get_bell_ZNE(s, n_list, chip="qiskit_aer", chip_options=None):
    # get ZNE
    θodd, θeven = 5.1e-4, 5.1e-4
    m_ls, op_vals = await get_ZNE_vals(
        s, n_list, θodd, θeven, chip=chip, chip_options=chip_options
    )
    record = {"s": s, "chip": chip, "m": m_ls, "vals": op_vals}
    return record
