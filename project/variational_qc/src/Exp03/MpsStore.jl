# Persistence for the exp03 CPU MPS/DMRG extension (spec POST-001, POST-003).
# ED chunks remain untouched.  MPS production points use a separate directory and
# a separate schema; capacity/validation records are plain JSON sidecars so a
# failed trial is never mistaken for a D02 data point.

const MPS_SCHEMA = "exp03-mps/v1"
const MPS_CHUNKS_DIRNAME = "mps_chunks"
const MPS_PROGRESS_NAME = "mps_progress.json"
const MPS_BLOCK = 5

function mps_source_fingerprint()
    root = normpath(joinpath(@__DIR__, "..", ".."))
    paths = [joinpath(root, p) for p in
             ("src/Exp03.jl", "src/Exp03/MpsGapSolver.jl", "src/Exp03/MpsStore.jl",
              "scripts/run_exp03_mps.jl", "scripts/verify_exp03_mps.jl",
              "src/Exp03/Store.jl", "src/Exp03/GapSolver.jl",
              "src/Shared01/Hamiltonian.jl",
              "Project.toml", "Manifest.toml")]
    return bytes2hex(sha256(join(read.(filter(isfile, paths), String), "\n")))
end

mps_params_dict(p::MpsDMRGParams) =
    Dict(string(k) => getfield(p, k) for k in fieldnames(MpsDMRGParams))

function mps_runtime()
    return Dict("julia_version" => string(VERSION),
                "ITensors_version" => string(Base.pkgversion(ITensors)),
                "ITensorMPS_version" => string(Base.pkgversion(ITensorMPS)),
                "blas_threads" => BLAS.get_num_threads(),
                "julia_threads" => Threads.nthreads())
end

mps_chunk_id(L::Integer, ib::Integer) = "mps_L$(L)-b$(ib)"
_mps_chunks(dir) = joinpath(dir, MPS_CHUNKS_DIRNAME)
mps_chunk_path(dir, L, ib) = joinpath(_mps_chunks(dir), "gap_$(mps_chunk_id(L, ib)).npz")
mps_detail_path(dir, L, ib) = joinpath(_mps_chunks(dir), "gap_$(mps_chunk_id(L, ib)).json")

mps_chunk_exists(dir::AbstractString, L::Integer, ib::Integer) =
    isfile(mps_chunk_path(dir, L, ib))

function _atomic_text(path::AbstractString, text::AbstractString)
    mkpath(dirname(path))
    tmp = path * ".tmp"
    open(tmp, "w") do io
        write(io, text)
    end
    mv(tmp, path; force=true)
    return path
end

function _json_safe(x)
    if x isa AbstractFloat
        return isfinite(x) ? Float64(x) : nothing
    elseif x isa Integer || x isa Bool || x isa AbstractString || x === nothing
        return x
    elseif x isa AbstractVector
        return [_json_safe(v) for v in x]
    elseif x isa NamedTuple
        return Dict(string(k) => _json_safe(v) for (k, v) in pairs(x))
    elseif x isa AbstractDict
        return Dict(string(k) => _json_safe(v) for (k, v) in x)
    else
        return string(x)
    end
end

function _state_dict(st::MpsStateResult)
    return _json_safe(Dict(
        "index" => st.index,
        "E_pen" => st.E_pen,
        "E" => st.E,
        "sz2" => st.sz2,
        "xbar" => st.xbar,
        "reflection" => st.reflection,
        "max_bond_dim" => st.max_bond_dim,
        "accepted" => st.accepted,
        "sweep_ok" => st.sweep_ok,
        "last_energy_change" => st.last_energy_change,
        "max_trunc_error" => st.max_trunc_error,
        "n_sweeps" => st.n_sweeps,
        "sweep_energies" => st.sweep_energies,
        "trunc_errors" => st.trunc_errors,
    ))
end

function mps_point_dict(r::MpsPointResult)
    return _json_safe(Dict(
        "schema" => MPS_SCHEMA,
        "method" => r.method,
        "L" => r.L,
        "s" => r.s,
        "delta" => r.delta,
        "E0" => r.E0,
        "E1" => r.E1,
        "Delta" => r.delta_gap,
        "chi" => r.chi,
        "chi_ladder" => r.chi_ladder,
        "nstates" => r.nstates,
        "n_accepted" => r.n_accepted,
        "max_bond_dim" => r.max_bond_dim,
        "last_energy_change" => r.last_energy_change,
        "max_trunc_error" => r.max_trunc_error,
        "sweep_ok" => r.sweep_ok,
        "sector_ok" => r.sector_ok,
        "overlap_min_eig" => r.overlap_min_eig,
        "sz2_0" => r.sz2_0,
        "xbar_0" => r.xbar_0,
        "reflection_0" => r.reflection_0,
        "sz2_1" => r.sz2_1,
        "xbar_1" => r.xbar_1,
        "reflection_1" => r.reflection_1,
        "wall_seconds" => r.wall_seconds,
        "peak_rss_mib" => r.peak_rss_mib,
        "valid" => mps_point_valid(r),
        "states" => [_state_dict(st) for st in r.states],
        "params" => mps_params_dict(r.params),
        "runtime" => mps_runtime(),
        "source_fingerprint" => mps_source_fingerprint(),
    ))
