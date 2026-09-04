import asyncio
import os
from pathlib import Path


from qiskit import QuantumCircuit


from qmeas.random import (
    AerOptions,
    QuarkOptions,
    RandomMeasConfig,
    SettingRun,
    run_random,
)

from qmeas.models.xxz import get_initial_state

HERE = Path(__file__).resolve().parent
# aer: independence, pauli
qc = get_initial_state(8, phase_idx=1)
meas_indices = [(2,), (3,), (4,), (5,)]  # Arrange the swap bits together
setting_runs = [
    SettingRun(num_settings=3**4, num_shots=1024),
    SettingRun(num_settings=3**5, num_shots=1024),
]
aer_opts = AerOptions(method="matrix_product_state", device="CPU", precision="single")
meas_config = RandomMeasConfig(
    qc=qc,
    setting_runs=setting_runs,
    meas_indices=meas_indices,
    ensemble="haar",
    runner_opts=aer_opts,
    output_dir=HERE / "data/aer-shadow/",
    name="aer-shadow",
)
res = asyncio.run(
    run_random(
        config=meas_config,
    )
)
