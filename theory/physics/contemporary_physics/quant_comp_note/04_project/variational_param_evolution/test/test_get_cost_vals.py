import os
import sys
import math

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "variational_fidelity")
)

from get_cost_vals import get_cost_vals
from get_evolution_qc import get_evolution_qc
from get_initial_state import get_initial_state
from create_op import get_ssh_constrained_H


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
    evs = get_cost_vals(qc, Hc)
    assert isinstance(evs, np.ndarray)
    print(evs)


def test_output_val():
    qc = get_initial_state(8, -1)
    Hc = get_ssh_constrained_H(8, 1, 1, ϵ=1)
    evs = get_cost_vals(qc, Hc)
    print(evs)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
