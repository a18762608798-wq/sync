# Matched-budget diagnostic of uniform versus reflection-orbit XXZ angles.
# Uses archived S01 states and the existing Exp04 circuit/gradient; never writes
# formal S06/S03 products. Usage: julia --project=. -t 6 SCRIPT OUTPUT_DIR
push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra, Random, Optim, NPZ, JSON3, SHA, Dates
using Shared01, Exp04
BLAS.set_num_threads(1)

const AUDIT_ROOT = normpath(joinpath(@__DIR__, ".."))
const AUDIT_SEED = 20261105
const AUDIT_SAMPLES = 64
const AUDIT_STARTS = 4
const AUDIT_PASSES = 2
const AUDIT_ITERATIONS = 1000

function save_record(path, record)
    mkpath(dirname(path))
    temporary = path * ".tmp"
    open(io -> JSON3.write(io, record), temporary, "w")
    mv(temporary, path; force=true)
end

function sharing_map(p, family)
    family == "orbit" && return collect(1:8p)
    family == "uniform" || error("unknown sharing family: $family")
    return [4(l - 1) + j for l in 1:p for j in (1, 2, 1, 2, 3, 4, 3, 4)]
end

function objective(H, initial, meta, p, delta, family)
    mapping = sharing_map(p, family)
    expanded = zeros(8p)
    full_gradient = similar(expanded)
    buffer = similar(initial)
    schedule = bond_schedule(meta, delta, p)
    workspace = make_gradwork(meta, p, delta)
    function expand!(parameters)
        for j in eachindex(mapping)
            expanded[j] = parameters[mapping[j]]
        end
        return expanded
    end
    f(parameters) = energy_of(expand!(parameters), H, initial, meta, p, delta, buffer)
    function g!(gradient, parameters)
        adjoint_gradient!(full_gradient, expand!(parameters), H, initial, meta,
                          p, delta, schedule, workspace)
        fill!(gradient, 0)
        for j in eachindex(mapping)
            gradient[mapping[j]] += full_gradient[j]
        end
        return gradient
    end
    return f, g!, mapping
end

function verify_gradients(reference)
    H, _, _, target = reference
    initial = psi_init("triv", 8)
    meta = build_meta(8, "triv")
    rng = MersenneTwister(AUDIT_SEED)
    records = []
    for p in (1, 2)
        _, g!, mapping = objective(H, initial, meta, p, -2.0, "uniform")
        parameters = rand(rng, 4p)
        gradient = zeros(4p)
        g!(gradient, parameters)
        full = pshift_gradient(parameters[mapping], H, initial, meta, p, -2.0,
                               similar(target))
        expected = zeros(4p)
        for j in eachindex(mapping)
            expected[mapping[j]] += full[j]
        end
        discrepancy = maximum(abs.(gradient .- expected))
        @assert discrepancy < 1e-7
        push!(records, (; p, max_gradient_difference=discrepancy))
    end
    return records
end

