# D09 winner bands + exact E0 (+ exact observables for the S06 exact-Q overlay),
# read-only from production S06 (p=1 winners) and shared-01 S01 (exact states).
# Band rule (spec PRE-004): at each s the band label is the p=1 winning
# initial state, argmin_a C_a(s), coded 1 = triv, 2 = topo, 3 = afm — the same
# coding as S06 a_star (LEG_LABELS order). Pure kernels + thin I/O; the Python
# plot script consumes the archived labels and never recomputes physics.

const D09_L = 8  # S01 system size; Ŝ(π) = S(π)/L (same normalization as D04a)
const D09_NPZ_NAME = "exp04_D09.npz"
const PHASE_TRIV = 1
const PHASE_TOPO = 2
const PHASE_AFM = 3

"""Build exp04_D09.npz: p=1 winner bands + exact E0 for both production δ lines.

Reads the production `exp04_S06.npz` for the band labels (`a_star[:, p=1]`)
and `shared01_S01.npz` (ψ, E0, grids) at the two `DELTAS` rows for the exact
quantities; asserts the s-grids match. No VQE quantity is recomputed here.
"""
function build_D09(dir::AbstractString, s01_path::AbstractString, s06_path::AbstractString)
    s01 = NPZ.npzread(s01_path)
    s06 = NPZ.npzread(s06_path)
    sg = vec(s01["s_grid"])
    dg = vec(s01["delta_grid"])
    sg == S_GRID || throw(ErrorException("S01 s_grid mismatch"))
    vec(s06["s_grid"]) == S_GRID || throw(ErrorException("S06 s_grid mismatch"))
    ns = length(S_GRID)
    nd = length(DELTAS)
    phase = zeros(Int, ns, nd)
    E0 = zeros(ns, nd)
    spi = zeros(ns, nd)
    zt = zeros(ns, nd)
    os = zeros(ns, nd)
    for (di, delta) in enumerate(DELTAS)
        tag = delta < 0 ? "dm2" : "d085"
        a1 = vec(Int.(s06["$(tag)_a_star"][:, 1]))
        all(a -> a in (PHASE_TRIV, PHASE_TOPO, PHASE_AFM), a1) ||
            throw(ErrorException("S06 a_star out of range"))
        phase[:, di] = a1
        j = argmin(abs.(dg .- delta))
        abs(Float64(dg[j]) - delta) < 1e-12 ||
            throw(ErrorException("delta $delta missing from S01 grid"))
        for i in 1:ns
            psi = ComplexF64.(vec(s01["psi"][i, j, :]))
            C = zz_correlators(psi)
            spi[i, di] = structure_factor(C, pi) / D09_L   # normalized Ŝ(π), as in D04a
            zt[i, di] = z_tilde(psi).z_tilde
            os[i, di] = string_order(psi)              # raw O_str (Ô = -O_str)
            E0[i, di] = Float64(s01["E0"][i, j])
        end
    end
    path = joinpath(dir, D09_NPZ_NAME)
    tmp = path * ".tmp"
    NPZ.npzwrite(tmp, Dict(
        "s_grid" => S_GRID,
        "deltas" => collect(DELTAS),
        "phase" => phase,
        "E0" => E0,
        "spi_exact" => spi,
        "z_tilde" => zt,
        "ostr_exact" => os,
    ))
    mv(tmp, path; force=true)
    return path
end