end

"""Check recorded values, rather than trusting the recorded valid flag."""
function mps_record_valid(rec)
    get(rec, "schema", "") == MPS_SCHEMA || return false
    get(rec, "method", "") == MPS_METHOD || return false
    get(rec, "valid", false) === true || return false
    nums = ("E0", "E1", "Delta", "last_energy_change", "max_trunc_error",
            "overlap_min_eig", "sz2_0", "sz2_1", "xbar_0", "xbar_1",
            "reflection_0", "reflection_1")
    all(k -> get(rec, k, nothing) isa Real && isfinite(rec[k]), nums) || return false
    rec["Delta"] ≥ -1e-12 || return false
    abs(rec["Delta"] - (rec["E1"] - rec["E0"])) < 1e-10 || return false
    rec["last_energy_change"] < MPS_ENERGY_DRIFT_TOL || return false
    rec["max_trunc_error"] < MPS_TRUNC_TOL || return false
    rec["overlap_min_eig"] > 1e-10 || return false
    for tag in ("0", "1")
        abs(rec["sz2_$tag"]) < MPS_SYM_TOL || return false
        abs(rec["xbar_$tag"] - 1) < MPS_SYM_TOL || return false
        abs(rec["reflection_$tag"] - 1) < MPS_SYM_TOL || return false
    end
    states = get(rec, "states", [])
    count(st -> get(st, "accepted", false) === true, states) ≥ 2 || return false
    for st in states
        ev = get(st, "sweep_energies", [])
        tr = get(st, "trunc_errors", [])
        length(ev) ≥ 2 && !isempty(tr) || return false
        all(x -> x isa Real && isfinite(x), ev) || return false
        all(x -> x isa Real && isfinite(x), tr) || return false
        abs(ev[end] - ev[end-1]) < MPS_ENERGY_DRIFT_TOL || return false
        maximum(tr) < MPS_TRUNC_TOL || return false
    end
    return true
end

function mps_record_matches(rec, L::Integer, s::Real, p::MpsDMRGParams;
                            delta::Real=DELTA_FIXED)
    get(rec, "L", nothing) == L && get(rec, "s", nothing) == Float64(s) &&
        get(rec, "delta", nothing) == Float64(delta) || return false
    get(rec, "source_fingerprint", "") == mps_source_fingerprint() || return false
    haskey(rec, "params") && haskey(rec, "runtime") || return false
    all(get(rec["params"], k, nothing) == v for (k, v) in mps_params_dict(p)) || return false
    return all(get(rec["runtime"], k, nothing) == v for (k, v) in mps_runtime())
end

function mps_pair_valid(pair)
    haskey(pair, "low") && haskey(pair, "high") || return false
    low, high = pair["low"], pair["high"]
    mps_record_valid(low) && mps_record_valid(high) || return false
    all(low[k] == high[k] for k in ("L", "s", "delta")) || return false
    high["chi"] == 2low["chi"] || return false
    return abs(low["Delta"] - high["Delta"]) < MPS_CHI_GAP_TOL
end

"""Derived blocks retain both chi calculations; individual point files are primary."""
function save_mps_chunk_records(dir::AbstractString, L::Integer, ib::Integer, pairs)
    all(mps_pair_valid, pairs) || error("refusing invalid or unconverged MPS block")
    all(p -> p["high"]["L"] == L, pairs) || error("MPS block L mismatch")
    mkpath(_mps_chunks(dir))
    recs = [p["high"] for p in pairs]
    keys = ("s", "E0", "E1", "Delta", "chi", "last_energy_change", "max_trunc_error",
            "sz2_0", "xbar_0", "reflection_0", "sz2_1", "xbar_1", "reflection_1")
    arrays = Dict{String,Any}(k => [r[k] for r in recs] for k in keys)
    arrays["L"] = Int(L)
    path = mps_chunk_path(dir, L, ib)
    NPZ.npzwrite(path * ".tmp", arrays)
    mv(path * ".tmp", path; force=true)
    detail = Dict("schema" => MPS_SCHEMA, "L" => L, "block" => ib,
                  "s" => arrays["s"], "pairs" => pairs)
    _atomic_text(mps_detail_path(dir, L, ib), JSON3.write(_json_safe(detail)))
    return path
end

function save_mps_point_json(path::AbstractString, r::MpsPointResult)
    return _atomic_text(path, JSON3.write(mps_point_dict(r)))
