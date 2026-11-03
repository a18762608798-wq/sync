# Independent diagnostic only: score delta=-2 against p=1, keeping the
# per-window endpoints pooled over both lines. Never overwrite joint products.
# Run: julia --project=. --startup-file=no scripts/diag_exp06_dm2_window.jl
# Add delta=0.85 on the saved window without reselecting it: append --companion.

using JSON3, NPZ, SHA, Statistics

function dm2_score(s_mean, o_mean, smax, omax, indices, q_ref)
    q = 4 / 3 .+ 2 .* o_mean[indices] ./ omax .-
        (4 / 3) .* s_mean[indices] ./ smax
    return (d_raw=mean(abs.(q .- q_ref)), r=cor(q, q_ref))
end

function better_dm2_window(candidate, best)
    isnothing(best) && return true
    candidate.r > best.r + 1e-12 && return true
    abs(candidate.r - best.r) <= 1e-12 || return false
    candidate.d_raw < best.d_raw - 1e-12 && return true
    abs(candidate.d_raw - best.d_raw) <= 1e-12 || return false
    candidate.length > best.length && return true
    return candidate.length == best.length && candidate.start < best.start
end

function search_dm2_window(s_units, o_units, indices, q_ref)
    n_units, n_points = size(s_units)
    cs = vcat(zeros(1, n_points), cumsum(s_units; dims=1))
    co = vcat(zeros(1, n_points), cumsum(o_units; dims=1))
    best = nothing
    n_candidates = 0
    for len in 10:2:n_units, start in 0:(n_units-len)
        sm = (cs[start+len+1, :] - cs[start+1, :]) / len
        om = (co[start+len+1, :] - co[start+1, :]) / len
        smax = maximum(sm)  # Both lines, not only the scored 15 points.
        omax = maximum(-om)
        omax = omax > 0 ? omax : 1e-12
        candidate = merge((start=start, length=len),
            dm2_score(sm, om, smax, omax, indices, q_ref),
            (S_max=smax, O_max=omax))
        better_dm2_window(candidate, best) && (best = candidate)
        n_candidates += 1
    end
    return best, n_candidates
end

