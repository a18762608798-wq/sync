import asyncio
import os
from pathlib import Path

from qiskit import QuantumCircuit

from qmeas.random import (
    AerOptions,
    CorrectionInput,
    QuarkOptions,
    RandomMeasConfig,
    SettingRun,
    run_random,
)

test_idx = 4

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
            setting_runs=[SettingRun(setting_num, shot_num)],
            meas_indices=[(0,), (5,), (1,), (4,)],
            ensemble="derandom",
            runner_opts=AerOptions(method="density_matrix"),
            output_dir=HERE / "data",
            name="my_job",
        )

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
            ensemble="derandom",
            runner_opts=QuarkOptions(
                chip="Dongling",
                token=os.environ["QUARK_TOKEN"],
                correction_input=CorrectionInput(trivial_shot_num=1024),
            ),
            output_dir=HERE / "data",
            name="my_job",
        )

    result = asyncio.run(run_random(config))
    print("counts:", result["count_group"])
    print("trivial_counts:", result.get("trivial_count_group"))
