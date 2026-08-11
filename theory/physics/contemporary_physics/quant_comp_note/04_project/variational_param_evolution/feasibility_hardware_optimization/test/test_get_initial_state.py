import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from get_hw_initial_state import get_initial_state


def draw_all():
    print(get_initial_state(phase_idx=1).draw())
    print(get_initial_state(phase_idx=0).draw())
    print(get_initial_state(phase_idx=-1).draw())


if __name__ == "__main__":
    draw_all()
