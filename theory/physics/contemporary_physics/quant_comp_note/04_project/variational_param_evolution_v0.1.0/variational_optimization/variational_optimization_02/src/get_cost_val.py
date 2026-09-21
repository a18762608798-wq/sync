import asyncio

import numpy as np
from qiskit_aer.primitives import EstimatorV2
from qmeas.estimator import EstimatorConfig, QuarkEstimatorOptions, run_estimator

QUARK_CHIP = ["Baihua", "Dongling", "Shenglian"]
LOOPNUM = 10
QUBITNUM = 8
COUPLING_MAP = [pair for i in range(LOOPNUM - 1) for pair in [[i, i + 1], [i + 1, i]]]
COUPLING_MAP.append([0, LOOPNUM - 1])
COUPLING_MAP.append([LOOPNUM - 1, 0])


def get_cost_val(evolution_qc, cost_op, *, chip="qiskit_aer", chip_options=None):
    if chip == "qiskit_aer":
        return get_cost_val_by_qiskit_aer(evolution_qc, cost_op)
    elif chip in QUARK_CHIP:
        chip_options = {} if chip_options is None else chip_options
        correct = chip_options.get("correct", True)
        target_qubits = chip_options.get("target_qubits", [])
        name = chip_options.get("name", "my_job")
        shot_num = chip_options.get("shot_num", 1024)
        token = chip_options.get("token", None)
        return get_cost_val_by_quark(
            evolution_qc,
            cost_op,
            chip=chip,
            correct=correct,
            target_qubits=target_qubits,
            name=name,
            shot_num=shot_num,
            token=token,
        )
    else:
        raise (ValueError("The chip must be qiskit_aer or in QUARK_CHIP."))


def get_cost_val_by_qiskit_aer(evolution_qc, cost_op):
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


def get_cost_val_by_quark(
    evolution_qc,
    cost_op,
    chip="Baihua",
    correct=True,
    target_qubits=None,
    name="my_job",
    shot_num=1024,
    token=None,
):

    config = EstimatorConfig(
        qc=evolution_qc.decompose(),
        observables=[cost_op],
        runner_opts=QuarkEstimatorOptions(
            token=token,
            chip=chip,
            shots=shot_num,
            name=name,
            compiler="qiskit",
            correct=correct,
            target_qubits=target_qubits or [],
            coupling_map=COUPLING_MAP,
        ),
    )
    result = asyncio.run(run_estimator(config))
    cost_val = np.real(result["evs"][0])
    return cost_val
