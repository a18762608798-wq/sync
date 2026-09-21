import asyncio
import sys
from pathlib import Path

from qiskit_algorithms.optimizers import DIRECT_L, SLSQP

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from get_rZNE_spectrum import get_rZNE_spectrum


def main():
    direct_optimizer = DIRECT_L(max_evals=500)
    slsqp_optimizer = SLSQP(maxiter=5000, ftol=1e-12, disp=False)

    gs_rzne, bell_rzne = asyncio.run(
        get_rZNE_spectrum(
            s_ls=[0.5, 1],
            direct_optimizer=direct_optimizer,
            slsqp_optimizer=slsqp_optimizer,
            n_list=[0, 1, 2],
        )
    )
    print("gs_rzne:", gs_rzne)
    print("bell_rzne:", bell_rzne)


if __name__ == "__main__":
    main()