end

function _read_mps_progress(dir)
    path = joinpath(dir, MPS_PROGRESS_NAME)
    isfile(path) || return Set{String}()
    return Set{String}(open(JSON3.read, path)["completed_chunks"])
end

const _MPS_PROGRESS_LOCK = ReentrantLock()

"""Persist one MPS (L, s-block) chunk and its full per-state diagnostics."""
function save_mps_chunk(dir::AbstractString, L::Integer, ib::Integer,
                        s::Vector{Float64}, res::Vector{MpsPointResult};
                        record_progress::Bool=true)
    length(s) == length(res) || throw(ArgumentError("s and res length mismatch"))
    for (i, r) in enumerate(res)
        r.L == L && abs(r.s - s[i]) < 1e-12 ||
            throw(ArgumentError("MPS result does not match chunk L/s at index $i"))
    end
    all(mps_point_valid, res) ||
        throw(ErrorException("refusing to persist an invalid MPS chunk"))
    mkpath(_mps_chunks(dir))
    path = mps_chunk_path(dir, L, ib)
    tmp = path * ".tmp"
    NPZ.npzwrite(tmp, Dict(
        "L" => Int(L),
        "s" => s,
        "E0" => [r.E0 for r in res],
        "E1" => [r.E1 for r in res],
        "Delta" => [r.delta_gap for r in res],
        "chi" => [r.chi for r in res],
        "chi_max" => [maximum(r.chi_ladder) for r in res],
        "nstates" => [r.nstates for r in res],
        "max_bond_dim" => [r.max_bond_dim for r in res],
        "wall_seconds" => [r.wall_seconds for r in res],
        "peak_rss_mib" => [r.peak_rss_mib for r in res],
        "last_energy_change" => [r.last_energy_change for r in res],
        "max_trunc_error" => [r.max_trunc_error for r in res],
        "sz2_0" => [r.sz2_0 for r in res],
        "xbar_0" => [r.xbar_0 for r in res],
        "reflection_0" => [r.reflection_0 for r in res],
        "sz2_1" => [r.sz2_1 for r in res],
        "xbar_1" => [r.xbar_1 for r in res],
        "reflection_1" => [r.reflection_1 for r in res],
    ))
    mv(tmp, path; force=true)
    detail = Dict(
        "schema" => MPS_SCHEMA,
        "L" => Int(L),
        "block" => Int(ib),
        "s" => s,
        "points" => [mps_point_dict(r) for r in res],
    )
    _atomic_text(mps_detail_path(dir, L, ib), JSON3.write(detail))
    if record_progress
        lock(_MPS_PROGRESS_LOCK) do
            done = _read_mps_progress(dir)
            push!(done, mps_chunk_id(L, ib))
            _atomic_text(joinpath(dir, MPS_PROGRESS_NAME),
                         JSON3.write(Dict("schema" => MPS_SCHEMA,
                                          "completed_chunks" => sort(collect(done)))))
        end
    end
    return path
end

function load_mps_chunk(dir::AbstractString, L::Integer, ib::Integer)
    arrays = NPZ.npzread(mps_chunk_path(dir, L, ib))
    details = open(JSON3.read, mps_detail_path(dir, L, ib))
    return arrays, details
end

function mps_completed_chunks(dir::AbstractString)
    return _read_mps_progress(dir)
end

"""Save one capacity trial, including failures, without touching D02."""
function save_capacity_trial(dir::AbstractString, L::Integer, chi::Integer,
                             r::Union{MpsPointResult,Nothing};
                             error::Union{Nothing,AbstractString}=nothing,
                             extra::AbstractDict=Dict{String,Any}())
    mkpath(dir)
    path = joinpath(dir, "L$(L)_chi$(chi).json")
    rec = if r === nothing
        Dict("schema" => MPS_SCHEMA, "L" => Int(L), "chi" => Int(chi),
             "valid" => false, "status" => "error", "error" => something(error, "unknown"),
             "extra" => extra)
    else
        d = mps_point_dict(r)
        d["status"] = mps_point_valid(r) ? "ok" : "invalid"
        d["extra"] = extra
        d
    end
    return _atomic_text(path, JSON3.write(_json_safe(rec)))
end

function save_capacity_summary(path::AbstractString, summary::AbstractDict)
    target = endswith(path, ".json") ? path : joinpath(path, "summary.json")
    return _atomic_text(target, JSON3.write(_json_safe(summary)))
end


