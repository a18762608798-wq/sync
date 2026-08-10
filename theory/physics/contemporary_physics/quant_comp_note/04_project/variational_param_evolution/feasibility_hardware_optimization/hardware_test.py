"""
真机 (Baihua) 与模拟机 (qiskit_aer) 效果对比测试.

Part 1: 直接用三种初始态 (phase_idx = -1, 0, 1) 测量各自分支对应的
        哈密顿量 cost_fun (含 ϵ=1 对称性保护项), 分别跑 aer 与真机.

Part 2: 先在 aer 上 DIRECT_L + SLSQP 优化出最优路径, 再用
        get_evolution_path / get_evolution_qc 重构电路, 分别在 aer 与真机
        上测量对应 cost_fun (含 ϵ=1 对称性保护项).

用法: .CondaPkg/.pixi/envs/default/bin/python feasibility_hardware_optimization/hardware_test.py            # aer + 真机
      .CondaPkg/.pixi/envs/default/bin/python feasibility_hardware_optimization/hardware_test.py aer        # 仅模拟机
      .CondaPkg/.pixi/envs/default/bin/python feasibility_hardware_optimization/hardware_test.py quark      # 仅真机
"""

import os
import sys

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from create_op import get_ssh_constrained_H
from get_cost_vals import get_cost_vals
from get_evolution_qc import get_evolution_qc
from get_evolution_path import get_evolution_path
from get_initial_state import get_initial_state
from var_optimization import _sigmoid, get_branch_start, inner_optimize, τ

QUARK_TARGET_QUBITS = [138, 125, 126, 127, 128, 129, 142, 141]
N_QUBIT = 8


def _quark_opts(name):
    return {
        "target_qubits": QUARK_TARGET_QUBITS,
        "name": name,
        "shot_num": 1024 * 4,
    }


def _measure(qc, s, δ, chip, name):
    Hc = get_ssh_constrained_H(N_QUBIT, s, δ, ϵ=1)
    opts = _quark_opts(name) if chip != "qiskit_aer" else None
    return get_cost_vals(qc, Hc, chip=chip, chip_options=opts)


def _measure_ops(qc, ops, chips, name_prefix):
    for name, (pauli, qubits) in ops.items():
        op = SparsePauliOp.from_sparse_list(
            [(pauli, qubits, 1.0)], num_qubits=qc.num_qubits
        )
        line = f"<{name}>: "
        for chip in chips:
            if chip == "qiskit_aer":
                val = get_cost_vals(qc, op, chip=chip)
            else:
                opts = {
                    "target_qubits": QUARK_TARGET_QUBITS[: qc.num_qubits],
                    "name": f"{name_prefix}_{name}",
                    "shot_num": 1024 * 4,
                }
                val = get_cost_vals(qc, op, chip=chip, chip_options=opts)
            line += f"  {chip:10s} = {val: .4f}"
        print(line)


def part0(chips):
    """Part 0: 两比特 Bell 态 |Φ+⟩ 与纯态 |00⟩, 测量 XX/YY/ZZ 等, aer 与真机对比."""
    print("=" * 60)
    print("Part 0: 两比特态测量 (aer / 真机)")
    print("=" * 60)

    bell = QuantumCircuit(2, 2)
    bell.h(0)
    bell.cx(0, 1)
    print("Bell 态 |Φ+⟩:")
    _measure_ops(
        bell,
        {
            "XX": ("XX", [0, 1]),
            "YY": ("YY", [0, 1]),
            "ZZ": ("ZZ", [0, 1]),
        },
        chips,
        "bell",
    )

    pure = QuantumCircuit(2, 2)
    print("纯态 |00⟩:")
    _measure_ops(
        pure,
        {
            "IZ": ("IZ", [0, 1]),
            "ZI": ("IZ", [0, 1]),
            "ZZ": ("ZZ", [0, 1]),
        },
        chips,
        "pure00",
    )


def part1(chips):
    """Part 1: 三种初始态在其分支对应 (s, δ) 下的 cost_fun.

    分支映射 (对应 get_branch_start 的起点):
      phase_idx =  1  -> δ≠0, s=0    -> H(s=0,   δ=1)
      phase_idx =  0  -> δ=0,  s≠±1  -> H(s=0.5, δ=0)
      phase_idx = -1  -> δ≠0, s=1    -> H(s=1,   δ=1)
    """
    print("=" * 60)
    print("Part 1: 初始态在各分支哈密顿量下的 cost_fun (ϵ=1)")
    print("=" * 60)
    cases = [
        (1, (0, 1)),
        (0, (0.5, 0)),
        (-1, (1, 1)),
    ]
    for phase_idx, (s, δ) in cases:
        qc = get_initial_state(N_QUBIT, phase_idx)
        line = f"phase_idx={phase_idx:2d}  H(s={s}, δ={δ}): "
        for chip in chips:
            evs = _measure(qc, s, δ, chip, f"hardware_part1_p{phase_idx}")
            line += f"  {chip:10s} = {evs: .8f}"
        print(line)


def _reconstruct_path(t, step, phase_idx, s1, δ1, order=1):
    """把优化得到的 t 向量解码回 (qc, path), 与 var_optimization.objective 一致."""
    x = _sigmoid(t)
    v0, us, uδ = x[0:3]
    Δts = τ * x[3 : 3 + step]
    Δtds = x[3 + step : 3 + 2 * step]

    start = get_branch_start(phase_idx, v0)
    sp = start[0] + us * (s1 - start[0])
    δp = start[1] + uδ * (δ1 - start[1])
    control = (sp, δp)

    initial = get_initial_state(N_QUBIT, phase_idx)
    qc, path = get_evolution_qc(
        initial, start, (s1, δ1), control, Δts, Δtds, order=order
    )
    return qc, path


def part2(chips):
    """Part 2: aer 上 DIRECT_L + SLSQP 优化最优路径, 再测 aer / 真机 cost."""
    print("=" * 60)
    print("Part 2: 优化最优路径, 重构电路测量 cost_fun (ϵ=1)")
    print("=" * 60)

    s1, δ1 = 0.5, 0.5
    step, order = 1, 1
    direct_l_optimizer = DIRECT_L(max_evals=1000)
    slsqp_optimizer = SLSQP(maxiter=500, ftol=1e-12, disp=False)

    best_phase_idx, _, t0_map, _ = inner_optimize(
        N_QUBIT,
        s1,
        δ1,
        step=step,
        order=order,
        optimizer=direct_l_optimizer,
        chip="qiskit_aer",
        disp=True,
    )
    best_phase_idx, best_result, t0_map, _ = inner_optimize(
        N_QUBIT,
        s1,
        δ1,
        step=step,
        order=order,
        t0=t0_map,
        optimizer=slsqp_optimizer,
        chip="qiskit_aer",
        disp=True,
    )

    t = t0_map[best_phase_idx]
    qc, path = _reconstruct_path(t, step, best_phase_idx, s1, δ1, order)

    print(f"最优分支 phase_idx={best_phase_idx}, t = {np.round(t, 4)}")
    print(f"路径点: {[(round(s, 4), round(d, 4)) for s, d in path]}")

    for chip in chips:
        evs = _measure(qc, s1, δ1, chip, "hardware_part2_opt")
        print(f"优化路径 cost_fun ({chip:10s}) = {evs: .8f}")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "aer":
        chips = ["qiskit_aer"]
    elif arg == "quark":
        chips = ["Baihua"]
    else:
        chips = ["qiskit_aer", "Baihua"]

    part0(chips)
    part1(chips)
    part2(chips)
