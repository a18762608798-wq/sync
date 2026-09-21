import itertools
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from qiskit_algorithms.optimizers import DIRECT_L, SLSQP, SPSA
from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from var_optimization import outer_optimize


def _serialize_t0_map(t0_map):
    """{(order, step, phase_idx): 向量} -> {"o,s,p": list}，便于 npz 保存."""
    return {f"{o},{s},{p}": list(v) for (o, s, p), v in t0_map.items()}


def _deserialize_t0_map(rec):
    """{"o,s,p": list} -> {(order, step, phase_idx): ndarray}."""
    return {tuple(map(int, k.split(","))): np.asarray(v) for k, v in rec.items()}


def _serialize_history_map(history_map):
    """{(order, step, phase_idx): [{t, fun}]} -> {"o,s,p": [{t: list, fun: float}]}."""
    return {
        f"{o},{s},{p}": [
            {"t": np.asarray(rec["t"]).tolist(), "fun": float(rec["fun"])}
            for rec in records
        ]
        for (o, s, p), records in history_map.items()
    }


target_qubits = [138, 125, 126, 127, 128, 129, 142, 141]


def _run_one(s, chip, t0=None, optimizer=None):
    (
        best_step,
        best_order,
        best_phase_idx,
        best_result,
        t0_map,
        history_map,
    ) = outer_optimize(
        8,
        s,
        0.3,
        max_steps=[3, 2],
        orders=[1, 2],
        t0=t0,
        optimizer=optimizer,
        chip_options={
            "name": f"s={s}",
            "shot_num": 1024 * 4,
            "target_qubits": target_qubits,
        },
        chip=chip,
        disp=False,
    )
    return best_step, best_order, best_phase_idx, best_result.fun, t0_map, history_map


def _wrapper(args):
    return _run_one(*args)


def save_qc_spectrum(
    path, processes=8, chip="qiskit_aer", t0_maps=None, optimizer=None
):
    """t0_maps: list, 与 slist 对齐, 每项是上一阶段输出的 t0_map (或 None 用默认).
    同时保存每段的 t0_map 与 history."""
    slist = np.arange(0.1, 0.9 + 1e-6, 0.1125)
    chip_list = [chip] * len(slist)
    if t0_maps is None:
        t0_maps = [None] * len(slist)
    if optimizer is None:
        optimizer = SLSQP(maxiter=1000, ftol=1e-6, disp=False)

    with Pool(processes=processes) as pool:
        results = list(
            tqdm(
                pool.imap(
                    _wrapper,
                    zip(
                        slist,
                        chip_list,
                        t0_maps,
                        itertools.repeat(optimizer),
                    ),
                ),
                total=len(slist),
                desc="s 扫描",
            )
        )

    steps = [o[0] for o in results]
    orders = [o[1] for o in results]
    pidxs = [o[2] for o in results]
    vals = [o[3] for o in results]
    out_t0_maps = [_serialize_t0_map(o[4]) for o in results]
    out_history_maps = [_serialize_history_map(o[5]) for o in results]

    np.savez(
        path,
        slist=slist,
        steps=steps,
        orders=orders,
        pidxs=pidxs,
        vals=vals,
        t0_maps=np.asarray(out_t0_maps, dtype=object),
        history_maps=np.asarray(out_history_maps, dtype=object),
    )


def load_t0_maps(path):
    """从某阶段结果 npz 读取 t0_maps, 供下一阶段作初值."""
    with np.load(path, allow_pickle=True) as data:
        return [_deserialize_t0_map(rec) for rec in data["t0_maps"]]


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    direct_path = HERE / "./data/aer_qc_spectrum_direct.npz"
    aer_path = HERE / "./data/aer_qc_spectrum.npz"
    quark_path = HERE / "./data/quark_qc_spectrum.npz"

    # 阶段1: 模拟机 DIRECT_L 全局优化, 得到全局初值 t0_map 与 history
    direct_optimizer = DIRECT_L(max_evals=2000)
    save_qc_spectrum(direct_path, chip="qiskit_aer", optimizer=direct_optimizer)

    # 阶段2: 模拟机 SLSQP 以 DIRECT_L 结果为初值精修, 覆盖 t0_map/history
    aer_optimizer = SLSQP(maxiter=10000, ftol=1e-10, disp=False)
    direct_t0_maps = load_t0_maps(direct_path)
    save_qc_spectrum(
        aer_path, chip="qiskit_aer", t0_maps=direct_t0_maps, optimizer=aer_optimizer
    )

    # 阶段3: 真机 SPSA 以模拟机 SLSQP 结果为初值微调
    quark_optimizer = SPSA(maxiter=500, blocking=True, trust_region=True, resamplings=1)
    sim_t0_maps = load_t0_maps(aer_path)
    save_qc_spectrum(
        quark_path,
        chip="Baihua",
        t0_maps=sim_t0_maps,
        optimizer=quark_optimizer,
    )
