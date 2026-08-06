from qiskit_aer.primitives import EstimatorV2

QUARK_CHIP = ["Baihua", "Dongling", "Shenglian"]


def get_cost_vals(evolution_qc, cost_op, *, chip="qiskit_aer"):
    if chip == "qiskit_aer":
        return get_cost_vals_by_qiskit_aer(evolution_qc, cost_op)
    elif chip in QUARK_CHIP:
        pass
        # return get_cost_vals_by_quark(evolution_qc, cost_op)
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
