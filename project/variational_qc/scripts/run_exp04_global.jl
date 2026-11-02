# Diagnostic full-grid global-sampling VQE (exp04 T018, NON-production).
#
# Same (δ,s,leg) grid as production, but p = 1, 2, 3 ALL use run_leg_global
# (N_GLOBAL uniform samples + zero vector, top-K L-BFGS each depth).
# Independent archive under data/exp04_global/ with S06-compatible keys
# (gm2_/gd085_ prefixes); production data/exp04/ is untouched.
# Spec PRE-003 (warm chain) still governs production; this is exploratory.
#
#   julia --project=. --startup-file=no scripts/run_exp04_global.jl

push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra
BLAS.set_num_threads(1)  # point-level threading only (constitution V)
using Shared01  # load order: Exp04 reuses Shared01.Hamiltonian read-only
using Shared01: build_hamiltonian
using Exp04
using Exp04: LEG_LABELS, psi_init
using Exp04: build_meta, run_leg_global, energy_of, expect_ztot, overlap_xbar, overlap_reflect
using Exp02
using Exp02: zz_correlators, structure_factor
using Exp02: string_order
using NPZ, JSON3, Dates

const OUT_DIR = joinpath(@__DIR__, "..", "data", "exp04_global")
const PROD_DIR = joinpath(@__DIR__, "..", "data", "exp04")
const DELTAS = (-2.0, 0.85)
const S_GRID = [i / 100 for i in 1:99]  # same convention as S01 / S06
const THETA_MAX = 24
const TAGS = Dict(-2.0 => "gm2", 0.85 => "gd085")

"""Winner-state observables + symmetry diagnostics for one (δ,s,p)."""
function eval_best(delta::Real, a_star::String, theta_star::Vector{Float64}, p::Integer)
    meta = build_meta(8, a_star)
    psi0 = psi_init(a_star, 8)
    psi = apply_circuit!(zeros(ComplexF64, 256), psi0, theta_star, meta, p, Float64(delta))
    C = zz_correlators(psi)
    spi = structure_factor(C, pi)
    ostr = string_order(psi)
    zt = abs(expect_ztot(psi, 8))
    xb = abs(overlap_xbar(psi, 8) - 1)
    xr = abs(overlap_reflect(psi, 8) - 1)
    return spi, ostr, zt, xb, xr
end

function run_line(delta::Real)
    ns = length(S_GRID)
    theta_star = fill(NaN, ns, 3, THETA_MAX)
    E_star = zeros(ns, 3)
    a_star = zeros(Int, ns, 3)
    spi = zeros(ns, 3)
    ostr = zeros(ns, 3)
    e0 = zeros(ns)
    leg_E = zeros(ns, 3, 3)
    conv = falses(ns, 3, 3)
    stagn = falses(ns, 3, 3)
    dtail = zeros(ns, 3, 3)
    theta_leg = fill(NaN, ns, 3, 3, THETA_MAX)
    einit = zeros(ns, 3)
    sym = zeros(ns, 3, 3)
    Threads.@threads for i in 1:ns
        s = S_GRID[i]
        H = build_hamiltonian(8, s, Float64(delta))
        e0[i] = minimum(eigvals(Hermitian(H)))
        di = round(Int, 100 * Float64(delta))
        si = round(Int, 100 * Float64(s))
        for (li, leg) in enumerate(LEG_LABELS)
            meta = build_meta(8, leg)
            psi0 = psi_init(leg, 8)
            einit[i, li] = real(dot(psi0, H * psi0))
            for p in 1:3
                st = run_leg_global(H, psi0, meta, Float64(delta), p, di, si, li)
                leg_E[i, li, p] = st.energy
                conv[i, li, p] = st.converged
                stagn[i, li, p] = st.stagnant
                dtail[i, li, p] = st.dtail
                thv = Vector{Float64}(st.theta)
                theta_leg[i, li, p, 1:length(thv)] = thv
            end
        end
        for p in 1:3
            vals = [leg_E[i, li, p] for li in 1:3]
            li = argmin(vals)
            a = LEG_LABELS[li]
            th = Vector{Float64}(vec(theta_leg[i, li, p, :]))
            a_star[i, p] = li
            E_star[i, p] = vals[li]
            thv = th[1:8 * p]
            theta_star[i, p, 1:length(thv)] = thv
            sp, os, zt, xb, xr = eval_best(Float64(delta), a, thv, p)
            spi[i, p] = sp
            ostr[i, p] = os
            sym[i, p, :] = [zt, xb, xr]
        end
    end
    return Dict("theta_star" => theta_star, "E_star" => E_star, "a_star" => a_star,
                "spi" => spi, "ostr" => ostr, "e0" => e0, "leg_E" => leg_E,
                "theta_leg" => theta_leg, "conv" => conv, "stagn" => stagn,
                "dtail" => dtail, "einit" => einit, "sym" => sym)
