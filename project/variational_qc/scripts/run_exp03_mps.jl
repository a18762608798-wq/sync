# CPU exp03: capacity, smoke, validate, crosscheck, production, assemble.
# Full validation is mandatory before production. Every solve is saved immediately.
push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra, JSON3, Dates, SHA, NPZ, Distributed
BLAS.set_num_threads(parse(Int, get(ENV, "EXP03_MPS_BLAS_THREADS", "1")))
using Exp03

const ROOT = normpath(joinpath(@__DIR__, ".."))
const RUN_ID = mps_source_fingerprint()[1:12]
const RUN_DIR = get(ENV, "EXP03_MPS_RUN_DIR",
                    joinpath(ROOT, "data", "validation", "exp03-mps-v2-20261104", RUN_ID))
const CAP_DIR = joinpath(RUN_DIR, "capacity")
const VAL_DIR = joinpath(RUN_DIR, "validation")
const PROD_DIR = get(ENV, "EXP03_MPS_PROD_DIR", joinpath(ROOT, "data", "exp03-mps", RUN_ID))
const ED_DIR = joinpath(ROOT, "data", "exp03")
const ED_REF_PATH = joinpath(ROOT, "data", "validation", "exp03-l-capacity-20261104", "ed_reference.json")

function params(chi)
    return mps_params(chi;
        nsweeps_ground_max=parse(Int, get(ENV, "EXP03_MPS_SWEEPS_GROUND_MAX", "120")),
        nsweeps_excited_max=parse(Int, get(ENV, "EXP03_MPS_SWEEPS_EXCITED_MAX", "120")),
        seed=parse(Int, get(ENV, "EXP03_MPS_SEED", "1234")))
end

function point_path(dir, L, s, p)
    config = join((string(k, "=", repr(getfield(p, k))) for k in fieldnames(MpsDMRGParams)), ";")
    runtime = mps_runtime()
    config *= join((string(k,"=",runtime[k]) for k in sort(collect(keys(runtime)))),";")
    id = bytes2hex(sha256(config))[1:12]
    return joinpath(dir, "points", "L$(L)_s$(round(Int,10000s))_chi$(p.chi)_$(id).json")
end

function obtain_point(dir, L, s, chi)
    p = params(chi)
    path = point_path(dir, L, s, p)
    if isfile(path)
        rec = open(JSON3.read, path)
        mps_record_matches(rec, L, s, p) || error("stale/incompatible result: $path")
        println("REUSE L=$L s=$s chi=$chi valid=$(mps_record_valid(rec))")
        return rec, path
    end
    println("START L=$L s=$s chi=$chi $(now())")
    flush(stdout)
    try
        r = solve_gap_mps(L, s, chi; params=p)
        save_mps_point_json(path, r)
        println("DONE L=$L s=$s chi=$chi valid=$(mps_point_valid(r)) " *
                "gap=$(r.delta_gap) drift=$(r.last_energy_change) wall=$(r.wall_seconds)s")
    catch err
        failure = Dict("schema" => MPS_SCHEMA, "method" => MPS_METHOD,
            "L" => L, "s" => s, "delta" => DELTA_FIXED, "chi" => chi,
            "valid" => false, "error" => sprint(showerror, err),
            "params" => mps_params_dict(p), "runtime" => mps_runtime(),
            "source_fingerprint" => mps_source_fingerprint())
        save_capacity_summary(path, failure)
        rethrow()
    end
    flush(stdout)
    return open(JSON3.read, path), path
end

function obtain_pair(dir, L, s, chi)
    low, lp = obtain_point(dir, L, s, chi)
    high, hp = obtain_point(dir, L, s, 2chi)
    pair = Dict("low" => low, "high" => high,
                "low_path" => relpath(lp, ROOT), "high_path" => relpath(hp, ROOT))
    mps_pair_valid(pair) || error("invalid/unconverged chi pair at L=$L s=$s chi=$chi/$(2chi)")
    return pair
end

