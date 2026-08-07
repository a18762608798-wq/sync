import asyncio

import numpy as np
from qiskit_aer.primitives import EstimatorV2
from submit_quark_task import submit_ops_task

QUARK_CHIP = ["Baihua", "Dongling", "Shenglian"]


def get_cost_vals(evolution_qc, cost_op, *, chip="qiskit_aer", options=None):
    if chip == "qiskit_aer":
        return get_cost_vals_by_qiskit_aer(evolution_qc, cost_op)
    elif chip in QUARK_CHIP:
        options = {} if options is None else options
        correct = options.get("correct", True)
        target_qubits = options.get("target_qubits", [])
        return get_cost_vals_by_quark(
            evolution_qc,
            cost_op,
            chip=chip,
            correct=correct,
            target_qubits=target_qubits,
        )
    else:
        raise (ValueError("The chip must be qiskit_aer or in QUARK_CHIP."))


def get_cost_vals_by_qiskit_aer(evolution_qc, cost_op):
    pub = (
        evolution_qc.decompose(),
        cost_op,
    )
    estimator = EstimatorV2(
        options={
            "backend_options": {
                "method": "matrix_product_state",
            }
        }
    )

    job = estimator.run([pub])
    result = job.result()

    return result[0].data.evs


def get_cost_vals_by_quark(
    evolution_qc, cost_op, chip="Baihua", correct=True, target_qubits=None
):
    result = asyncio.run(
        submit_ops_task(
            evolution_qc.decompose(),
            cost_op,
            chip=chip,
            correct=correct,
            target_qubits=target_qubits,
        )
    )
    cost_val = np.real(result["op_vals"][0])
    return cost_val