function run_job(job, reference, directory, fingerprint)
    delta, s, p, leg, family, seed = job
    file = joinpath(directory, "points", "d$(round(Int, 100delta))_s$(round(Int, 100s))_p$(p)_$(leg)_$(family).json")
    if isfile(file)
        record = open(JSON3.read, file)
        record["fingerprint"] == fingerprint || error("resume fingerprint mismatch")
        return record
    end
    started = time()
    H, e0, gap, target = reference
    initial = psi_init(leg, 8)
    meta = build_meta(8, leg)
    f, g!, mapping = objective(H, initial, meta, p, delta, family)
    n = maximum(mapping)
    rng = MersenneTwister(seed)
    candidates = [zeros(n)]
    append!(candidates, [4pi .* rand(rng, n) for _ in 1:AUDIT_SAMPLES])
    sample_energies = f.(candidates)
    selected = sortperm(sample_energies)[1:AUDIT_STARTS]
    options = Optim.Options(g_tol=Exp04.G_TOL, x_abstol=Exp04.X_TOL,
                            f_abstol=Exp04.F_TOL, iterations=AUDIT_ITERATIONS)
    refinements = Any[]
    for index in selected
        parameters = copy(candidates[index])
        passes = Any[]
        for pass in 1:AUDIT_PASSES
            result = optimize(f, g!, parameters, LBFGS(), options)
            parameters = Vector{Float64}(Optim.minimizer(result))
            gradient = zeros(n)
            g!(gradient, parameters)
            converged = Optim.converged(result) || norm(gradient) < Exp04.G_TOL
            state = similar(initial)
            apply_circuit!(state, initial, parameters[mapping], meta, p, delta)
            energy = real(dot(state, H * state))
            fidelity = abs2(dot(target, state))
            norm_error = abs(norm(state) - 1)
            ztot2 = sum(abs2(state[b + 1]) * (8 - 2count_ones(UInt(b)))^2 for b in 0:255)
            spinflip_error = abs(overlap_xbar(state, 8) - 1)
            reflection_error = abs(overlap_reflect(state, 8) - 1)
            @assert norm_error < 1e-8 && ztot2 < 1e-8
            @assert spinflip_error < 1e-8 && reflection_error < 1e-8
            @assert energy >= e0 - 1e-9 && abs(energy - f(parameters)) < 1e-10
            @assert -1e-10 <= fidelity <= 1 + 1e-10
            push!(passes, (; pass, theta=copy(parameters), energy,
                energy_error=energy-e0, fidelity, converged,
                gradient_norm=norm(gradient), iterations=Optim.iterations(result),
                f_calls=Optim.f_calls(result), g_calls=Optim.g_calls(result),
                x_converged=Optim.x_converged(result),
                f_converged=Optim.f_converged(result),
                g_converged=Optim.g_converged(result), norm_error, ztot2,
                spinflip_error, reflection_error))
            converged && break
        end
        accepted = [r for r in passes if r.converged]
        best = isempty(accepted) ? nothing : accepted[argmin([r.energy for r in accepted])]
        push!(refinements, (; sample_index=index, sample_energy=sample_energies[index],
                            passes, best))
    end
    accepted = [r.best for r in refinements if r.best !== nothing]
    best = isempty(accepted) ? nothing : accepted[argmin([r.energy for r in accepted])]
    record = (; fingerprint, delta, s, p, leg, family, seed, nparameters=n,
               e0, exact_gap=gap, target="archived S01 normalized ground state",
               nsamples=length(candidates), nstarts=AUDIT_STARTS, refinements,
               valid=best !== nothing, best, wall_seconds=time()-started)
    save_record(file, record)
    println("DONE delta=$delta s=$s p=$p leg=$leg family=$family valid=$(record.valid)",
            best === nothing ? "" : " F=$(best.fidelity) dE=$(best.energy_error)")
    flush(stdout)
    return record
end

