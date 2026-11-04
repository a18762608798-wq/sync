# Execution calibration only; no D02 points are published by this script.
# Compare identical validated L=16 tasks at 24/32/48 single-thread workers.
push!(LOAD_PATH,joinpath(@__DIR__,"..","src"))
using Distributed, LinearAlgebra, JSON3, Dates, SHA
BLAS.set_num_threads(1)
using Exp03
const BENCH_ROOT = normpath(joinpath(@__DIR__,".."))

function benchmark_warmup()
    r = solve_gap_mps(6,0.5,64)
    mps_point_valid(r) || error("benchmark warm-up failed scientific gates")
    return nothing
end

function benchmark_point(job,dir)
    index,s,ref = job
    r = solve_gap_mps(16,s,128)
    valid = mps_point_valid(r) && maximum(abs.([r.E0-ref[1],r.E1-ref[2],r.delta_gap-ref[3]])) < MPS_ED_GAP_TOL
    result = Dict("index"=>index,"L"=>16,"s"=>s,"chi"=>128,"valid"=>valid,
        "wall_seconds"=>r.wall_seconds,"peak_rss_mib"=>r.peak_rss_mib,
        "E0"=>r.E0,"E1"=>r.E1,"Delta"=>r.delta_gap,
        "reference"=>ref,"runtime"=>mps_runtime(),"diagnostics"=>mps_point_dict(r))
    save_capacity_summary(joinpath(dir,"point_$(index).json"),result)
    valid || error("benchmark task $index failed ED/convergence checks")
    return result
end

function benchmark_main()
    stamp = Dates.format(now(),"yyyymmdd-HHMMSS")
    out = get(ENV,"EXP03_MPS_BENCH_DIR",joinpath(BENCH_ROOT,"data","validation","exp03-mps-parallel-"*stamp))
    counts = parse.(Int,split(get(ENV,"EXP03_MPS_BENCH_WORKERS","24,32,48"),","))
    n = parse(Int,get(ENV,"EXP03_MPS_BENCH_POINTS","96"))
    ss = (0.1,0.3,0.5,0.6,0.8,0.9)
    refs = Dict(s=>let e=solve_gap(16,s); [e.E0,e.E1,e.delta_gap]; end for s in ss)
    jobs = [(i,ss[mod1(i,length(ss))],refs[ss[mod1(i,length(ss))]]) for i in 1:n]
    results = Any[]
    for count in counts
        count ≤ Sys.CPU_THREADS || error("worker count exceeds available logical CPUs")
        dir = joinpath(out,"workers_$count")
        ids = addprocs(count; exeflags=`--project=$BENCH_ROOT --startup-file=no --threads=1`,
                       env=["OPENBLAS_NUM_THREADS"=>"1"])
        @sync for id in ids
            @async remotecall_wait(Base.include,id,Main,@__FILE__)
        end
        @sync for id in ids
            @async remotecall_wait(benchmark_warmup,id)
        end
        println("BENCH START workers=$count tasks=$n $(now())")
        flush(stdout)
        elapsed = @elapsed records = pmap(job->benchmark_point(job,dir),jobs; batch_size=1)
        summary = Dict("workers"=>count,"points"=>n,"elapsed_seconds"=>elapsed,
            "points_per_second"=>n/elapsed,"all_valid"=>all(r["valid"] for r in records),
            "max_single_process_rss_mib"=>maximum(r["peak_rss_mib"] for r in records),
            "source_fingerprint"=>mps_source_fingerprint(),"completed_utc"=>string(now(UTC)),
            "benchmark_script_sha256"=>bytes2hex(sha256(read(@__FILE__))),
            "solver_params"=>mps_params_dict(mps_params(128)))
        # RSS above is reported per result; use a conservative count*max bound.
        summary["conservative_worker_rss_bound_mib"] = count*summary["max_single_process_rss_mib"]
        save_capacity_summary(joinpath(dir,"summary.json"),summary)
        push!(results,summary)
        save_capacity_summary(joinpath(out,"summary.json"),Dict("results"=>results,"calibration_L"=>16,
            "same_tasks_all_configurations"=>true,"startup_and_warmup_excluded"=>true))
        println("BENCH DONE workers=$count elapsed=$(round(elapsed;digits=2))s rate=$(n/elapsed) points/s")
        flush(stdout)
        rmprocs(ids)
    end
    println("parallel calibration: $out")
end

if abspath(PROGRAM_FILE) == (@__FILE__)
    benchmark_main()
end
