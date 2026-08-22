import sys
from pathlib import Path


from qiskit import transpile


sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from get_initial_state import get_initial_state
from get_evolution_qc import get_evolution_qc, get_evolution_path


LOOPNUM = 10
QUBITNUM = 8
COUPLING_MAP = [pair for i in range(LOOPNUM - 1) for pair in [[i, i + 1], [i + 1, i]]]
COUPLING_MAP.append([0, LOOPNUM - 1])
COUPLING_MAP.append([LOOPNUM - 1, 0])


initial_state = get_initial_state(phase_idx=0)
start = [1, 1]
end = [0.5, 0.5]
x = [0.5]
path = get_evolution_path(start, end, x)
Δts = [1]
qc = get_evolution_qc(
    initial_state,
    path,
    Δts,
    order=1,
)
tqc1 = transpile(
    qc,
    basis_gates=["u3", "cz"],
    optimization_level=1,  # 优化等级
    coupling_map=COUPLING_MAP,
    routing_method="sabre",
)
tqc3 = transpile(
    qc,
    basis_gates=["u3", "cz"],
    optimization_level=3,  # 优化等级
    coupling_map=COUPLING_MAP,
    routing_method="sabre",
)
print(tqc1)
print(tqc1.depth())  # 电路深度
print(tqc3)
print(tqc3.depth())  # 电路深度
