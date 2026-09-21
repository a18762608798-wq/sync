from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter

from get_op import get_xyz


def get_evolution_qc(
    initial_state,
    θodd,
    θeven,
    *,
    n=0,
):
    qc = initial_state.copy()  # 防止共享qc被修改.
    qubit_num = qc.num_qubits

    synth = SuzukiTrotter(order=1, reps=1)
    H_odd, H_even = get_xyz()
    evo_odd = PauliEvolutionGate(
        H_odd,
        time=θodd,
        synthesis=synth,
    )
    evo_even = PauliEvolutionGate(
        H_even,
        time=θeven,
        synthesis=synth,
    )

    qc.append(evo_even, range(qubit_num))
    qc.append(evo_odd, range(qubit_num))
    ideal_u = qc.copy()
    qc.barrier()
    if n != 0:
        cargs = range(qc.num_clbits)
        for _ in range(n):
            qc.append(ideal_u.inverse(), range(qubit_num), cargs)
            qc.barrier()
            qc.append(ideal_u, range(qubit_num), cargs)
            qc.barrier()

    return qc
