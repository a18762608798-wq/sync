import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from get_hardware_initial_state import get_hardware_initial_state


def draw_all():
    get_hardware_initial_state(phase_idx=1).draw()
    get_hardware_initial_state(phase_idx=-1).draw()
    get_hardware_initial_state(phase_idx=0).draw()


if __name__ == "__main__":
    draw_all()
