"""exp07 T001 Qiskit 电路构造器：复用 exp06 构造器并分支化（p=2 三分支）。

对应表（Exp04.jl run_exp04_global.jl → 本模块）：
- theta_leg[point, leg, p, params]：point=s_idx-1（1..99），leg=a-1（1=triv/2=topo/3=AFM），
  p=1..3 → 本实验固定 p=2（索引 1），单层 8 参数（δ≠0），两层共 16 参数，尾部 NaN-pad 忽略。
- conv/stagn[point, leg, p]：同点同分支 p=2 两者皆假 → 该点判 invalid（spec PRE-002），不另做优化。
- build_init/build_ansatz/build_estimator_circuit/build_calib_circuits：直接复用
  exp06_circuits（初态/轨道/键酉/RXX→RYY→RZZ 顺序/L=8 约定完全一致，见其 docstring 对应表）。
- 本模块零 qmeas 依赖，单源可审计；分支参数读取只读 data/exp04/exp04_S06.npz。

a* 获胜标签仅记录不决定执行分支：三路各取各自 θ*_a（p=2）执行。
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exp06_circuits import (  # noqa: E402
    A_LABELS,
    L,
    build_ansatz,
    build_calib_circuits,
    build_estimator_circuit,
    build_init,
    orbit_params,
)

__all__ = [
    "A_LABELS",
    "L",
    "P",
    "SPARSE",
    "TAG_OF_DI",
    "build_init",
    "build_ansatz",
    "build_estimator_circuit",
    "build_calib_circuits",
    "orbit_params",
    "branch_theta",
    "branch_invalid",
    "branch_circuit",
]

P = 2
SPARSE = list(range(1, 100, 7))  # s_idx 1-based：1,8,…,99 → 15 点（与 exp06 同点）
assert len(SPARSE) == 15
TAG_OF_DI = {1: "dm2", 2: "d085"}  # di=1 → δ=-2；di=2 → δ=0.85
N_BRANCH = 3


def branch_theta(s06path: str | Path, delta_idx: int, s_idx: int,
                 branch: int) -> np.ndarray:
    """取某 (δ线, s 点, 分支) 的 p=2 θ 向量（去 NaN-pad 尾部）。

    s06path 只读 data/exp04/exp04_S06.npz；delta_idx∈{1,2}，s_idx∈1..99，branch∈{1,2,3}。
    """
    assert delta_idx in TAG_OF_DI and 1 <= int(s_idx) <= 99 and branch in (1, 2, 3)
    s06 = np.load(s06path)
    tag = TAG_OF_DI[delta_idx]
    row = np.asarray(s06[f"{tag}_theta_leg"])[int(s_idx) - 1, branch - 1, P - 1, :]
    row = row[~np.isnan(row)]
    assert len(row) >= L * P, f"θ 长度 {len(row)} < 需要 {L * P}"
    return row


def branch_invalid(s06path: str | Path, delta_idx: int, s_idx: int,
                   branch: int) -> bool:
    """该分支是否 invalid：S06 同点同分支 p=2 conv 与 stagn 皆假（spec PRE-002）。"""
    assert delta_idx in TAG_OF_DI and 1 <= int(s_idx) <= 99 and branch in (1, 2, 3)
    s06 = np.load(s06path)
    tag = TAG_OF_DI[delta_idx]
    conv = bool(np.asarray(s06[f"{tag}_conv"])[int(s_idx) - 1, branch - 1, P - 1])
    stagn = bool(np.asarray(s06[f"{tag}_stagn"])[int(s_idx) - 1, branch - 1, P - 1])
    return (not conv) and (not stagn)


def branch_circuit(s06path: str | Path, delta_idx: int, s_idx: int, branch: int,
                   delta: float):
    """该 (δ线, s 点, 分支) 的完整 estimator 电路（初态 + p=2 拟设 + 全 Z 测量）。"""
    theta = branch_theta(s06path, delta_idx, s_idx, branch)
    return build_estimator_circuit(theta, branch, P, float(delta))
