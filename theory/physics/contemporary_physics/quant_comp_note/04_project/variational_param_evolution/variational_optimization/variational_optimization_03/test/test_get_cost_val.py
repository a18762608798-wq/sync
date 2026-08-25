import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from get_initial_state import get_initial_state
from get_evolution_qc import get_evolution_qc
from get_op import get_ssh_constrained_H
from get_cost_val import get_cost_val


if __name__ == "__main__":
    initial_state = get_initial_state()
    evolution_qc = get_evolution_qc(initial_state, 0.216093, 0.138569, n=0)
    cost_op = get_ssh_constrained_H(1, ϵ=0)
    cost_val = get_cost_val(evolution_qc, cost_op)
    print("cost_val =", cost_val)
