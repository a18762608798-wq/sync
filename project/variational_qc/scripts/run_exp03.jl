# Formal production run for exp03 (T005/T012/T014/T016).
# Thin orchestration only: module APIs -> chunked persist -> assembly.
# Experiment conditions come from specs/exp03/spec.md; nothing is redefined here.
#
# Parallelism: process-level (one Julia worker per core slot, BLAS single-threaded).
# ARPACK keeps Fortran SAVE state and is not thread-safe, so a single process can
# only diagonalize serially; independent processes each own a private ARPACK state.
# Tasks are (L, s-block) pairs, so resume is just "skip existing chunk files".
#
# Env knobs: EXP03_WORKERS (default 6), EXP03_LS (comma list, e.g. "8" for a smoke run).

push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra
BLAS.set_num_threads(1)  # each worker is single-threaded (constitution V)
using Shared01  # load order: Exp03 reuses Shared01 read-only
using Exp03
using Exp03: solve_gap, s_grid_points, save_chunk, assemble_D02, chunk_exists, LS, BLOCK
using Distributed

const SRCDIR = normpath(joinpath(@__DIR__, "..", "src"))
const OUT_DIR = normpath(joinpath(@__DIR__, "..", "data", "exp03"))
const NWORKERS = parse(Int, get(ENV, "EXP03_WORKERS", "6"))
const ONLY_LS = let raw = get(ENV, "EXP03_LS", "")
    isempty(raw) ? collect(LS) : parse.(Int, split(raw, ","))
end

if NWORKERS > 1 && nworkers() == 1
    addprocs(NWORKERS; exeflags=`--project=$(Base.active_project()) --startup-file=no -t 1`)
end

@everywhere push!(LOAD_PATH, $(SRCDIR))
@everywhere begin
    using LinearAlgebra
    BLAS.set_num_threads(1)
    using Exp03

    function run_task(L::Int, ib::Int)
        pts = Exp03.s_grid_points()
        lo = (ib - 1) * Exp03.BLOCK + 1
        hi = min(ib * Exp03.BLOCK, length(pts))
        s = pts[lo:hi]
        res = [Exp03.solve_gap(L, x) for x in s]
        Exp03.save_chunk($(OUT_DIR), L, ib, s, res; record_progress=false)
        GC.gc()  # release the (large) factorization workspace between tasks
        return (L, ib, length(res))
    end
end

function main()
    pts = s_grid_points()
    nblocks = cld(length(pts), BLOCK)
    todo = [(L, ib) for L in ONLY_LS for ib in 1:nblocks if !chunk_exists(OUT_DIR, L, ib)]
    println("workers: ", nworkers(), " | threads/worker: ", Threads.nthreads())
    println("points per L: ", length(pts), " | blocks per L: ", nblocks)
    println("chunks to compute: ", length(todo), " / ", length(ONLY_LS) * nblocks)
    flush(stdout)
    t0 = time()
    done = pmap(t -> run_task(t[1], t[2]), todo)
    println("computed ", length(done), " chunks in ", round(time() - t0, digits = 1), " s")
    flush(stdout)
    println("ED reference chunks complete. Current paper assembly requires the verified CPU MPS L=32 row.")
    println("Use run_exp03_mps.jl assemble after full MPS validation; this ED runner does not replace D02.")
end

main()
