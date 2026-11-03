"""exp07 本地单元测试（T006）：纯逻辑 + Aer 仿真，零真机调用。

CondaPkg env python -m pytest test/test_exp07_local.py
Aer 黄金交叉（抽样 (δ,s) 获胜分支 p=2 vs S06 spi/ostr，容限 1e-8）不通过不得进 T003。
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from exp07_circuits import (  # noqa: E402
    L,
    P,
    SPARSE,
    TAG_OF_DI,
    branch_circuit,
    branch_invalid,
    branch_theta,
    build_init,
    orbit_params,
)

PROJ = Path(__file__).resolve().parent.parent
QISKIT = pytest.importorskip("qiskit")
Aer = pytest.importorskip("qiskit_aer")
S06 = PROJ / "data/exp04/exp04_S06.npz"


def aer_statevector(qc):
    from qiskit.quantum_info import Statevector
    qc2 = qc.copy()
    qc2.remove_final_measurements()
    return np.asarray(Statevector.from_instruction(qc2).data)


def probs_of(psi):
    p = np.abs(np.asarray(psi)) ** 2
    return p / p.sum()


def exp_zdiag(probs, pauli_dict):
    ev = 0.0
    for b in range(1 << L):
        bits = [(b >> q) & 1 for q in range(L)]
        z = [1 - 2 * x for x in bits]
        for qs, c in pauli_dict.items():
            v = c
            for q in qs:
                v *= z[q]
            ev += v * probs[b]
    return ev


def s_pi_of(probs):
    d = {}
    for i in range(L):
        for j in range(L):
            if i == j:
                continue
            key = tuple(sorted((i, j)))
            d[key] = d.get(key, 0) + (-1) ** (i - j) / L
    return exp_zdiag(probs, d) + 1.0


def string_of(probs):
    terms = {}
    for a in (0, 1):
        for b in (6, 7):
            key = tuple(sorted({a, 2, 3, 4, 5, b}))
            terms[key] = terms.get(key, 0) + 1.0
    return exp_zdiag(probs, terms)


def test_branch_theta_matches_s06():
    s06 = np.load(S06)
    for di in (1, 2):
        tag = TAG_OF_DI[di]
        for si in (1, 50, 99):
            for a in (1, 2, 3):
                raw = np.asarray(s06[f"{tag}_theta_leg"])[si - 1, a - 1, P - 1, :]
                assert branch_theta(S06, di, si, a) == pytest.approx(raw[~np.isnan(raw)])
    assert len(branch_theta(S06, 1, 1, 1)) == L * P


def test_branch_invalid_matches_flags():
    s06 = np.load(S06)
    n_inv = 0
    for di in (1, 2):
        tag = TAG_OF_DI[di]
        for si in SPARSE:
            for a in (1, 2, 3):
                conv = bool(np.asarray(s06[f"{tag}_conv"])[si - 1, a - 1, P - 1])
                stagn = bool(np.asarray(s06[f"{tag}_stagn"])[si - 1, a - 1, P - 1])
                assert branch_invalid(S06, di, si, a) == ((not conv) and (not stagn))
                n_inv += branch_invalid(S06, di, si, a)
    assert n_inv == 0


def test_init_and_orbit_layout():
    psi = aer_statevector(build_init(1))
    assert psi[170] == pytest.approx(0.25)
    th = np.arange(1, 25, dtype=float)
    lay = orbit_params(th, 2, 3, 0.85)
    assert lay[0]["odd"][0] == (1.0, 2.0)
    assert lay[0]["even"][1] == (7.0, 8.0)
    assert lay[1]["odd"][0] == (9.0, 10.0)


def test_golden_cross_winner_p2_vs_s06():
    """Aer 黄金交叉：获胜分支 p=2 电路 vs S06 spi/ostr（容限 1e-8）。"""
    s06 = np.load(S06)
    deltas = np.asarray(s06["deltas"])
    n_checked = 0
    for di, delta in enumerate(deltas, start=1):
        tag = TAG_OF_DI[di]
        for si in (1, 50, 99):
            a = int(np.asarray(s06[f"{tag}_a_star"])[si - 1, P - 1])
            psi = aer_statevector(branch_circuit(S06, di, si, a, float(delta)))
            probs = probs_of(psi)
            assert s_pi_of(probs) == pytest.approx(
                s06[f"{tag}_spi"][si - 1, P - 1], abs=1e-8)
            assert string_of(probs) == pytest.approx(
                s06[f"{tag}_ostr"][si - 1, P - 1], abs=1e-8)
            n_checked += 1
    assert n_checked == 6


def test_groups_and_bill_consistent():
    groups = json.loads((PROJ / "data/exp07/joint/groups.json").read_text())["groups"]
    bill = json.loads((PROJ / "data/exp07/joint/rounds/r001/bill.json").read_text())
    assert len(groups) == 90
    assert bill["total_tasks"] == 46000 and bill["confirmed"] is True


def test_mitigation_identity_and_q():
    from exp07_assemble import (  # noqa: E402
        branch_window_stats,
        search_best_branch_window,
        window_endpoints90,
    )
    from exp06_assemble import (  # noqa: E402
        mitigate_counts,
        q_hat_basis,
    )
    rng = np.random.default_rng(0)
    ideal = rng.random(256)
    ideal /= ideal.sum()
    Ms = [np.eye(2)] * 8
    out = mitigate_counts({format(b, "08b"): int(ideal[b] * 10 ** 9)
                           for b in range(256)}, Ms, 8)
    assert np.allclose(out / out.sum(), ideal, atol=1e-6)
    qb = q_hat_basis(8.0, 4.0)
    assert qb.shape == (256,)
    ep = window_endpoints90(np.arange(90, dtype=float),
                            -np.arange(90, dtype=float))
    assert ep["S_max"] == 89.0 and ep["O_max"] == 89.0


def test_branch_window_search_synthetic():
    from exp07_assemble import search_best_branch_window  # noqa: E402
    rng = np.random.default_rng(1)
    U, G = 20, 90
    S = rng.random((U, G)) + 4.0
    O = -rng.random((U, G)) - 1.0
    q_sim30 = rng.random(30)
    branch_idx = np.array([gi % 3 + 1 for gi in range(G)])
    pair_idx = np.array([gi // 3 for gi in range(G)])
    # NOTE: synthetic layout only checks mechanics, not spec ordering.
    win = search_best_branch_window(S, O, q_sim30, branch_idx, pair_idx)
    assert win["length"] % 2 == 0 and win["length"] >= 10
    assert set(win["r_a"]) == {"1", "2", "3"}
    assert win["pass"] is None