function main()
    repo = normpath(joinpath(@__DIR__, ".."))
    source = joinpath(repo, "data", "exp06", "joint", "exp06_D08_joint.npz")
    formal = joinpath(repo, "data", "exp06", "joint", "exp06_manifest_joint.json")
    hashes = Dict(path => bytes2hex(sha256(read(path))) for path in (source, formal))
    processing = JSON3.read(read(formal, String))["readout_mitigation"]
    @assert processing["probability_repair"] == "euclidean-simplex-projection"
    data = npzread(source)
    s_units, o_units = data["s_post"], data["o_post"]
    indices = findall(x -> isapprox(x, -2.0; atol=1e-9), vec(data["deltas"]))
    @assert size(s_units) == size(o_units) == (500, 30)
    @assert length(indices) == 15
    @assert all(isfinite, s_units) && all(isfinite, o_units)
    ids = vec(data["unit_ids"])
    @assert all(diff(ids) .== 1)

    # Independently confirm the reference is the p=1 column of S06.
    s06 = npzread(joinpath(repo, "data", "exp04", "exp04_S06.npz"))
    rows = Int.(vec(data["s_idx"])[indices])
    q_ref = 4 / 3 .+ 2 .* s06["dm2_ostr"][rows, 1] .-
        (4 / 3) .* s06["dm2_spi"][rows, 1] ./ 8
    @assert isapprox(q_ref, vec(data["q_sim_p1"])[indices]; atol=1e-12)

    best, n_candidates = search_dm2_window(s_units, o_units, indices, q_ref)
    @assert 0 <= best.start && iseven(best.length) && best.length >= 10
    @assert best.start + best.length <= length(ids)
    window = (best.start+1):(best.start+best.length)
    sm = vec(mean(s_units[window, :]; dims=1))
    om = vec(mean(o_units[window, :]; dims=1))
    @assert isapprox(maximum(sm), best.S_max; atol=1e-12)
    @assert isapprox(maximum(-om), best.O_max; atol=1e-12)
    q_units = 4 / 3 .+ 2 .* o_units[window, indices] ./ best.O_max .-
        (4 / 3) .* s_units[window, indices] ./ best.S_max
    q_mean = vec(mean(q_units; dims=1))
    q_se = vec(std(q_units; dims=1, corrected=true)) ./ sqrt(best.length)
    @assert isapprox(cor(q_mean, q_ref), best.r; atol=1e-12)
    @assert isapprox(mean(abs.(q_mean .- q_ref)), best.d_raw; atol=1e-12)

    d09 = npzread(joinpath(repo, "data", "exp04", "exp04_D09.npz"))
    @assert isapprox(vec(d09["s_grid"])[rows], vec(data["s_grid"])[indices])
    phases = Int.(d09["phase"][rows, 1])
    outdir = joinpath(repo, "data", "exp06", "diagnostics", "dm2_window")
    mkpath(outdir)
    npzwrite(joinpath(outdir, "dm2_window.npz"), Dict(
        "s_grid" => vec(data["s_grid"])[indices],
        "q_sim_p1" => q_ref,
        "q_sim_p2" => vec(data["q_sim_p2"])[indices],
        "win_mean" => q_mean, "win_se" => q_se,
        "q_units" => q_units, "unit_ids" => ids[window], "phase" => phases,
    ))
    manifest = Dict(
        "diagnostic_only" => true, "delta" => -2.0,
        "reference_p" => 1, "n_units_total" => length(ids),
        "scored_points" => length(indices), "n_candidates" => n_candidates,
        "endpoint_points" => 30,
        "endpoint_rule" => "top1-max-pooled-window-both-lines",
        "ranking" => ["r descending", "d_raw ascending", "length descending", "start ascending"],
        "window" => Dict(string(k) => v for (k, v) in pairs(best)),
        "window_indexing" => "zero-based half-open",
        "window_stop" => best.start + best.length,
        "stderr_def" => "inter-unit sample standard deviation / sqrt(window length); endpoints held fixed",
        "readout_mitigation" => processing,
        "sources_sha256" => Dict(replace(relpath(k, repo), '\\' => '/') => v
                                  for (k, v) in hashes),
    )
    open(joinpath(outdir, "manifest.json"), "w") do io
        JSON3.pretty(io, manifest)
    end
    @assert all(bytes2hex(sha256(read(path))) == hash for (path, hash) in hashes)
    println("dm2 diagnostic: ", best, "; candidates=", n_candidates)
    println("Saved diagnostic data; formal joint data and manifest unchanged.")
end

