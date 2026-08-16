import sys
from pathlib import Path
import json


from qiskit_algorithms.optimizers import SPSA, DIRECT_L


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from optimize_pipeline import optimize_pipeline
from save_aer_spectrum import END


TARGET_QUBITS = [125, 126, 127, 128, 129, 142, 141, 140, 139, 138]


quark_optimizer = SPSA(
    maxiter=500,
    blocking=True,
    trust_region=True,
    resamplings=1,
)

chip_options = {
    "name": "垃圾量子计算机",
    "shot_num": 1024 * 10,
    "target_qubits": TARGET_QUBITS,
}

if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "data"
    with open(out / "aer_dic.json") as f:
        aer_dic = json.load(f)
    t0 = [aer_dic[k]["res"]["t"] for k in aer_dic]  # the key will be str
    quark_dic = optimize_pipeline(
        END,
        discrete_vars=None,
        t0=t0,
        optimizer=quark_optimizer,
        chip="Baihua",
        chip_options=chip_options,
        robust=False,
        robust_options=None,
        progress=True,
    )

    with open(out / "quark_dic.json", "w") as f:
        json.dump(quark_dic, f, indent=2)
