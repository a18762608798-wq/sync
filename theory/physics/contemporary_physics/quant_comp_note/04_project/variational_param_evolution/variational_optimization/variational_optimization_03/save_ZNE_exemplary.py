import sys
from pathlib import Path
import json
import asyncio
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

DATA_DIR = HERE / "data"


TARGET_QUBITS = [126, 127, 128, 129, 142, 141, 140, 139]
NLIST = list(range(5))


from get_ZNE_val import get_gs_ZNE, get_bell_ZNE


def _dump(record, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {out_path}")


async def save_gs_ZNE_exemplary(s, chip="qiskit_aer", chip_options=None, out_path=None):
    direct_optimizer = DIRECT_L(
        max_evals=500,
    )
    slsqp_optimizer = SLSQP(
        maxiter=1000,
        ftol=1e-12,
        disp=False,
    )
    opts = None
    if chip_options is not None:
        opts = dict(chip_options)
        opts["name"] = f"gs_{opts.get('name', 'my_job')}"
    record = await get_gs_ZNE(
        s,
        direct_optimizer,
        slsqp_optimizer,
        NLIST,
        chip=chip,
        chip_options=opts,
    )
    _dump(record, out_path)


async def save_bell_ZNE_exemplary(
    s, chip="qiskit_aer", chip_options=None, out_path=None
):
    opts = None
    if chip_options is not None:
        opts = dict(chip_options)
        opts["name"] = f"bell_{opts.get('name', 'my_job')}"
    record = await get_bell_ZNE(s, NLIST, chip=chip, chip_options=opts)
    _dump(record, out_path)


async def main():
    s = 1
    chip_options = {
        "shot_num": 1024 * 50,
        "correct": False,
        "name": f"s = {s}",
        "target_qubits": TARGET_QUBITS,
    }
    await asyncio.gather(
        save_gs_ZNE_exemplary(
            s,
            chip="Baihua",
            chip_options=chip_options,
            out_path=DATA_DIR / "ZNE_exemplary.json",
        ),
        save_bell_ZNE_exemplary(
            s,
            chip="Baihua",
            chip_options=chip_options,
            out_path=DATA_DIR / "bell_ZNE_exemplary.json",
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
