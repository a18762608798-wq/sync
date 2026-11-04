# Incremental persistence for exp03 (constitution IV).
# Chunks: one .npz per (L, s-block) + progress manifest + D02 assembly.
# I/O only; physics lives in GapSolver/Fit.

const SCHEMA = "exp03/v1"
const ED_LS = (8, 12, 16, 20, 24)
const LS = ED_LS  # historical ED producer; paper assembly uses PAPER_LS explicitly
const PAPER_LS = (8, 16, 24, 32)
const BLOCK = 5  # s-points per chunk file (fine granularity for pmap + resume)
const CHUNKS_DIRNAME = "chunks"
const PROGRESS_NAME = "progress.json"
const D02_NPZ_NAME = "exp03_D02.npz"
const MANIFEST_NAME = "exp03_manifest.json"

const GAP_MIN_TOL = -1e-12  # roundoff allowance on spec Δ ≥ 0
const FIT_TOL = 1e-12       # fit recompute consistency

chunk_id(L::Integer, ib::Integer) = "L$(L)-b$(ib)"
_chunks(dir) = joinpath(dir, CHUNKS_DIRNAME)
_chunkpath(dir, L, ib) = joinpath(_chunks(dir), "gap_$(chunk_id(L, ib)).npz")

"""True iff the chunk file exists (cross-process resumability; no shared JSON)."""
chunk_exists(dir::AbstractString, L::Integer, ib::Integer) = isfile(_chunkpath(dir, L, ib))

function _read_progress(dir)
    path = joinpath(dir, PROGRESS_NAME)
    isfile(path) || return Set{String}()
    return Set{String}(open(JSON3.read, path)["completed_chunks"])
end

completed_chunks(dir::AbstractString) = _read_progress(dir)

const _PROGRESS_LOCK = ReentrantLock()

"""Persist one (L, s-block) chunk (atomically) and record it in the progress file."""
function save_chunk(dir::AbstractString, L::Integer, ib::Integer,
                    s::Vector{Float64}, res::Vector{GapResult};
                    record_progress::Bool = true)
    mkpath(_chunks(dir))
    path = _chunkpath(dir, L, ib)
    tmp = path * ".tmp"
    NPZ.npzwrite(tmp, Dict(
        "L" => L,
        "s" => s,
        "E0" => [r.E0 for r in res],
        "E1" => [r.E1 for r in res],
        "Delta" => [r.delta_gap for r in res],
    ))
    mv(tmp, path; force=true)
    if record_progress
        lock(_PROGRESS_LOCK) do
            done = _read_progress(dir)
            push!(done, chunk_id(L, ib))
            open(joinpath(dir, PROGRESS_NAME), "w") do io
                JSON3.write(io, Dict("schema" => SCHEMA, "completed_chunks" => sort(collect(done))))
            end
        end
    end
    return path
end

"""Assemble all chunks into the single D02 product + manifest (hard asserts inside)."""
function assemble_ed_reference(dir::AbstractString)
    s_grid = collect(Float64, S_GRID)
    npts = length(s_grid)
    nblocks = cld(npts, BLOCK)
    D = zeros(length(LS), npts)
    for (r, L) in enumerate(LS)
        col = 0
        for ib in 1:nblocks
            c = NPZ.npzread(_chunkpath(dir, L, ib))
            Int(c["L"][]) == L || throw(ErrorException("chunk L mismatch: $(_chunkpath(dir, L, ib))"))
            s = vec(c["s"])
            d = vec(c["Delta"])
            for t in eachindex(s)
                col += 1
                col ≤ npts || throw(ErrorException("L=$L has too many points"))
                abs(Float64(s[t]) - s_grid[col]) < 1e-12 ||
                    throw(ErrorException("L=$L s-grid mismatch at index $col"))
                D[r, col] = Float64(d[t])
            end
        end
        col == npts || throw(ErrorException("L=$L incomplete: $col/$npts"))
    end
    all(isfinite, D) || throw(ErrorException("non-finite Δ grid"))
    minimum(D) ≥ GAP_MIN_TOL || throw(ErrorException("Δ below tolerance: $(minimum(D))"))

    # D02c: s = 0.5 is i = 50; five points reused from the grid.
    i05 = findfirst(x -> abs(x - 0.5) < 1e-12, s_grid)
    i05 === nothing && throw(ErrorException("s=0.5 missing from grid"))
    xs = [1.0 / L for L in LS]
    ys = [D[r, i05] for r in 1:length(LS)]
    fit = quadratic_fit(xs, ys)
    all(isfinite, (fit.a, fit.b, fit.c)) || throw(ErrorException("non-finite fit coefficients"))

    npz_path = joinpath(dir, D02_NPZ_NAME)
    tmp = npz_path * ".tmp"
    NPZ.npzwrite(tmp, Dict(
        "s_grid" => s_grid,
        "Ls" => collect(LS),
        "Delta" => D,
        "fit_x" => xs,
        "fit_y" => ys,
        "fit_a" => fit.a,
        "fit_b" => fit.b,
        "fit_c" => fit.c,
    ))
    mv(tmp, npz_path; force=true)

    githead = try
        readchomp(`git rev-parse --short HEAD`)
    catch
        "unknown"
    end
    manifest = Dict(
        "schema" => SCHEMA,
        "H_def" => H_DEF_ID,
        "sector_basis" => "Z_tot=0 orbits under {I, Xbar, R, XbarR}, all-+ symmetrized",
        "sector_dims" => Dict(string(L) => length(sector_basis(L).members) for L in LS),
        "delta" => DELTA_FIXED,
        "grid" => "s = i/100, i = 1..99 (101-partition minus boundaries)",
        "points_per_L" => npts,
        "fit" => "least squares Δ = a + b/L + c/L² over five L",
        "solver" => "sparse ARPACK eigs(nev=2, which=:SR)",
        "arpack_tol" => ARPACK_TOL,
        "arpack_ncv" => ARPACK_NCV,
        "resid_tol" => RESID_TOL,
        "gap_min_tol" => GAP_MIN_TOL,
        "fit_tol" => FIT_TOL,
        "julia_version" => string(VERSION),
        "git_head" => githead,
        "created_utc" => string(Dates.now(Dates.UTC)),
    )
    manifest_path = joinpath(dir, MANIFEST_NAME)
    open(manifest_path, "w") do io
        JSON3.write(io, manifest)
    end
    return npz_path, manifest_path
end
