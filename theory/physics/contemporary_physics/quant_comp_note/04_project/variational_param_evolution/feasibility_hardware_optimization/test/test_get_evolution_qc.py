import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from get_hw_initial_state import get_initial_state
from get_hw_evolution_qc import get_evolution_qc, get_evolution_path

initial_state = get_initial_state(phase_idx=1)
start = [1, 1]
end = [0.5, 0.5]
x = [0.5, 0.8, 0.1]
path = get_evolution_path(start, end, x)
Δts = [2, 10, 5]
qc = get_evolution_qc(
    initial_state,
    path,
    Δts,
    order=1,
)
print(qc.draw())
