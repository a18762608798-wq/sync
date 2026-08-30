import asyncio
import json
import sys
from pathlib import Path


import numpy as np
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

SHENGLIAN_TARGET_QUBITS = [67, 61, 68, 62, 69, 76, 82, 75]
BAIHUA_TARGET_QUBITS = [13, 14, 15, 16, 17, 30, 29, 28]
SHENGLIAN_NLIST = list(range(4))
BAIHUA_NLIST = list(range(5))

CHIP_CONFIGS = {
    "Shenglian": {
        "target_qubits": SHENGLIAN_TARGET_QUBITS,
        "nlist": SHENGLIAN_NLIST,
    },
    "Baihua": {
        "target_qubits": BAIHUA_TARGET_QUBITS,
        "nlist": BAIHUA_NLIST,
    },
}

AER_NLIST = list(range(4))

SLIST = np.linspace(0.01, 1, 50)
IDEAL_BELL_VAL = -12.0

from get_rZNE_spectrum import get_rZNE_spectrum


def _dump(record, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {out_path}")


async def save_rZNE_spectrum(chip):
    if chip in CHIP_CONFIGS:
        cfg = CHIP_CONFIGS[chip]
        nlist = cfg["nlist"]
        chip_options = {
            "shot_num": 1024 * 20,
            "correct": True,
            "name": "Save-rZNE-spectrum",
            "target_qubits": cfg["target_qubits"],
        }
    elif chip == "qiskit_aer":
        nlist = AER_NLIST
        chip_options = None
    else:
        raise ValueError(
            f"Unknown chip: {chip}. Must be one of {list(CHIP_CONFIGS)} or 'qiskit_aer'."
        )
    direct_optimizer = DIRECT_L(
        max_evals=500,
    )
    slsqp_optimizer = SLSQP(
        maxiter=1000,
        ftol=1e-12,
        disp=False,
    )
    gs_rzne, bell_rzne = await get_rZNE_spectrum(
        s_ls=SLIST,
        direct_optimizer=direct_optimizer,
        slsqp_optimizer=slsqp_optimizer,
        n_list=nlist,
        ideal_bell_val=IDEAL_BELL_VAL,
        chip=chip,
        chip_options=chip_options,
    )
    record = {
        "gs": gs_rzne,
        "bell": bell_rzne,
    }
    _dump(record, HERE / "data" / chip / "rZNE_spectrum.json")


async def main():
    await asyncio.gather(
        # save_rZNE_spectrum("Shenglian"),
        save_rZNE_spectrum("Baihua"),
    )


if __name__ == "__main__":
    asyncio.run(main())
