# Current four-size D02 checks; --legacy checks the retained five-size ED baseline.
push!(LOAD_PATH,joinpath(@__DIR__,"..","src"))
using LinearAlgebra, NPZ, JSON3, SHA
BLAS.set_num_threads(1)
using Exp03

const DATA_DIR = get(ENV,"EXP03_DATA_DIR",joinpath(@__DIR__,"..","data","exp03"))

function main()
    legacy = "--legacy" in ARGS
    ls = collect(legacy ? ED_LS : PAPER_LS)
    d = NPZ.npzread(joinpath(DATA_DIR,D02_NPZ_NAME))
    manifest = open(JSON3.read,joinpath(DATA_DIR,MANIFEST_NAME))
    @assert manifest["schema"] == SCHEMA
    @assert manifest["H_def"] == H_DEF_ID
    @assert manifest["delta"] == DELTA_FIXED
    @assert vec(d["Ls"]) == ls "D02 sizes do not match the current paper; use --legacy only for historical ED evidence"
    s,D = vec(d["s_grid"]),d["Delta"]
    @assert s == Float64.(s_grid_points())
    @assert size(D) == (length(ls),99)
    @assert all(isfinite,D) && minimum(D) ≥ GAP_MIN_TOL
    for (row,L) in enumerate(ls)
        if L in ED_LS
            @assert manifest["sector_dims"][string(L)] == length(sector_basis(L).members)
        end
        if !legacy
            offset = 0
            method = manifest["methods"][row]
            @assert method == (L in ED_LS ? "ed-arpack" : MPS_METHOD)
            for source in manifest["sources"][string(L)]
                path = String(source["path"])
                @assert bytes2hex(sha256(read(path))) == source["sha256"]
                if L in ED_LS
                    chunk = NPZ.npzread(path)
                    ss,ds = vec(chunk["s"]),vec(chunk["Delta"])
                else
                    detail = open(JSON3.read,path)
                    @assert all(mps_pair_valid,detail["pairs"])
                    ss = [p["high"]["s"] for p in detail["pairs"]]
                    ds = [p["high"]["Delta"] for p in detail["pairs"]]
                    for p in detail["pairs"], key in ("low","high")
                        @assert p[key]["source_fingerprint"] == mps_source_fingerprint()
                        @assert p[key]["L"] == L && p[key]["delta"] == DELTA_FIXED
                    end
                end
                tail = offset + length(ss)
                @assert Float64.(ss) == s[(offset+1):tail]
                @assert Float64.(ds) == D[row,(offset+1):tail]
                offset = tail
            end
            @assert offset == length(s)
        end
    end
    xs,ys = 1.0 ./ ls,D[:,50]
    @assert vec(d["fit_x"]) == xs && vec(d["fit_y"]) == ys
    fit = quadratic_fit(xs,ys)
    for k in (:a,:b,:c)
        @assert abs(getfield(fit,k)-d["fit_$k"][]) < FIT_TOL
    end
    window = findall(x -> 0.52-1e-12 ≤ x ≤ 0.65+1e-12,s)
    @assert length(window) == 14
    if !legacy
        vd = String(manifest["validation_dir"])
        run(`$(Base.julia_cmd()) --project=$(dirname(Base.active_project())) --startup-file=no $(joinpath(@__DIR__,"verify_exp03_mps.jl")) $vd`)
    end
    println(legacy ? "VERIFY-EXP03-LEGACY-ED-OK (current four-size result is pending)" : "VERIFY-EXP03-OK")
end

main()
