from qiskit_aer.primitives import EstimatorV2


def get_cost_vals(evolution_qc, cost_op):
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