"""Assemble only the four paper sizes, preserving ED and both-chi MPS sources."""
function assemble_D02(dir::AbstractString; ed_dir::AbstractString,
                        mps_dir::AbstractString, validation_dir::AbstractString)
    validation = open(JSON3.read,joinpath(validation_dir,"validation","summary.json"))
    capacity = open(JSON3.read,joinpath(validation_dir,"capacity","summary.json"))
    get(validation,"complete",false) === true || error("full MPS validation missing")
    get(capacity,"feasible",false) === true || error("L=32 capacity not passed")
    for rec in (validation,capacity)
        rec["source_fingerprint"] == mps_source_fingerprint() || error("stale release evidence")
    end
    all(r -> r["valid"] === true, validation["records"]) || error("invalid ED/MPS comparison")
    expected = Set(vcat([(L,Float64(s)) for L in (8,12,16) for s in s_grid_points()],
                       [(24,s) for s in (0.1,0.5,0.6,0.9)],[(26,0.5),(28,0.5)]))
    Set((Int(r["L"]),Float64(r["s"])) for r in validation["records"]) == expected ||
        error("incomplete release validation coverage")
    mps_pair_valid(capacity["pair"]) || error("invalid capacity chi pair")
    sg = Float64.(s_grid_points())
    nblocks = cld(length(sg),BLOCK)
    D = zeros(length(PAPER_LS),length(sg))
    sources = Dict{String,Any}()
    methods = ["ed-arpack","ed-arpack","ed-arpack",MPS_METHOD]
    for (row,L) in enumerate(PAPER_LS)
        offset = 0
        row_sources = Any[]
        for ib in 1:nblocks
            if L in ED_LS
                path = _chunkpath(ed_dir,L,ib)
                arrays = NPZ.npzread(path)
                ss,ds = vec(arrays["s"]),vec(arrays["Delta"])
                Int(arrays["L"][]) == L || error("ED chunk L mismatch")
                all(isfinite,arrays["E0"]) && all(isfinite,arrays["E1"]) || error("nonfinite ED energies")
                maximum(abs.(ds .- (vec(arrays["E1"]) .- vec(arrays["E0"])))) < 1e-12 ||
                    error("ED chunk gap inconsistency")
            else
                path = mps_detail_path(mps_dir,L,ib)
                detail = open(JSON3.read,path)
                detail["L"] == L || error("MPS chunk L mismatch")
                pairs = detail["pairs"]
                all(mps_pair_valid,pairs) || error("invalid MPS chi-pair evidence")
                for pair in pairs, key in ("low","high")
                    rec = pair[key]
                    rec["source_fingerprint"] == mps_source_fingerprint() || error("stale MPS point")
                    rec["L"] == L && rec["delta"] == DELTA_FIXED || error("MPS model mismatch")
                end
                ss = [p["high"]["s"] for p in pairs]
                ds = [p["high"]["Delta"] for p in pairs]
                all(ss .== detail["s"]) || error("MPS sidecar coordinates inconsistent")
            end
            length(ss) == length(ds) || error("chunk coordinate length mismatch")
            last = offset + length(ss)
            last ≤ length(sg) || error("too many points L=$L")
            Float64.(ss) == sg[(offset+1):last] || error("chunk grid mismatch L=$L")
            D[row,(offset+1):last] = ds
            offset = last
            push!(row_sources,Dict("path"=>abspath(path),"sha256"=>bytes2hex(sha256(read(path)))))
        end
        offset == length(sg) || error("incomplete grid L=$L")
        sources[string(L)] = row_sources
    end
    all(isfinite,D) && minimum(D) ≥ GAP_MIN_TOL || error("invalid paper gap grid")
    xs = 1.0 ./ collect(PAPER_LS)
    ys = D[:,50]
    fit = quadratic_fit(xs,ys)
    mkpath(dir)
    path = joinpath(dir,D02_NPZ_NAME)
    NPZ.npzwrite(path * ".tmp",Dict("s_grid"=>sg,"Ls"=>collect(PAPER_LS),"Delta"=>D,
        "fit_x"=>xs,"fit_y"=>ys,"fit_a"=>fit.a,"fit_b"=>fit.b,"fit_c"=>fit.c))
    mv(path * ".tmp",path; force=true)
    manifest = Dict("schema"=>SCHEMA,"H_def"=>H_DEF_ID,"delta"=>DELTA_FIXED,
        "Ls"=>collect(PAPER_LS),"methods"=>methods,"sources"=>sources,
        "sector_dims"=>Dict(string(L)=>length(sector_basis(L).members) for L in PAPER_LS if L in ED_LS),
        "points_per_L"=>length(sg),"fit"=>"least squares a+b/L+c/L^2 over four paper sizes",
        "resid_tol"=>RESID_TOL,"gap_min_tol"=>GAP_MIN_TOL,"fit_tol"=>FIT_TOL,
        "validation_dir"=>abspath(validation_dir),"source_fingerprint"=>mps_source_fingerprint(),
        "created_utc"=>string(Dates.now(Dates.UTC)),"runtime"=>mps_runtime())
    mp = joinpath(dir,MANIFEST_NAME)
    _atomic_text(mp,JSON3.write(manifest))
    return path,mp
end
