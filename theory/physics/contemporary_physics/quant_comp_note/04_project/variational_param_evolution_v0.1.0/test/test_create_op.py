import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from create_op import get_Ui, get_ssh_H, get_ssh_constrained_H


def _link_supports(qubit_num, s, delta):
    supports = set()
    for label, _ in get_ssh_H(qubit_num, s, delta).to_list():
        idx = [i for i, c in enumerate(label) if c != "I"]
        supports.add(tuple(idx))
    return supports


def test_dimer_limits():
    assert _link_supports(8, 0.0, 0.5) == {(i, i + 1) for i in range(0, 8, 2)}
    assert _link_supports(8, 1.0, 0.5) == {(i, i + 1) for i in range(1, 7, 2)}


def test_n4_known_coeffs():
    coeffs = dict(get_ssh_H(4, 0.5, 0.5).to_list())
    assert coeffs == {
        "IIXX": 0.5,
        "IIZZ": 0.25,
        "IXXI": 0.5,
        "IZZI": 0.25,
        "XXII": 0.5,
        "ZZII": 0.25,
    }


def test_get_ssh_constrained_H():
    Hc = get_ssh_constrained_H(4, 0.5, 0.5)
    assert Hc == get_ssh_H(4, 0.5, 0.5) - (get_Ui(4, "X") + 2 * get_Ui(4, "Z"))
    Hc2 = get_ssh_constrained_H(4, 0.5, 0.5, ϵ=2)
    assert Hc2 == get_ssh_H(4, 0.5, 0.5) - 2 * (get_Ui(4, "X") + 2 * get_Ui(4, "Z"))


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
