import sys
from pathlib import Path
import json


from qiskit_algorithms.optimizers import SPSA, DIRECT_L


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from optimize_pipeline import optimize_pipeline


END = [0.25, 0.3]


direct_optimizer = DIRECT_L(
    max_evals=500,
)

aer_optimizer = SPSA(
    maxiter=100,
    blocking=True,
    trust_region=True,
    resamplings=1,
)


if __name__ == "__main__":
    # Direct_L
    direct_dic = optimize_pipeline(
        END,
        discrete_vars=None,
        t0=None,
        optimizer=direct_optimizer,
        chip="qiskit_aer",
        chip_options=None,
        progress=True,
    )
    out = Path(__file__).resolve().parent / "data"
    with open(out / "direct_dic.json", "w") as f:
        json.dump(direct_dic, f, indent=2)

    # Aer
    t0 = [direct_dic[i]["res"]["t"] for i in range(len(direct_dic))]
    aer_dic = optimize_pipeline(
        END,
        discrete_vars=None,
        t0=t0,
        optimizer=aer_optimizer,
        chip="qiskit_aer",
        chip_options=None,
        progress=True,
    )

    with open(out / "aer_dic.json", "w") as f:
        json.dump(aer_dic, f, indent=2)
