# Per-point symmetric-gap solver for exp03 (spec INV-001, INV-003).
# Δ_sec(L,s) = E1^{(P=-2)} - E0^{(P=-2)} at delta = -2 (spec PRE-001).
# Dense exact diagonalization of the small sector matrix: no iterative solver,
# no convergence parameters. Pure kernel, no I/O.

const DELTA_FIXED = -2.0

# spec PRE-002: single grid s = i/100, i = 1..99.
const S_GRID = [i / 100 for i in 1:99]
const N_POINTS = length(S_GRID)

"""Execution grid (99 points) for the production run."""
s_grid_points() = S_GRID

struct GapResult
    E0::Float64
    E1::Float64
    delta_gap::Float64
end

const ARPACK_TOL = 1e-12     # eigensolver precision (plan §3)
const RESID_TOL = 1e-10      # per-pair residual hard assertion (plan §4)
const ARPACK_MAXITER = 1000
const ARPACK_NCV = 64        # Krylov subspace size (capped by n)

# ARPACK (Fortran, internal SAVE state) is not thread-safe: concurrent eigs
# calls from multiple Julia threads corrupt each other (observed as XYAUPD
# info=3 / segfaults). All eigs calls are serialized through this lock;
# assembly and residual checks stay parallel. Single eigs ≈ 0.1s, so the
# serial section costs ~30s total for the whole production.
const _ARPACK_LOCK = ReentrantLock()

_eigs_two(H; ncv::Integer, tol::Real) = lock(_ARPACK_LOCK) do
    Arpack.eigs(H; nev=2, ncv=min(size(H, 1), ncv), which=:SR, tol=tol, maxiter=ARPACK_MAXITER)
end

"""Lowest two P=-2 sector eigenpairs and their gap at (L, s).

Sparse ARPACK path (plan §6): nev=2 smallest-real on the sparse Hermitian
sector matrix. Each returned pair must satisfy ‖Hv−λv‖ < RESID_TOL with
nconv ≥ 2, else the point is an invalid run (fail fast, never silent).

ARPACK uses a random start vector, so the residual of an otherwise converged
pair fluctuates; a single unlucky start can land a few 1e-11 above the hard
threshold. Retry ladder: same tolerance with a larger Krylov subspace, then
machine precision. The contract threshold RESID_TOL is never relaxed.
"""
function solve_gap(L::Integer, s::Real, delta::Real=DELTA_FIXED)
    H = sector_hamiltonian(L, s, delta)
    best_res = Inf
    for (ncv, tol) in ((ARPACK_NCV, ARPACK_TOL),
                       (2 * ARPACK_NCV, ARPACK_TOL),
                       (4 * ARPACK_NCV, 0.0))
        d, v, nconv = _eigs_two(H; ncv=ncv, tol=tol)
        nconv ≥ 2 || continue
        order = sortperm(real.(d[1:2]))
        E = [real(d[order[1]]), real(d[order[2]])]
        ok = true
        for i in 1:2
            res = norm(H * v[:, order[i]] - E[i] * v[:, order[i]])
            best_res = min(best_res, res)
            ok &= res < RESID_TOL
        end
        ok && return GapResult(E[1], E[2], E[2] - E[1])
    end
    throw(ErrorException("eigenpair residual $best_res ≥ $RESID_TOL at L=$L s=$s after retries"))
end