function main()
    length(ARGS) == 1 || error("pass an output directory")
    directory = abspath(ARGS[1])
    config = (; L=8, deltas=[-2.0,0.85], s_values=[0.15,0.5,0.85],
              depths=[1,2], legs=["triv","topo","afm"], families=["uniform","orbit"],
              seed=AUDIT_SEED, samples=AUDIT_SAMPLES, starts=AUDIT_STARTS,
              max_passes=AUDIT_PASSES, max_iterations_per_pass=AUDIT_ITERATIONS,
              g_tol=Exp04.G_TOL, x_tol=Exp04.X_TOL, f_tol=Exp04.F_TOL,
              objective="energy", fidelity="squared overlap with archived S01 ground state")
    paths = [@__FILE__, joinpath(AUDIT_ROOT,"src/Exp04/Ansatz.jl"),
             joinpath(AUDIT_ROOT,"src/Exp04/VQELoop.jl"),
             joinpath(AUDIT_ROOT,"src/Exp04/InitStates.jl"),
             joinpath(AUDIT_ROOT,"src/Shared01/Hamiltonian.jl"),
             joinpath(AUDIT_ROOT,"data/shared01/shared01_S01.npz")]
    sources = [(path=relpath(path,AUDIT_ROOT), sha256=bytes2hex(sha256(read(path)))) for path in paths]
    fingerprint = bytes2hex(sha256(JSON3.write((; config, sources))))
    manifest = (; config, sources, fingerprint, julia_version=string(VERSION),
                optim_version=string(Base.pkgversion(Optim)),
                julia_threads=Threads.nthreads(), blas_threads=BLAS.get_num_threads(),
                created_utc=string(now(UTC)))
    manifest_path = joinpath(directory,"manifest.json")
    if isfile(manifest_path)
        open(JSON3.read,manifest_path)["fingerprint"] == fingerprint || error("configuration changed")
    else
        save_record(manifest_path,manifest)
    end
    archive = NPZ.npzread(joinpath(AUDIT_ROOT,"data/shared01/shared01_S01.npz"))
    references = Dict()
    reference_checks = Any[]
    for delta in config.deltas, s in config.s_values
        e0,e1,target = point_at(archive,s,delta)
        H = build_hamiltonian(8,s,delta)
        residual = norm(H*target-e0*target)
        @assert residual < 1e-9 && abs(norm(target)-1) < 1e-10
        @assert e1-e0 > 1e-8 "use nondegenerate archived targets"
        references[(delta,s)] = (H,e0,e1-e0,target)
        push!(reference_checks,(;delta,s,e0,gap=e1-e0,residual))
    end
    gradients = verify_gradients(references[(-2.0,0.5)])
    save_record(joinpath(directory,"validation.json"),(; fingerprint, reference_checks, gradients))
    println("REFERENCE-AND-GRADIENT-OK")
    flush(stdout)
    jobs = NamedTuple[]
    for (di,delta) in enumerate(config.deltas), (si,s) in enumerate(config.s_values),
        p in config.depths, (li,leg) in enumerate(config.legs), family in config.families
        seed = AUDIT_SEED + 100000di + 10000si + 100p + li
        push!(jobs,(;delta,s,p,leg,family,seed))
    end
    Threads.@threads :dynamic for i in eachindex(jobs)
        job = jobs[i]
        run_job(job,references[(job.delta,job.s)],directory,fingerprint)
    end
    records = [open(JSON3.read,path) for path in sort(readdir(joinpath(directory,"points");join=true)) if endswith(path,".json")]
    @assert length(records)==72 && all(r->r["valid"],records)
    lookup = Dict((Float64(r["delta"]),Float64(r["s"]),Int(r["p"]),String(r["leg"]),String(r["family"]))=>r for r in records)
    comparisons = Any[]
    for delta in config.deltas, s in config.s_values, p in config.depths, leg in config.legs
        uniform = lookup[(delta,s,p,leg,"uniform")]["best"]
        orbit = lookup[(delta,s,p,leg,"orbit")]["best"]
        push!(comparisons,(;delta,s,p,leg,uniform_fidelity=uniform["fidelity"],
            orbit_fidelity=orbit["fidelity"],fidelity_change=orbit["fidelity"]-uniform["fidelity"],
            uniform_energy_error=uniform["energy_error"],orbit_energy_error=orbit["energy_error"]))
    end
    summary = (;fingerprint, complete=true, optimizations=length(records), comparisons,
        fidelity_improved=count(r->r.fidelity_change>1e-8,comparisons),
        fidelity_tied=count(r->abs(r.fidelity_change)<=1e-8,comparisons),
        fidelity_lower=count(r->r.fidelity_change < -1e-8,comparisons))
    save_record(joinpath(directory,"summary.json"),summary)
    println("SHARING-COMPARISON-OK jobs=72 improved=$(summary.fidelity_improved) tied=$(summary.fidelity_tied) lower=$(summary.fidelity_lower)")
end

main()
