import sys
from pathlib import Path


from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from get_evolution_path import get_evolution_path
from get_hardware_op import get_hardware_ssh_H


def get_evolution_qc(
    initial_state,
    start,
    end,
    control,
    Δts,
    decompose_points,
    order=1,
):
    qc = initial_state
    qubit_num = qc.num_qubits
    path = get_evolution_path(start, end, control, Δts, decompose_points)
    path_length = len(path)
    for path_idx in range(path_length):
        s, δ = path[path_idx]
        Δt = Δts[path_idx]
        H = get_hardware_ssh_H(qubit_num, s, δ)

        synth = SuzukiTrotter(order=order, reps=1)
        evo = PauliEvolutionGate(
            H,
            time=Δt,
            synthesis=synth,
        )

        qc.append(evo, range(qubit_num))

    return qc, path
