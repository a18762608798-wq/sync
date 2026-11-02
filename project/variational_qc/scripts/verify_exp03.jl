# Production assertions for exp03 (T008/T015): full-output checks on data/exp03/.
# Locks the spec Contract F conditions (VAL-001..VAL-005): grid, fit recompute,
# D02b subset, non-negativity. Failure => invalid run.
# Prints VERIFY-EXP03-OK plus diagnostics on success.

push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra
BLAS.set_num_threads(1)
using Shared01  # load order for Exp03
using Shared01: H_DEF_ID
using Exp03
using Exp03: sector_basis
using Exp03: quadratic_fit, s_grid_points
using Exp03: SCHEMA, LS, GAP_MIN_TOL, FIT_TOL
using NPZ, JSON3

const DATA_DIR = joinpath(@__DIR__, "..", "data", "exp03")

function main()
    d = NPZ.npzread(joinpath(DATA_DIR, "exp03_D02.npz"))
    manifest = open(JSON3.read, joinpath(DATA_DIR, "exp03_manifest.json"))
    @assert manifest["schema"] == SCHEMA == "exp03/v1"
    @assert manifest["H_def"] == H_DEF_ID
    @assert manifest["delta"] == -2.0
    @assert vec(d["Ls"]) == collect(LS)

    s = vec(d["s_grid"])
    D = d["Delta"]
    @assert s == collect(Float64, s_grid_points())
    @assert size(D) == (5, 99)
    @assert all(isfinite, D)
    @assert minimum(D) ≥ GAP_MIN_TOL

    # Sector dims re-derived (constructive check; L=16 enumeration is trivial).
    for (r, L) in enumerate(LS)
        @assert manifest["sector_dims"][string(L)] == length(sector_basis(L).members)
    end

    # D02c: five points at s = 0.5 (i = 50), fit recomputed from the grid.
    i05 = findfirst(x -> abs(x - 0.5) < 1e-12, s)
    @assert i05 !== nothing
    xs = [1.0 / L for L in LS]
    ys = [D[r, i05] for r in 1:5]
    @assert vec(d["fit_x"]) == xs && vec(d["fit_y"]) == ys
    fit = quadratic_fit(xs, ys)
    @assert abs(fit.a - d["fit_a"][]) < FIT_TOL
    @assert abs(fit.b - d["fit_b"][]) < FIT_TOL
    @assert abs(fit.c - d["fit_c"][]) < FIT_TOL

    # D02b subset: s in [0.53, 0.65] must be present and complete.
    sel = findall(x -> 0.53 - 1e-12 ≤ x ≤ 0.65 + 1e-12, s)
    @assert !isempty(sel)
    @assert length(sel) == count(x -> 0.53 - 1e-12 ≤ x ≤ 0.65 + 1e-12, collect(Float64, s_grid_points()))

    # Diagnostics (recorded only, no pass thresholds per spec VAL-004).
    println("fit: a = $(d["fit_a"][]), b = $(d["fit_b"][]), c = $(d["fit_c"][])")
    for (r, L) in enumerate(LS)
        m, i = findmin(D[r, :])
        println("L=$L: min Δ_sec = $m at s = $(s[i])")
    end
    println("D02b window points: ", length(sel))
    println("VERIFY-EXP03-OK")
end

main()
