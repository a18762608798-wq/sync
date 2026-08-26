import asyncio
import json
import sys
from pathlib import Path


import numpy as np
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
TARGET_QUBITS = [126, 127, 128, 129, 142, 141, 140, 139]
IDEAL_BELL_VAL = -12.0
SLIST = np.linspace(0, 1, 20)
NLIST = list(range(5))

from get_rZNE_spectrum import get_rZNE_spectrum


def _dump(record, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {out_path}")


async def save_rZNE_spectrum(out_path, chip="qiskit_aer"):
    direct_optimizer = DIRECT_L(
        max_evals=500,
    )
    slsqp_optimizer = SLSQP(
        maxiter=1000,
        ftol=1e-12,
        disp=False,
    )
    chip_options = {
        "shot_num": 1024 * 50,
        "correct": False,
        "name": "Save-rZNE-spectrum",
        "target_qubits": TARGET_QUBITS,
    }
    gs_rzne, bell_rzne = await get_rZNE_spectrum(
        s_ls=SLIST,
        direct_optimizer=direct_optimizer,
        slsqp_optimizer=slsqp_optimizer,
        n_list=NLIST,
        ideal_bell_val=IDEAL_BELL_VAL,
        chip=chip,
        chip_options=chip_options,
    )
    record = {
        "gs": gs_rzne,
        "bell": bell_rzne,
    }
    _dump(record, out_path)


if __name__ == "__main__":
    asyncio.run(
        save_rZNE_spectrum(
            HERE / "data" / "rZNE_spectrum.json",
            chip="Baihua",
        )
    )