function fixed_window_companion()
    repo = normpath(joinpath(@__DIR__, ".."))
    outdir = joinpath(repo, "data", "exp06", "diagnostics", "dm2_window")
    parent_path = joinpath(outdir, "manifest.json")
    parent = JSON3.read(read(parent_path, String))
    @assert parent["diagnostic_only"] && parent["reference_p"] == 1
    @assert parent["delta"] == -2 && parent["endpoint_points"] == 30
    for (relative, expected) in pairs(parent["sources_sha256"])
        @assert bytes2hex(sha256(read(joinpath(repo, String(relative))))) == expected
    end
    parent_hash = bytes2hex(sha256(read(parent_path)))
    source = joinpath(repo, "data", "exp06", "joint", "exp06_D08_joint.npz")
    data = npzread(source)
    s_units, o_units = data["s_post"], data["o_post"]
    indices = findall(x -> isapprox(x, 0.85; atol=1e-9), vec(data["deltas"]))
    @assert size(s_units) == size(o_units) == (500, 30)
    @assert length(indices) == 15
    win = parent["window"]
    start, len = Int(win["start"]), Int(win["length"])
    @assert 0 <= start && iseven(len) && len >= 10
    @assert Int(parent["window_stop"]) == start + len <= size(s_units, 1)
    window = (start+1):(start+len)
    smax, omax = Float64(win["S_max"]), Float64(win["O_max"])
    sm = vec(mean(s_units[window, :]; dims=1))
    om = vec(mean(o_units[window, :]; dims=1))
    @assert isapprox(maximum(sm), smax; atol=1e-12)
    @assert isapprox(maximum(-om), omax; atol=1e-12)

    s06 = npzread(joinpath(repo, "data", "exp04", "exp04_S06.npz"))
    rows = Int.(vec(data["s_idx"])[indices])
    q_ref = 4 / 3 .+ 2 .* s06["d085_ostr"][rows, 1] .-
        (4 / 3) .* s06["d085_spi"][rows, 1] ./ 8
    @assert isapprox(q_ref, vec(data["q_sim_p1"])[indices]; atol=1e-12)
    q_units = 4 / 3 .+ 2 .* o_units[window, indices] ./ omax .-
        (4 / 3) .* s_units[window, indices] ./ smax
    q_mean = vec(mean(q_units; dims=1))
    q_se = vec(std(q_units; dims=1, corrected=true)) ./ sqrt(len)
    score = dm2_score(sm, om, smax, omax, indices, q_ref)
    @assert isapprox(cor(q_mean, q_ref), score.r; atol=1e-12)
    @assert isapprox(mean(abs.(q_mean .- q_ref)), score.d_raw; atol=1e-12)
    d09 = npzread(joinpath(repo, "data", "exp04", "exp04_D09.npz"))
    @assert isapprox(vec(d09["deltas"]), [-2.0, 0.85])
    @assert isapprox(vec(d09["s_grid"])[rows], vec(data["s_grid"])[indices])
    ids = vec(data["unit_ids"])[window]
    @assert ids == collect(start:(start+len-1))
    npzwrite(joinpath(outdir, "d085_same_window.npz"), Dict(
        "s_grid" => vec(data["s_grid"])[indices],
        "q_sim_p1" => q_ref, "q_sim_p2" => vec(data["q_sim_p2"])[indices],
        "win_mean" => q_mean, "win_se" => q_se, "q_units" => q_units,
        "unit_ids" => ids, "phase" => Int.(d09["phase"][rows, 2]),
    ))
    manifest = Dict(
        "diagnostic_only" => true, "delta" => 0.85, "reference_p" => 1,
        "n_units_total" => size(s_units, 1), "scored_points" => 15,
        "endpoint_points" => 30, "endpoint_rule" => parent["endpoint_rule"],
        "window_selected_on_delta" => -2.0, "window_reselected" => false,
        "window_indexing" => parent["window_indexing"], "window_stop" => start+len,
        "window" => Dict("start" => start, "length" => len, "S_max" => smax,
                         "O_max" => omax, "r" => score.r, "d_raw" => score.d_raw),
        "stderr_def" => parent["stderr_def"],
        "readout_mitigation" => parent["readout_mitigation"],
        "sources_sha256" => Dict(String(k) => String(v)
                                  for (k, v) in pairs(parent["sources_sha256"])),
        "selection_manifest" => "data/exp06/diagnostics/dm2_window/manifest.json",
        "selection_manifest_sha256" => parent_hash,
    )
    open(joinpath(outdir, "d085_same_window_manifest.json"), "w") do io
        JSON3.pretty(io, manifest)
    end
    @assert bytes2hex(sha256(read(parent_path))) == parent_hash
    for (relative, expected) in pairs(parent["sources_sha256"])
        @assert bytes2hex(sha256(read(joinpath(repo, String(relative))))) == expected
    end
    println("d085 fixed dm2 window: [", start, ",", start+len, "); ", score)
    println("Same ", len, " units and shared endpoints; no window search or formal writes.")
end

if isempty(ARGS)
    main()
elseif ARGS == ["--companion"]
    fixed_window_companion()
else
    error("usage: diag_exp06_dm2_window.jl [--companion]")
end