function setup_workers(njobs)
    requested = parse(Int,get(ENV,"EXP03_MPS_WORKERS","24"))
    requested ≥ 1 || error("EXP03_MPS_WORKERS must be positive")
    count = min(requested,njobs,Sys.CPU_THREADS)
    println("parallel workers=$count, BLAS threads per worker=1")
    flush(stdout)
    if nprocs() == 1 && count > 1
        ids = addprocs(count; exeflags=`--project=$ROOT --startup-file=no --threads=1`,
                       env=["OPENBLAS_NUM_THREADS"=>"1","EXP03_MPS_BLAS_THREADS"=>"1"])
        for id in ids
            remotecall_wait(Base.include,id,Main,@__FILE__)
        end
    end
end

point_map(f,items) = nprocs() > 1 ? pmap(f,items; batch_size=1) : map(f,items)

function capacity()
    chis = parse.(Int, split(get(ENV, "EXP03_MPS_CHIS", "128,256,512"), ","))
    previous = nothing
    previous_path = nothing
    trials = Any[]
    pair = nothing
    setup_workers(min(2,length(chis)))
    batches = [chis[i:min(i+1,end)] for i in 1:2:length(chis)]
    for batch in batches
        computed = point_map(chi -> obtain_point(CAP_DIR,32,0.5,chi),batch)
        for (chi,(rec,path)) in zip(batch,computed)
            push!(trials,Dict("path"=>relpath(path,ROOT),"chi"=>chi,"valid"=>mps_record_valid(rec)))
            if previous !== nothing
                candidate = Dict("low"=>previous,"high"=>rec,
                    "low_path"=>relpath(previous_path,ROOT),"high_path"=>relpath(path,ROOT))
                if mps_pair_valid(candidate)
                    pair = candidate
                    break
                end
            end
            previous,previous_path = rec,path
        end
        pair === nothing || break
    end
    summary = Dict("schema" => MPS_SCHEMA, "L" => 32, "s" => 0.5,
        "source_fingerprint" => mps_source_fingerprint(), "trials" => trials,
        "feasible" => pair !== nothing, "pair" => pair,
        "completed_utc" => string(now(UTC)))
    save_capacity_summary(joinpath(CAP_DIR, "summary.json"), summary)
    pair === nothing && error("L=32 did not pass the tested chi ladder; production remains blocked")
    println("CAPACITY-EXP03-MPS-OK")
end

function ed_reference(L, s)
    if L ≤ 16
        r = solve_gap(L, s)
        return Dict("E0" => r.E0, "E1" => r.E1, "Delta" => r.delta_gap,
                    "source" => "ED recomputed with residual gate")
    elseif L == 24
        index = round(Int, 100s)
        ib = cld(index, BLOCK)
        path = Exp03._chunkpath(ED_DIR, L, ib)
        d = NPZ.npzread(path)
        i = findfirst(x -> abs(x - s) < 1e-12, vec(d["s"]))
        i === nothing && error("missing ED reference L=$L s=$s")
        return Dict("E0" => d["E0"][i], "E1" => d["E1"][i], "Delta" => d["Delta"][i],
                    "source" => relpath(path, ROOT), "sha256" => bytes2hex(sha256(read(path))))
    end
    L in (26, 28) && s == 0.5 || error("no ED reference for L=$L s=$s")
    d = open(JSON3.read, ED_REF_PATH)["L$L"]
    return Dict("E0" => d["E0"], "E1" => d["E1"], "Delta" => d["delta"],
                "source" => relpath(ED_REF_PATH, ROOT), "sha256" => bytes2hex(sha256(read(ED_REF_PATH))))
end

validation_points() = vcat([(L, Float64(s)) for L in (8,12,16) for s in s_grid_points()],
                            [(24, s) for s in (0.1,0.5,0.6,0.9)], [(26,0.5),(28,0.5)])

