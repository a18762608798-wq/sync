import sys
from pathlib import Path


from qiskit_algorithms.optimizers import SPSA, SLSQP, DIRECT_L


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


from optimize_pipeline import optimize_pipeline

direct_optimizer = DIRECT_L(
    max_evals=10000,
)
spsa_optimizer = SPSA(
    maxiter=500,
    blocking=True,
    trust_region=True,
    resamplings=1,
)

if __name__ == "__main__":
    end = [0.5, 0.5]

    res = optimize_pipeline(
        end,
        discrete_vars=None,
        t0=None,
        optimizer=direct_optimizer,
        chip="qiskit_aer",
        chip_options=None,
        robust=False,
        robust_options=None,
        progress=True,
    )
