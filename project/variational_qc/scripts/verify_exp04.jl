# Production assertions for exp04 (T008): full-output checks on data/exp04/.
# Locks every spec Contract F condition (VAL-001..VAL-008); failure => invalid run.
# Prints VERIFY-EXP04-OK plus diagnostics on success.

push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra
using Statistics
BLAS.set_num_threads(1)
using Shared01  # load order for Exp04
using Shared01: H_DEF_ID
using Exp02
using Exp04
using Exp04: SCHEMA, DELTAS, S_GRID, THETA_MAX
using NPZ, JSON3

const DATA_DIR = joinpath(@__DIR__, "..", "data", "exp04")

const FIELDS = ("theta_star", "E_star", "a_star", "spi", "ostr", "e0",
                "leg_E", "theta_leg", "conv", "stagn", "dtail", "einit", "sym")

function check_line(d10, tag::String, delta::Real, stag_tol::Real)
    c = Dict(k => d10["$(tag)_$(k)"] for k in FIELDS)
    ns = 99
    @assert size(c["theta_star"]) == (ns, 3, THETA_MAX)
    @assert size(c["theta_leg"]) == (ns, 3, 3, THETA_MAX)
    @assert size(c["E_star"]) == (ns, 3)
    npl = [8, 16, 24]  # both production lines have δ≠0 (PRE-001)
    for i in 1:ns, p in 1:3
        row = vec(c["theta_star"][i, p, :])
        @assert count(isfinite, row) == npl[p]  # NaN pad beyond Nθ
        @assert all(isfinite, [c["E_star"][i, p], c["spi"][i, p], c["ostr"][i, p]])
        for li in 1:3
            @assert c["conv"][i, li, p]
            @assert !c["stagn"][i, li, p]
            theta = vec(c["theta_leg"][i, li, p, 1:npl[p]])
            H = Shared01.build_hamiltonian(8, i / 100, Float64(delta))
            leg = LEG_LABELS[li]
            actual = energy_of(theta, H, psi_init(leg, 8), build_meta(8, leg),
                               p, Float64(delta), zeros(ComplexF64, 256))
            @assert abs(actual - c["leg_E"][i, li, p]) < 1e-8
        end
        a = Int(c["a_star"][i, p])
        @assert 1 ≤ a ≤ 3
        @assert isequal(vec(c["theta_leg"][i, a, p, :]), vec(c["theta_star"][i, p, :]))
        @assert c["leg_E"][i, a, p] == minimum(vec(c["leg_E"][i, :, p]))  # winner = min leg
        @assert c["E_star"][i, p] ≤ c["einit"][i, a] + 1e-8  # VQE never worsens init
        @assert c["E_star"][i, p] ≥ c["e0"][i] - 1e-8        # variational principle
        @assert maximum(vec(c["sym"][i, p, :])) < 1e-8       # symmetry preserved
    end
end

function main()
    d10 = NPZ.npzread(joinpath(DATA_DIR, "exp04_S06.npz"))
    s03 = NPZ.npzread(joinpath(DATA_DIR, "exp04_S03.npz"))
    manifest = open(JSON3.read, joinpath(DATA_DIR, "exp04_manifest.json"))
    stag_tol = 0.0  # retained function argument; no stagnation acceptance
    @assert manifest["schema"] == SCHEMA == "exp04/v2"
    @assert manifest["optimization_protocol"] == OPTIMIZATION_PROTOCOL
    @assert Exp04.decode_protocol(d10["optimization_protocol"]) == OPTIMIZATION_PROTOCOL
    @assert Exp04.decode_protocol(s03["optimization_protocol"]) == OPTIMIZATION_PROTOCOL
    @assert manifest["H_def"] == H_DEF_ID
    @assert vec(d10["deltas"]) == collect(DELTAS)
    check_line(d10, "dm2", -2.0, stag_tol)
    check_line(d10, "d085", 0.85, stag_tol)

    # S03: 594 groups reference the same S06 values.
    th, meta = s03["theta"], s03["meta"]
    @assert size(th) == (594, THETA_MAX) && size(meta) == (594, 4)
    r = 0
    for (di, tag) in enumerate(["dm2", "d085"])
        c = Dict(k => d10["$(tag)_$(k)"] for k in FIELDS)
        for i in 1:99, p in 1:3
            r += 1
            @assert vec(meta[r, :]) == [di, i, p, Int(c["a_star"][i, p])]
            @assert isequal(vec(th[r, :]), vec(c["theta_star"][i, p, :]))
        end
    end

    # D09 (VAL-003): combined figure + winner bands locked to the S06 archive.
    s01 = NPZ.npzread(joinpath(@__DIR__, "..", "data", "shared01", "shared01_S01.npz"))
    d09 = NPZ.npzread(joinpath(DATA_DIR, "exp04_D09.npz"))
    @assert vec(d09["s_grid"]) == S_GRID
    @assert vec(d09["deltas"]) == collect(DELTAS)
    for ext in ("pdf", "png")
        @assert isfile(joinpath(@__DIR__, "..", "figs", "exp04", "exp04_D09.$(ext)"))
    end
    for (di, delta, tag) in ((1, -2.0, "dm2"), (2, 0.85, "d085"))
        j = argmin(abs.(vec(s01["delta_grid"]) .- delta))
        @assert abs(Float64(s01["delta_grid"][j]) - delta) < 1e-12
        @assert maximum(abs.(vec(s01["E0"][:, j]) .- vec(d09["E0"][:, di]))) < 1e-10
        # Band rule recomputed from the same archive (spec VAL-003, PRE-004):
        # bands are the S06 p=1 winning legs.
        @assert vec(Int.(d10["$(tag)_a_star"][:, 1])) == vec(d09["phase"][:, di])
        # Exact overlay column recomputed from S01 exact states.
        ns = 99
        oo = zeros(ns)
        for i in 1:ns
            psi = ComplexF64.(vec(s01["psi"][i, j, :]))
            oo[i] = string_order(psi)
        end
        @assert maximum(abs.(vec(oo) .- vec(d09["ostr_exact"][:, di]))) < 1e-12
    end

    # Diagnostics (recorded only, no pass thresholds per spec VAL-007).
    for (tag, delta) in [("dm2", -2.0), ("d085", 0.85)]
        c = Dict(k => d10["$(tag)_$(k)"] for k in FIELDS)
        mono = sum(c["E_star"][i, p + 1] > c["E_star"][i, p] + 1e-8
                   for i in 1:99 for p in 1:2)
        gap = vec(c["E_star"]) - vec(repeat(vec(c["e0"]), 1, 3))
        println("δ=$delta: p-monotonicity violations=$mono, " *
                "max(E*-E0)=$(maximum(gap)), median=$(median(vec(gap)))")
        println("δ=$delta: a* counts=$( [[sum(vec(c["a_star"][:, q]) .== a) for a in 1:3] for q in 1:3] ) per p")
        println("δ=$delta: stagnant legs=$(sum(vec(c["stagn"])))")
    end
    println("VERIFY-EXP04-OK")
end

main()
