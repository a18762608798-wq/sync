import asyncio
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

from get_rZNE_val import get_rZNE_vals


IDEAL_BELL_VAL = -12.0
IDEAL_E0_VAL = -13.49973


def save_rZNE_vals(zne_path, bell_path, zne_fitting_path, bell_fitting_path):
    with open(zne_path, encoding="utf-8") as f:
        zne = json.load(f)
    with open(bell_path, encoding="utf-8") as f:
        bell = json.load(f)

    bell_record = asyncio.run(get_rZNE_vals(bell, ideal_val=IDEAL_BELL_VAL))
    r = bell_record["r"]
    zne_record = asyncio.run(get_rZNE_vals(zne, ideal_val=IDEAL_E0_VAL, r=r))

    # save to json
    for record, path in [
        (zne_record, zne_fitting_path),
        (bell_record, bell_fitting_path),
    ]:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {path}")


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    # chip = "Shenglian"
    chip = "Shenglian"
    data_dir = HERE / "data" / chip
    save_rZNE_vals(
        data_dir / "ZNE_exemplary.json",
        data_dir / "bell_ZNE_exemplary.json",
        data_dir / "rZNE_exemplary.json",
        data_dir / "bell_rZNE_exemplary.json",
    )
    # chip = "Baihua"
    chip = "Baihua"
    data_dir = HERE / "data" / chip
    save_rZNE_vals(
        data_dir / "ZNE_exemplary.json",
        data_dir / "bell_ZNE_exemplary.json",
        data_dir / "rZNE_exemplary.json",
        data_dir / "bell_rZNE_exemplary.json",
    )
