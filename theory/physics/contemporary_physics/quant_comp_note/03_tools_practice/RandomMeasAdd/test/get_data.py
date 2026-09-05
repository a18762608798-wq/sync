import asyncio
from pathlib import Path


from qmeas.random import (
    AerOptions,
    RandomMeasConfig,
    SettingRun,
    run_random,
)

from qmeas.models.xxz import get_initial_state

HERE = Path(__file__).resolve().parent

# 两种测量方案：independent 每个比特独立幺正，shared 组内共享旋转参数。
# NOTE: independent 没有顺序要求, 但是建议考虑zr等结构奇偶绑定.
schemes = {
    "independent": [(2,), (5,), (3,), (4,)],
    "shared": [(2, 5), (3, 4)],
}

setting_runs = [
    SettingRun(num_settings=3**5, num_shots=1024),
    SettingRun(num_settings=3**6, num_shots=1024),
]
aer_opts = AerOptions(
    method="matrix_product_state", device="CPU", precision="single", mitigation=True
)

for scheme_name, meas_indices in schemes.items():
    for pidx in (1, 0, -1):
        qc = get_initial_state(8, pidx=pidx)
        name = f"aer_{scheme_name}_pidx_{pidx}"
        meas_config = RandomMeasConfig(
            qc=qc,
            setting_runs=setting_runs,
            meas_indices=meas_indices,
            ensemble="haar",
            runner_opts=aer_opts,
            seed=521,
            output_dir=HERE / "data" / name,
            name=name,
        )
        asyncio.run(run_random(config=meas_config))
        print(f"done: {name}")
