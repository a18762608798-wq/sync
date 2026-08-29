from collections.abc import Callable
from dataclasses import dataclass
from itertools import product

import numpy as np
from qiskit.circuit import ParameterVector

# 旋转角 [rx 角, ry 角], 对应待测 Pauli X / Y / Z。
PAULI_ROTATIONS = np.array(
    [
        [np.pi / 2, 0],
        [np.pi / 2, np.pi / 2],
        [0, 0],
    ],
    dtype=float,
)

AngleSampler = Callable[
    [int, int, np.random.Generator],
    tuple[np.ndarray, np.ndarray],
]


def _sample_haar(group_num, setting_num, rng):
    theta = np.arccos(rng.uniform(-1.0, 1.0, size=(group_num, setting_num)))
    phi = rng.uniform(0.0, 2.0 * np.pi, size=(group_num, setting_num))
    return theta, phi


def _sample_pauli(group_num, setting_num, rng):
    idx = rng.choice(3, size=(group_num, setting_num))
    return PAULI_ROTATIONS[idx, 0], PAULI_ROTATIONS[idx, 1]


def _sample_derandom(group_num, setting_num, rng):
    if setting_num > 3**group_num:
        raise ValueError(f"setting_num={setting_num} exceeds 3^{group_num}")

    bases = np.array(list(product(range(3), repeat=group_num)), dtype=int)
    selected = bases[rng.choice(3**group_num, size=setting_num, replace=False)].T
    return PAULI_ROTATIONS[selected, 0], PAULI_ROTATIONS[selected, 1]


ANGLE_SAMPLERS: dict[str, AngleSampler] = {
    "haar": _sample_haar,
    "pauli": _sample_pauli,
    "derandom": _sample_derandom,
}


@dataclass
class ParameterGenerator:
    angle_sampler: AngleSampler
    rng: np.random.Generator

    def generate(self, params, setting_num):
        theta_vals, phi_vals = self.angle_sampler(
            len(params[0]), setting_num, self.rng
        )
        theta, phi = params
        binds = {theta[i]: theta_vals[i].tolist() for i in range(len(theta))}
        binds.update({phi[i]: phi_vals[i].tolist() for i in range(len(phi))})
        return binds


def create_parameter_generator(ensemble, *, seed=None):
    try:
        sampler = ANGLE_SAMPLERS[ensemble]
    except KeyError:
        raise ValueError(
            f"Unknown ensemble: {ensemble!r}. Available: {list(ANGLE_SAMPLERS)}"
        ) from None

    return ParameterGenerator(sampler, np.random.default_rng(seed))
