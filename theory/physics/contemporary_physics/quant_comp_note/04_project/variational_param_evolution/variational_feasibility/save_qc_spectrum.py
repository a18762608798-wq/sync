import itertools
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from var_optimization import outer_optimize


def _serialize_x0_map(x0_map):
    """{(order, step, phase_idx): 向量} -> {"o,s,p": list}，便于 npz 保存."""
    return {f"{o},{s},{p}": list(v) for (o, s, p), v in x0_map.items()}


def _deserialize_x0_map(rec):
    """{"o,s,p": list} -> {(order, step, phase_idx): ndarray}."""
    return {tuple(map(int, k.split(","))): np.asarray(v) for k, v in rec.items()}


def _run_one(s, chip, x0=None, optimizer_options=None):
    best_step, best_order, best_phase_idx, best_result, x0_map = outer_optimize(
        8,
        s,
        0.3,
        max_steps=[3, 2],
        orders=[1, 2],
        x0=x0,
        method="COBYLA",
        optimizer_options=optimizer_options,
        chip_options={
            "name": f"s={s}",
            "shot_num": 1024 * 4,
            "target_qubits": [124, 125, 126, 127, 128, 129, 141, 142],
        },
        chip=chip,
        disp=False,
    )
    return best_step, best_order, best_phase_idx, best_result.fun, x0_map


def _wrapper(args):
    return _run_one(*args)


def save_qc_spectrum(
    path, processes=8, chip="qiskit_aer", x0_maps=None, optimizer_options=None
):
    """x0_maps: list, 与 slist 对齐, 每项是模拟机输出的 x0_map (或 None 用默认)."""
    slist = np.arange(0.1, 0.9 + 1e-6, 0.225)
    chip_list = [chip] * len(slist)
    if x0_maps is None:
        x0_maps = [None] * len(slist)
    if optimizer_options is None:
        optimizer_options = {"maxiter": 1000, "tol": 1e-6, "disp": False}

    with Pool(processes=processes) as pool:
        results = list(
            tqdm(
                pool.imap(
                    _wrapper,
                    zip(
                        slist,
                        chip_list,
                        x0_maps,
                        itertools.repeat(optimizer_options),
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
    out_x0_maps = [_serialize_x0_map(o[4]) for o in results]

    np.savez(
        path,
        slist=slist,
        steps=steps,
        orders=orders,
        pidxs=pidxs,
        vals=vals,
        x0_maps=np.asarray(out_x0_maps, dtype=object),
    )


def load_x0_maps(path):
    """从模拟机结果 npz 读取 x0_maps, 供量子计算机作初值."""
    with np.load(path, allow_pickle=True) as data:
        return [_deserialize_x0_map(rec) for rec in data["x0_maps"]]


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    aer_path = HERE / "./data/aer_qc_spectrum.npz"
    quark_path = HERE / "./data/quark_qc_spectrum.npz"

    # 模拟机先跑, 输出 x0_map
    optimizer_options = {"maxiter": 20000, "tol": 1e-4, "disp": False}
    save_qc_spectrum(aer_path, chip="qiskit_aer", optimizer_options=optimizer_options)

    # 用量子计算机跑, 以模拟机的 x0_map 作为输入初值
    optimizer_options = {"maxiter": 1000, "tol": 2e-2, "disp": False}
    sim_x0_maps = load_x0_maps(aer_path)
    save_qc_spectrum(
        quark_path,
        chip="Baihua",
        x0_maps=sim_x0_maps,
        optimizer_options=optimizer_options,
    )
