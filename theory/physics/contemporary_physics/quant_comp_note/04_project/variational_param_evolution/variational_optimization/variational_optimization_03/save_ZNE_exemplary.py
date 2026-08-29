import sys
from pathlib import Path
import json
import asyncio
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

DATA_DIR = HERE / "data"


SHENGLIAN_TARGET_QUBITS = [67, 61, 68, 62, 69, 76, 82, 75]
BAIHUA_TARGET_QUBITS = [13, 14, 15, 16, 17, 30, 29, 28]
SHENGLIAN_NLIST = list(range(3))
BAIHUA_NLIST = list(range(4))

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


from get_ZNE_val import get_gs_ZNE, get_bell_ZNE


def _dump(record, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {out_path}")


async def save_gs_ZNE_exemplary(
    s, nlist, chip="qiskit_aer", chip_options=None, out_path=None
):
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
        nlist,
        chip=chip,
        chip_options=opts,
    )
    _dump(record, out_path)


async def save_bell_ZNE_exemplary(
    s, nlist, chip="qiskit_aer", chip_options=None, out_path=None
):
    opts = None
    if chip_options is not None:
        opts = dict(chip_options)
        opts["name"] = f"bell_{opts.get('name', 'my_job')}"
    record = await get_bell_ZNE(s, nlist, chip=chip, chip_options=opts)
    _dump(record, out_path)


async def save_exemplary(chip):
    s = 1
    if chip in CHIP_CONFIGS:
        cfg = CHIP_CONFIGS[chip]
        nlist = cfg["nlist"]
        chip_options = {
            "shot_num": 1024 * 20,
            "correct": True,
            "name": f"s = {s}",
            "target_qubits": cfg["target_qubits"],
        }
    elif chip == "qiskit_aer":
        nlist = AER_NLIST
        chip_options = None
    else:
        raise ValueError(
            f"Unknown chip: {chip}. Must be one of {list(CHIP_CONFIGS)} or 'qiskit_aer'."
        )
    out_dir = DATA_DIR / chip
    await asyncio.gather(
        save_gs_ZNE_exemplary(
            s,
            nlist,
            chip=chip,
            chip_options=chip_options,
            out_path=out_dir / "ZNE_exemplary.json",
        ),
        save_bell_ZNE_exemplary(
            s,
            nlist,
            chip=chip,
            chip_options=chip_options,
            out_path=out_dir / "bell_ZNE_exemplary.json",
        ),
    )


async def main():
    await asyncio.gather(
        save_exemplary("Shenglian"),
        save_exemplary("Baihua"),
    )


if __name__ == "__main__":
    asyncio.run(main())
