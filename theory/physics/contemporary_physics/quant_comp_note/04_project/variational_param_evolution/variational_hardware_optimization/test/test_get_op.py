import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from get_op import get_ssh_constrained_H


def test_get_ssh_constrained_H():
    Hc = get_ssh_constrained_H(0.5, 0.5, ϵ=1)
    return Hc


if __name__ == "__main__":
    print(test_get_ssh_constrained_H())