end

function main()
    println("threads: ", Threads.nthreads())
    flush(stdout)
    mkpath(OUT_DIR)
    for delta in DELTAS
        tag = TAGS[delta]
        line_path = joinpath(OUT_DIR, "line_$(tag).npz")
        if isfile(line_path)
            println("δ=$delta: already complete")
            flush(stdout)
            continue
        end
        t0 = time()
        payload = run_line(Float64(delta))
        tmp = line_path * ".tmp"
        NPZ.npzwrite(tmp, merge(Dict("delta" => Float64(delta), "s_grid" => S_GRID), payload))
        mv(tmp, line_path; force=true)
        println("δ=$delta done in $(round(time() - t0, digits=1))s")
        flush(stdout)
    end
    # Assemble with S06-compatible key names.
    flat = Dict{String,Any}("s_grid" => S_GRID, "deltas" => collect(DELTAS))
    for delta in DELTAS
        tag = TAGS[delta]
        c = NPZ.npzread(joinpath(OUT_DIR, "line_$(tag).npz"))
        for k in ("theta_star", "E_star", "a_star", "spi", "ostr", "e0",
                  "leg_E", "theta_leg", "conv", "stagn", "dtail", "einit", "sym")
            flat["$(tag)_$(k)"] = c[k]
        end
    end
    s06_path = joinpath(OUT_DIR, "exp04global_S06.npz")
    NPZ.npzwrite(s06_path * ".tmp", flat)
    mv(s06_path * ".tmp", s06_path; force=true)
    manifest = Dict(
        "schema" => "exp04global/v1",
        "H_def" => "ssh-xxz-OBC-H-v1",
        "L" => 8,
        "deltas" => collect(DELTAS),
        "grid" => "s = i/100, i = 1..99 (same convention as S01)",
        "protocol" => "p=1,2,3 ALL global sampling (N_GLOBAL uniform + zero, top-K L-BFGS per depth); NO warm chain. Diagnostic archive, not production.",
        "seeds" => "deterministic per (δ,s,p,leg) via _derive_seed (same rule as production p=1 stage)",
        "n_global" => 64,
        "top_k" => 4,
        "julia_version" => string(VERSION),
        "created_utc" => string(Dates.now(Dates.UTC)),
    )
    manifest_path = joinpath(OUT_DIR, "exp04global_manifest.json")
    open(manifest_path, "w") do io
        JSON3.write(io, manifest)
    end
    # Self-check: global p=1 must reproduce production S06 p=1 (same seed stream).
    prod = NPZ.npzread(joinpath(PROD_DIR, "exp04_S06.npz"))
    for (delta, ptag) in ((-2.0, "dm2"), (0.85, "d085"))
        gtag = TAGS[delta]
        dE = maximum(abs.(vec(flat["$(gtag)_E_star"][:, 1]) .- vec(prod["$(ptag)_E_star"][:, 1])))
        println("p=1 vs production S06 max|dE| ($(ptag)): $dE")
        flush(stdout)
        dE < 1e-12 || throw(ErrorException("global p=1 diverged from production p=1"))
    end
    println("wrote: $s06_path")
    println("wrote: $manifest_path")
end

main()