function validate_one(point)
    L,s = point
    pair = L in (26,28) ? obtain_pair(VAL_DIR,L,s,256) : nothing
    rec,path = pair === nothing ? obtain_point(VAL_DIR,L,s,512) :
               (pair["high"],joinpath(ROOT,pair["high_path"]))
    ref = ed_reference(L,s)
    tol = L in (26,28) ? MPS_L26_L28_GAP_TOL : MPS_ED_GAP_TOL
    diffs = Dict(k=>abs(rec[k]-ref[k]) for k in ("E0","E1","Delta") if haskey(rec,k))
    ok = mps_record_valid(rec) && length(diffs) == 3 && all(v < tol for v in values(diffs))
    result = Dict("L"=>L,"s"=>s,"path"=>relpath(path,ROOT),"reference"=>ref,
                  "differences"=>diffs,"valid"=>ok,"pair"=>pair)
    save_capacity_summary(joinpath(VAL_DIR,"comparisons","L$(L)_s$(round(Int,10000s)).json"),result)
    println("ED CHECK L=$L s=$s valid=$ok diffs=$diffs")
    flush(stdout)
    ok || error("ED/MPS validation failed at L=$L s=$s; comparison record was saved")
    return result
end

function validation(; scope="full")
    points = scope == "full" ? validation_points() :
             scope == "crosscheck" ? [(26,0.5),(28,0.5)] : [(8,0.5),(12,0.5),(16,0.5),(24,0.5)]
    setup_workers(length(points))
    records = point_map(validate_one,points)
    failures = ["ED/DMRG validation failed at L=$(r["L"]) s=$(r["s"])" for r in records if !r["valid"]]
    complete = scope == "full" && length(records) == length(validation_points()) && isempty(failures)
    summary = Dict("schema"=>MPS_SCHEMA,"scope"=>scope,"complete"=>complete,
        "source_fingerprint"=>mps_source_fingerprint(),"records"=>records,"failures"=>failures)
    save_capacity_summary(joinpath(VAL_DIR,scope == "full" ? "summary.json" : "$(scope)_summary.json"),summary)
    isempty(failures) || error(join(failures,"\n"))
    println(complete ? "VALIDATE-EXP03-MPS-OK" : "EXP03-MPS-SAMPLE-OK (full validation is pending)")
end

function require_full_validation()
    verifier = joinpath(ROOT,"scripts","verify_exp03_mps.jl")
    run(`$(Base.julia_cmd()) --project=$ROOT --startup-file=no $verifier $RUN_DIR`)
end

function production()
    require_full_validation()
    setup_workers(length(s_grid_points()))
    pairs = point_map(s -> obtain_pair(PROD_DIR,32,s,256),s_grid_points())
    nblocks = cld(length(pairs),MPS_BLOCK)
    for ib in 1:nblocks
        lo = (ib-1)*MPS_BLOCK+1
        hi = min(ib*MPS_BLOCK,length(pairs))
        save_mps_chunk_records(PROD_DIR,32,ib,pairs[lo:hi])
    end
    println("MPS production completed: $PROD_DIR")
end

function main()
    mode = get(ARGS,1,"capacity")
    println("exp03 CPU MPS mode=$mode | BLAS=$(BLAS.get_num_threads()) | run=$RUN_DIR")
    flush(stdout)
    if mode == "capacity"
        capacity()
    elseif mode in ("validate","smoke","crosscheck")
        validation(; scope=mode == "validate" ? "full" : mode)
    elseif mode == "production"
        production()
    elseif mode == "assemble"
        require_full_validation()
        candidate = joinpath(RUN_DIR,"paper-candidate")
        assemble_D02(candidate; ed_dir=ED_DIR,mps_dir=PROD_DIR,validation_dir=RUN_DIR)
        println("paper candidate: $candidate")
    else
        error("unknown mode: $mode")
    end
end

if abspath(PROGRAM_FILE) == (@__FILE__)
    try
        main()
    catch err
        save_capacity_summary(joinpath(RUN_DIR,"run-failure-$(get(ARGS,1,"capacity")).json"),
            Dict("mode"=>get(ARGS,1,"capacity"),"error"=>sprint(showerror,err),
                 "source_fingerprint"=>mps_source_fingerprint(),"created_utc"=>string(now(UTC))))
        rethrow()
    end
end
