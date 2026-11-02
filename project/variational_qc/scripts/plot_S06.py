"""S06 diagnostic curves (exp04 T017): 2 figures = 2 delta-lines x Q.

Diagnostic only (not a paper product; paper shows D08 overlays).
Reads data/exp04/exp04_S06.npz (winner-state Q per p) and
data/exp04/exp04_D09.npz (exact Q from S01 exact states, built in Julia).
No physics recomputed here.

Q = 4/3 - 2*O_hat - (4/3)*S_hat with S_hat = S(pi)/L, O_hat = -O_str
(same normalization as D04a/b/c; L = 8). Each figure overlays exact Q
(blue solid, same language as D09 E0) and p = 1, 2, 3 in unified black
dashed styles. Style via scripts/figure_style.py. Self-checks grids,
shapes, and winner/min-leg agreement before plotting.

Run through scripts/run_py.jl (CondaPkg env).
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "..", "data", "exp04")
FIGDIR = os.path.join(HERE, "..", "figs", "exp04")

L_SYS = 8
TAGS = ["dm2", "d085"]
DELTA_LABELS = [r"$\delta=-2$", r"$\delta=0.85$"]
P_STYLES = ["--", ":", "-."]
EXACT_COLOR = "#0072B2"


def q_of(spi_raw, ostr_raw):
    """Winner-state Q from archived raw S(pi) / O_str (L = 8)."""
    s_hat = np.asarray(spi_raw, float) / L_SYS
    o_hat = -np.asarray(ostr_raw, float)
    return 4.0 / 3.0 - 2.0 * o_hat - (4.0 / 3.0) * s_hat


def q_of_exact(spi_norm, ostr_raw):
    """Exact Q from D09-archived normalized S-hat(pi) and raw O_str."""
    s_hat = np.asarray(spi_norm, float)
    o_hat = -np.asarray(ostr_raw, float)
    return 4.0 / 3.0 - 2.0 * o_hat - (4.0 / 3.0) * s_hat


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from figure_style import apply_figure_style, finalize_figure

    apply_figure_style()
    d = np.load(os.path.join(DATA, "exp04_S06.npz"))
    d09 = np.load(os.path.join(DATA, "exp04_D09.npz"))

    assert list(d["deltas"]) == [-2.0, 0.85]
    assert np.allclose(d09["s_grid"], d["s_grid"])
    assert np.array_equal(np.asarray(d09["deltas"], float), np.array([-2.0, 0.85]))
    s = d["s_grid"]
    assert s.shape == (99,)

    os.makedirs(FIGDIR, exist_ok=True)
    for tag, dlabel, di in [("dm2", DELTA_LABELS[0], 0),
                            ("d085", DELTA_LABELS[1], 1)]:
        E_star = d[f"{tag}_E_star"]
        leg_E = d[f"{tag}_leg_E"]
        assert E_star.shape == (99, 3) and leg_E.shape == (99, 3, 3)
        # winner = min leg (bit-exact: same archived floats)
        assert np.array_equal(E_star, leg_E.min(axis=1)), f"{tag} winner mismatch"
        qq = q_of(d[f"{tag}_spi"], d[f"{tag}_ostr"])
        assert qq.shape == (99, 3) and np.isfinite(qq).all(), f"{tag}/Q incomplete"
        q_exact = q_of_exact(d09["spi_exact"][:, di], d09["ostr_exact"][:, di])
        assert q_exact.shape == (99,) and np.isfinite(q_exact).all()

        fig, ax = plt.subplots()
        ax.plot(s, q_exact, color=EXACT_COLOR, linewidth=2.0, linestyle="-",
                zorder=2, label=r"$Q$ (exact)")
        for p in range(3):
            ax.plot(s, qq[:, p], color="black",
                    linestyle=P_STYLES[p], linewidth=1.5, zorder=3,
                    label=rf"$p={p + 1}$")
        ax.set_xlabel(r"$s$")
        ax.set_ylabel(r"$Q$")
        ax.set_title(rf"{dlabel} VQE")
        ax.legend(frameon=False, fontsize=10)
        finalize_figure(fig, os.path.join(FIGDIR, f"exp04_S06_{tag}_Q.pdf"))
        finalize_figure(fig, os.path.join(FIGDIR, f"exp04_S06_{tag}_Q.png"))
        plt.close(fig)
        print(f"wrote: figs/exp04/exp04_S06_{tag}_Q.pdf + .png")


if __name__ == "__main__":
    main()
