from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter


from get_op import get_ssh_H


def get_evolution_path(start, end, x):
    a = end[0] - start[0]
    b = end[1] - start[1]
    p = []
    for x_val in x:
        s = start[0] + a * x_val
        δ = start[1] + b * x_val
        p.append((s, δ))
    return p


def get_evolution_qc(
    initial_state,
    path,
    Δts,
    order=1,
):
    qc = initial_state
    qubit_num = qc.num_qubits
    path_length = len(path)
    for path_idx in range(path_length):
        s, δ = path[path_idx]
        Δt = Δts[path_idx]
        H = get_ssh_H(s, δ)

        synth = SuzukiTrotter(order=order, reps=1)
        evo = PauliEvolutionGate(
            H,
            time=Δt,
            synthesis=synth,
        )

        qc.append(evo, range(qubit_num))

    return qc
