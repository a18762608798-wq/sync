import asyncio
import os
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit

from qmeas.random import (
    AerOptions,
    QuarkOptions,
    RandomMeasConfig,
    SettingRun,
    run_random,
)

test_idx = 1

if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    setting_num = 2
    shot_num = 1024
    qc = QuantumCircuit(6, 4)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(3, 4)

    if test_idx == 1:
        config = RandomMeasConfig(
            qc=qc,
            setting_runs=[
                SettingRun(setting_num, shot_num),
                SettingRun(setting_num + 1, shot_num * 2),
            ],
            meas_indices=[(0,), (5,), (1,), (4,)],
            ensemble="pauli",
            seed=1,
            runner_opts=AerOptions(method="density_matrix"),
            output_dir=HERE / "data",
            name="my_job",
        )
        result = asyncio.run(run_random(config))

    elif test_idx == 2:
        config = RandomMeasConfig(
            qc=qc,
            setting_runs=[SettingRun(setting_num, shot_num)],
            meas_indices=[(0, 5), (1, 4)],
            ensemble="haar",
            runner_opts=AerOptions(),
            output_dir=HERE / "data",
            name="my_job",
        )

    elif test_idx == 3:
        config = RandomMeasConfig(
            qc=qc,
            setting_runs=[SettingRun(setting_num, shot_num)],
            meas_indices=[(0, 5), (1, 4)],
            ensemble="pauli",
            runner_opts=QuarkOptions(
                chip="Dongling",
                token=os.environ["QUARK_TOKEN"],
            ),
            output_dir=HERE / "data",
            name="my_job",
        )

    elif test_idx == 4:
        config = RandomMeasConfig(
            qc=qc,
            setting_runs=[SettingRun(setting_num, shot_num)],
            meas_indices=[(0, 5), (1, 4)],
            ensemble="haar",
            runner_opts=QuarkOptions(
                chip="Dongling",
                token=os.environ["QUARK_TOKEN"],
                correction=True,
            ),
            output_dir=HERE / "data",
            name="my_job",
        )

    result = asyncio.run(run_random(config))
    print(result)
    for npz_name in result["npz_files"]:
        data = np.load(HERE / "data" / npz_name)
        print(
            npz_name,
            "results:",
            data["measurement_results"].shape,
            "settings:",
            data["measurement_settings"].shape,
        )
