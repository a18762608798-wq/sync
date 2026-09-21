import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from get_op import get_xyz, get_ssh_constrained_H


def main():
    print("=== get_xyz: H_odd ===")
    Ho, He = get_xyz()
    print(Ho)

    print("=== get_xyz: H_even ===")
    print(He)

    print("=== get_ssh_constrained_H(s=0.25, Δ=1) ===")
    print(get_ssh_constrained_H(0.25))


if __name__ == "__main__":
    main()
