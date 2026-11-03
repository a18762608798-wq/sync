"""exp07 共享常量与落盘 helpers（零真机调用）。"""

from __future__ import annotations

import json
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "exp07"
FIGS_DIR = Path(__file__).resolve().parent.parent / "figs" / "exp07"

MASTER_SEED = 20261103
SHOTS = 1024
P_LEVEL = 2
SPARSE = list(range(1, 100, 7))  # s_idx 1-based：1,8,…,99 → 15 点（与 exp06 同点）
assert len(SPARSE) == 15
BRANCHES = (1, 2, 3)  # triv / topo / AFM，各取各自 p=2 最优参数
N_POINTS = 15 * 2 * len(BRANCHES)  # 90 点/单位
ROUND_UNITS = 500
UNIT_CIRCUITS = N_POINTS + 2  # 90 点 VQE + 2 标定
LINE = "joint"
S06_REF = "data/exp04/exp04_S06.npz"
S04_REF = "data/exp05/exp05_S04.npz"


def line_dir() -> Path:
    return DATA_DIR / "joint"


def unit_state_path(uid: int) -> Path:
    return line_dir() / "units" / f"{uid:05d}" / "state.json"


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    last: Exception | None = None
    for _ in range(20):
        try:
            tmp.replace(path)
            return
        except PermissionError as e:
            last = e
            time.sleep(0.1)
    raise last  # type: ignore[misc]


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)
