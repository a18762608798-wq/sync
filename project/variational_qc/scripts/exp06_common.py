"""exp06 共享常量与落盘 helpers（零真机调用）。v2 新协议。"""

from __future__ import annotations

import json
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "exp06"
PILOT_DIR = Path(__file__).resolve().parent.parent / "data" / "exp06_pilot"
FIGS_DIR = Path(__file__).resolve().parent.parent / "figs" / "exp06"

MASTER_SEED = 20261004
SHOTS = 1024
P_LEVEL = 1
SPARSE = list(range(1, 100, 7))  # s_idx 1-based：1,8,…,99 → 15 点
assert len(SPARSE) == 15
N_POINTS = 15
ROUND_UNITS = 1000
CAP_UNITS = 5000
PILOT_UNITS = 50
UNIT_CIRCUITS = N_POINTS + 2  # 15 点 VQE + 2 标定
# 判据（spec POST-002/Q7/Q8/Q9）：d 在 [-1,1] 归一化后计。
CRITERIA = {"v2.0": (0.30, 0.4), "v2.1": (0.40, 0.4), "v2.2": (0.50, 0.4),
            "v3.0-d085": (0.08, 0.9)}
CRITERION_FINAL = "v2.2"
DEFAULT_CRITERION = {"dm2": "v2.0", "d085": "v3.0-d085"}
FIXED_WINDOW_LEN = {"dm2": 20, "d085": 20}
D_THRESH, R_THRESH = CRITERIA["v2.0"]
CRITERION_VERSION = "v2.0"
MIN_WINDOW = 10
LINE_IDS = {"dm2": 1, "d085": 2}
LINE_OF_ID = {1: "dm2", 2: "d085"}
D08_OF_LINE = {"dm2": "D08a", "d085": "D08b"}

# v3 联测（Q12）：两线同窗口 30 点/单位。
JOINT_LINE = "joint"
JOINT_N_POINTS = 30
JOINT_UNIT_CIRCUITS = JOINT_N_POINTS + 2  # 30 点 VQE + 2 标定
V3_ROUND_UNITS = 500
EVEN_LEN_MIN = 10  # 展示窗口偶数长度下限


def root_of(pilot: bool) -> Path:
    return PILOT_DIR if pilot else DATA_DIR


def line_dir(line: str, pilot: bool = False) -> Path:
    return root_of(pilot) / line


def unit_state_path(line: str, uid: int, pilot: bool = False) -> Path:
    return line_dir(line, pilot) / "units" / f"{uid:05d}" / "state.json"


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    # Windows：目标被读句柄/索引器占用时 os.replace 会 PermissionError，重试。
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
