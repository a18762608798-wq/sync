# Formal production run for exp02 (T005).
# Thin orchestration only: S01 input gating -> module APIs -> chunked persist -> assembly.
# Experiment conditions come from specs/exp02/spec.md; nothing is redefined here.

push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra
BLAS.set_num_threads(1)  # grid-level threading only (constitution V)
using Shared01: S_GRID, DELTA_GRID, load_shared01
using Shared01: assert_s01_gate, EXPECTED_BASIS_CONVENTION
using Exp02
using Exp02: zz_correlators, structure_factor
using Exp02: panel_point
using Exp02: save_row, completed_rows, save_d03, assemble_D04

const S01_DIR = joinpath(@__DIR__, "..", "data", "shared01")
const OUT_DIR = joinpath(@__DIR__, "..", "data", "exp02")

const Q_GRID = collect(1:99) .* (2pi / 100)  # spec PRE-002: 101-partition minus boundaries
const REP_LABELS = ["trivial", "topological", "afm"]

"""Representative points come from the S01 manifest (spec PRE-003 selection rule)."""
function rep_coords(manifest)
    reps = manifest["representative_points_S02"]
    return Dict(label => (Float64(reps[label]["s"]), Float64(reps[label]["delta"]))
                for label in REP_LABELS)
end

function main()
    println("threads: ", Threads.nthreads())
    flush(stdout)
    arrays, manifest = load_shared01(S01_DIR)
    deg = assert_s01_gate(manifest, EXPECTED_BASIS_CONVENTION)
    s01_id = "shared01/v1 created $(manifest["created_utc"])"
    println("S01 gate OK; degenerate points: $(length(deg))")
    flush(stdout)

    psi_all = arrays["psi"]
    reps = manifest["representative_points_S02"]
    rep_ij = Dict(label => (Int(reps[label]["grid_index"][1]),
                            Int(reps[label]["grid_index"][2])) for label in REP_LABELS)
    nd = length(DELTA_GRID)
    todo = setdiff(Set(1:nd), completed_rows(OUT_DIR))
    println("rows to compute: $(length(todo)) / $nd")
    flush(stdout)
    t0 = time()
    Threads.@threads for j in collect(todo)
        pts = [panel_point(Vector{ComplexF64}(psi_all[i, j, :])) for i in 1:99]
        save_row(OUT_DIR, j, collect(Float64, S_GRID), Float64(DELTA_GRID[j]), pts)
    end
    println("rows done in $(round(time() - t0, digits=1))s")
    flush(stdout)

    # D03: normalised Ŝ(q)=S(q)/L curves at the three S02 representative points.
    curves = zeros(3, 99)
    for (k, label) in enumerate(REP_LABELS)
        i, j = rep_ij[label]
        C = zz_correlators(Vector{ComplexF64}(psi_all[i, j, :]))
        curves[k, :] = [structure_factor(C, q) / 8 for q in Q_GRID]
    end
    save_d03(OUT_DIR, collect(Q_GRID), curves, REP_LABELS)
    println("D03 curves done")
    flush(stdout)

    extra = Dict("q_grid" => "q = 2πk/100, k = 1..99 (includes q=π at k=50)",
                 "rep_points" => Dict(label => (Float64(reps[label]["s"]),
                                                Float64(reps[label]["delta"]))
                                      for label in REP_LABELS))
    npz_path, manifest_path = assemble_D04(OUT_DIR, collect(Float64, S_GRID),
        collect(Float64, DELTA_GRID), s01_id, deg, extra)
    println("wrote: $npz_path")
    println("wrote: $manifest_path")
end

main()
