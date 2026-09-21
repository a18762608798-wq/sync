import asyncio

import numpy as np
from qiskit import transpile
from qiskit_aer.primitives import EstimatorV2
from qmeas.estimator import EstimatorConfig, QuarkEstimatorOptions, run_estimator

QUARK_CHIP = ["Baihua", "Dongling", "Shenglian"]
QUBITNUM = 8
COUPLING_MAP = [pair for i in range(QUBITNUM - 1) for pair in [[i, i + 1], [i + 1, i]]]


def get_cost_val(evolution_qc, cost_op, *, chip="qiskit_aer", chip_options=None):
    if chip == "qiskit_aer":
        return get_cost_val_by_qiskit_aer(evolution_qc, cost_op)
    elif chip in QUARK_CHIP:
        return asyncio.run(
            get_cost_val_async(
                evolution_qc, cost_op, chip=chip, chip_options=chip_options
            )
        )
    else:
        raise (ValueError("The chip must be qiskit_aer or in QUARK_CHIP."))


async def get_cost_val_async(
    evolution_qc, cost_op, *, chip="qiskit_aer", chip_options=None
):
    if chip == "qiskit_aer":
        return await asyncio.to_thread(
            get_cost_val_by_qiskit_aer, evolution_qc, cost_op
        )
    elif chip in QUARK_CHIP:
        config = _build_quark_config(evolution_qc, cost_op, chip, chip_options)
        result = await run_estimator(config)
        return np.real(result["evs"][0])
    else:
        raise (ValueError("The chip must be qiskit_aer or in QUARK_CHIP."))


def _build_quark_config(evolution_qc, cost_op, chip, chip_options):
    chip_options = {} if chip_options is None else chip_options
    correct = chip_options.get("correct", True)
    target_qubits = chip_options.get("target_qubits", [])
    name = chip_options.get("name", "my_job")
    shot_num = chip_options.get("shot_num", 1024)
    token = chip_options.get("token", None)
    return EstimatorConfig(
        qc=evolution_qc,
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


def get_cost_val_by_qiskit_aer(evolution_qc, cost_op):
    pub = (
        transpile(evolution_qc, basis_gates=["cz", "u3"]),
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
