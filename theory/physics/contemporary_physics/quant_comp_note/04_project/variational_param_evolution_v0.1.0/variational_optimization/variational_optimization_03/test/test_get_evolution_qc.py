import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from get_initial_state import get_initial_state
from get_evolution_qc import get_evolution_qc


def main():
    initial_state = get_initial_state()
    qc = get_evolution_qc(initial_state, 0.2, 0.3, n=1)
    print(qc.draw())


if __name__ == "__main__":
    main()
