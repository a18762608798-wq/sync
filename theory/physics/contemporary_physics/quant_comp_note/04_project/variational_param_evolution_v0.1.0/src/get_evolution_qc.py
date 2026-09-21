from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter


from create_op import get_ssh_H
from get_evolution_path import get_evolution_path


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
        H = get_ssh_H(qubit_num, s, δ)

        synth = SuzukiTrotter(order=order, reps=1)
        evo = PauliEvolutionGate(
            H,
            time=Δt,
            synthesis=synth,
        )

        qc.append(evo, range(qubit_num))

    return qc, path
