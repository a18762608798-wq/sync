# Independently recheck saved MPS diagnostics and ED references.
# Usage: julia --project=. scripts/verify_exp03_mps.jl [run-directory] [--sample]
include(joinpath(@__DIR__, "run_exp03_mps.jl"))

function checked_point(path, L, s)
    isfile(path) || error("missing MPS evidence: $path")
    rec = open(JSON3.read,path)
    mps_record_matches(rec,L,s,params(Int(rec["chi"]))) || error("stale/configuration mismatch: $path")
    mps_record_valid(rec) || error("invalid MPS evidence: $path")
    return rec
end

function checked_pair(pair, L, s)
    pair === nothing && error("missing chi-pair evidence at L=$L s=$s")
    low = checked_point(joinpath(ROOT,pair["low_path"]),L,s)
    high = checked_point(joinpath(ROOT,pair["high_path"]),L,s)
    mps_pair_valid(Dict("low"=>low,"high"=>high)) || error("chi convergence failed at L=$L s=$s")
end

function verify_main()
    positional = filter(x -> !startswith(x,"--"),ARGS)
    dir = isempty(positional) ? RUN_DIR : abspath(positional[1])
    sample = "--sample" in ARGS
    summary_path = joinpath(dir,"validation",sample ? "smoke_summary.json" : "summary.json")
    summary = open(JSON3.read,summary_path)
    summary["source_fingerprint"] == mps_source_fingerprint() || error("stale validation summary")
    if !sample
        summary["scope"] == "full" && summary["complete"] === true || error("full validation incomplete")
    end
    records = summary["records"]
    seen = Set{Tuple{Int,Float64}}()
    for item in records
        L,s = Int(item["L"]),Float64(item["s"])
        (L,s) in seen && error("duplicate validation point L=$L s=$s")
        push!(seen,(L,s))
        rec = checked_point(joinpath(ROOT,item["path"]),L,s)
        ref = ed_reference(L,s)
        tol = L in (26,28) ? MPS_L26_L28_GAP_TOL : MPS_ED_GAP_TOL
        for k in ("E0","E1","Delta")
            abs(rec[k]-ref[k]) < tol || error("ED comparison failed L=$L s=$s $k")
        end
        L in (26,28) && checked_pair(item["pair"],L,s)
    end
    if sample
        isempty(seen) && error("empty sample validation")
        println("VERIFY-EXP03-MPS-SAMPLE-OK: $(length(seen)) points; full validation remains pending")
        return
    end
    seen == Set(validation_points()) || error("validation coverage does not match PRE-006/VAL-008")
    cap = open(JSON3.read,joinpath(dir,"capacity","summary.json"))
    cap["source_fingerprint"] == mps_source_fingerprint() || error("stale capacity summary")
    cap["feasible"] === true && cap["L"] == 32 && cap["s"] == 0.5 || error("L=32 capacity not passed")
    checked_pair(cap["pair"],32,0.5)
    println("VERIFY-EXP03-MPS-OK: full ED validation and L=32 capacity passed")
end

abspath(PROGRAM_FILE) == (@__FILE__) && verify_main()
