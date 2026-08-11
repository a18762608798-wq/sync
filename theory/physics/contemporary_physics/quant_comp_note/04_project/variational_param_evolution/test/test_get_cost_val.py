import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "variational_fidelity")
)

from get_cost_val import get_cost_val
from get_evolution_qc import get_evolution_qc
from get_initial_state import get_initial_state
from create_op import get_ssh_constrained_H, get_ssh_H


def test_output_shape_and_type():
    qc, _ = get_evolution_qc(
        get_initial_state(4, 1),
        (0, 1),
        (0.1, 1),
        (0.05, 1),
        [4 for _ in range(13)],
        [0.5 for _ in range(13)],
        order=1,
    )
    Hc = get_ssh_constrained_H(4, 0.1, 1, ϵ=1)
    evs = get_cost_val(qc, Hc)
    assert isinstance(evs, np.ndarray)
    print(evs)


def test_output_val():
    qc = get_initial_state(8, 1)
    Hc = get_ssh_constrained_H(8, 1, 1, ϵ=1)
    evs = get_cost_val(qc, Hc)
    print(evs)


def test_output_val_quark():
    qc = get_initial_state(8, 1)
    Hc = get_ssh_H(8, 0, 1)
    evs0 = get_cost_val(qc, Hc, chip="qiskit_aer")
    evs1 = get_cost_val(qc, Hc, chip="Baihua")
    print(evs0, evs1)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_output_val_quark"):
            fn()
            print(f"PASS {name}")
