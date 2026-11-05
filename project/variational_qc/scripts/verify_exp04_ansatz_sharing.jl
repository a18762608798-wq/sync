# Independently reread the matched-sharing experiment and optionally publish D11.
# Usage: julia --project=. SCRIPT RUN_DIR [--publish]
push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra, NPZ, JSON3, SHA, Dates
using Shared01, Exp04
BLAS.set_num_threads(1)

function write_product(path, value)
    mkpath(dirname(path))
    open(io -> JSON3.write(io, value), path * ".tmp", "w")
    mv(path * ".tmp", path; force=true)
end

function main()
    isempty(ARGS) && error("pass RUN_DIR [--publish]")
    root = normpath(joinpath(@__DIR__, ".."))
    directory = abspath(ARGS[1])
    manifest = open(JSON3.read, joinpath(directory, "manifest.json"))
    summary = open(JSON3.read, joinpath(directory, "summary.json"))
    config = manifest.config
    @assert config.L == 8 && config.objective == "energy"
    @assert Float64.(config.deltas) == [-2.0, 0.85]
    @assert Float64.(config.s_values) == [0.15, 0.5, 0.85]
    @assert Int.(config.depths) == [1, 2]
    @assert config.samples == 64 && config.starts == 4
    @assert config.max_passes == 2 && config.max_iterations_per_pass == 1000
    @assert summary.complete && summary.optimizations == 72
    @assert summary.fingerprint == manifest.fingerprint
    for source in manifest.sources
        @assert bytes2hex(sha256(read(joinpath(root, source.path)))) == source.sha256
    end
    archive = NPZ.npzread(joinpath(root, "data/shared01/shared01_S01.npz"))
    records = [open(JSON3.read, path) for path in sort(readdir(joinpath(directory, "points"); join=true)) if endswith(path, ".json")]
    @assert length(records) == 72
    lookup = Dict()
    checked_passes = 0
    max_energy_difference = max_fidelity_difference = 0.0
    for record in records
        delta, s, p = Float64(record.delta), Float64(record.s), Int(record.p)
        leg, family = String(record.leg), String(record.family)
        key = (delta, s, p, leg, family)
        @assert !haskey(lookup, key) && record.valid
        @assert record.fingerprint == manifest.fingerprint
        @assert record.nsamples == 65 && record.nstarts == 4
        mapping = family == "uniform" ? [4(l-1)+j for l in 1:p for j in (1,2,1,2,3,4,3,4)] : collect(1:8p)
        @assert record.nparameters == maximum(mapping)
        H = build_hamiltonian(8, s, delta)
        e0, e1, target = point_at(archive, s, delta)
        @assert norm(H*target-e0*target) < 1e-9 && e1-e0 > 1e-8
        initial, meta = psi_init(leg, 8), build_meta(8, leg)
        accepted_energies = Float64[]
        for refinement in record.refinements
            @assert length(refinement.passes) <= 2
            for pass in refinement.passes
                parameters = Float64.(pass.theta)
                @assert length(parameters) == maximum(mapping) && all(isfinite, parameters)
                state = similar(initial)
                apply_circuit!(state, initial, parameters[mapping], meta, p, delta)
                energy, fidelity = real(dot(state, H*state)), abs2(dot(target, state))
                de, df = abs(energy-pass.energy), abs(fidelity-pass.fidelity)
                @assert de < 1e-10 && df < 1e-12
                @assert energy >= e0-1e-9 && -1e-10 <= fidelity <= 1+1e-10
                @assert abs(norm(state)-1) < 1e-8
                @assert sum(abs2(state[b+1])*(8-2count_ones(UInt(b)))^2 for b in 0:255) < 1e-8
                @assert abs(overlap_xbar(state,8)-1) < 1e-8
                @assert abs(overlap_reflect(state,8)-1) < 1e-8
                @assert pass.iterations <= 1000
                @assert !pass.converged || pass.x_converged || pass.f_converged || pass.g_converged || pass.gradient_norm < config.g_tol
                pass.converged && push!(accepted_energies, energy)
                max_energy_difference = max(max_energy_difference, de)
                max_fidelity_difference = max(max_fidelity_difference, df)
                checked_passes += 1
            end
        end
        @assert !isempty(accepted_energies) && record.best.converged
        @assert abs(record.best.energy-minimum(accepted_energies)) < 1e-10
        matching = [pass for refinement in record.refinements for pass in refinement.passes if pass.converged && pass.theta == record.best.theta]
        @assert !isempty(matching) && abs(matching[1].fidelity-record.best.fidelity) < 1e-12
        lookup[key] = record
    end
    for delta in config.deltas, s in config.s_values, p in config.depths,
        leg in config.legs, family in config.families
        @assert haskey(lookup, (Float64(delta),Float64(s),Int(p),String(leg),String(family)))
    end
    validation = open(JSON3.read, joinpath(directory, "validation.json"))
    @assert length(validation.reference_checks) == 6 && length(validation.gradients) == 2
    @assert all(r->r.residual < 1e-9, validation.reference_checks)
    @assert all(r->r.max_gradient_difference < 1e-7, validation.gradients)
    paired = Any[]
    equal_parameters = Any[]
    winners = Any[]
    for delta in config.deltas, s in config.s_values, p in config.depths, leg in config.legs
        a,b = (lookup[(Float64(delta),Float64(s),Int(p),String(leg),family)] for family in ("uniform","orbit"))
        push!(paired,(;delta,s,p,leg,uniform_fidelity=a.best.fidelity,
            orbit_fidelity=b.best.fidelity,fidelity_change=b.best.fidelity-a.best.fidelity,
            uniform_energy_error=a.best.energy_error,orbit_energy_error=b.best.energy_error))
    end
    for delta in config.deltas, s in config.s_values, leg in config.legs
        a = lookup[(Float64(delta),Float64(s),2,String(leg),"uniform")]
        b = lookup[(Float64(delta),Float64(s),1,String(leg),"orbit")]
        @assert a.nparameters == b.nparameters == 8
        push!(equal_parameters,(;delta,s,leg,nparameters=8,uniform_p=2,orbit_p=1,
            uniform_fidelity=a.best.fidelity,orbit_fidelity=b.best.fidelity,
            fidelity_change=b.best.fidelity-a.best.fidelity))
    end
    for delta in config.deltas, s in config.s_values, p in config.depths, family in config.families
        pool = [lookup[(Float64(delta),Float64(s),Int(p),String(leg),String(family))] for leg in config.legs]
        selected = pool[argmin([r.best.energy for r in pool])]
        push!(winners,(;delta,s,p,family,leg=selected.leg,energy=selected.best.energy,
                       energy_error=selected.best.energy_error,fidelity=selected.best.fidelity))
    end
    verification = (;complete=true,tasks=length(records),checked_passes,
        max_energy_difference,max_fidelity_difference,reference_checks=validation.reference_checks,
        gradient_checks=validation.gradients,verified_utc=string(now(UTC)))
    write_product(joinpath(directory,"formal-verification.json"),verification)
    if "--publish" in ARGS
        product_path = joinpath(root,"data/exp04/exp04_D11.json")
        product = (;schema="exp04-sharing/v1",data_product="D11",producer="exp04",
            dependencies=["S01"],config,source_fingerprint=manifest.fingerprint,
            source_run=relpath(directory,root),records,comparisons=paired,
            equal_parameter_comparisons=equal_parameters,energy_selected_branches=winners,
            fidelity_improved=count(r->r.fidelity_change>1e-8,paired),
            fidelity_tied=count(r->abs(r.fidelity_change)<=1e-8,paired),
            fidelity_lower=count(r->r.fidelity_change < -1e-8,paired),verification)
        write_product(product_path,product)
        published = open(JSON3.read,product_path)
        @assert length(published.records)==72 && length(published.comparisons)==36
        @assert length(published.equal_parameter_comparisons)==18
        product_manifest = (;schema="exp04-sharing/v1",data_product="D11",producer="exp04",
            dependencies=["S01"],config,source_fingerprint=manifest.fingerprint,
            source_run=relpath(directory,root),sources=manifest.sources,
            source_manifest_sha256=bytes2hex(sha256(read(joinpath(directory,"manifest.json")))),
            verification,product=relpath(product_path,root),product_sha256=bytes2hex(sha256(read(product_path))),
            verifier_sha256=bytes2hex(sha256(read(@__FILE__))),figures=String[],
            tables=["tab:ansatz-fidelity"])
        write_product(joinpath(root,"data/exp04/exp04_D11_manifest.json"),product_manifest)
        println("PUBLISHED-D11 ",product_path)
    end
    println("VERIFY-EXP04-SHARING-OK tasks=72 passes=$checked_passes")
end

main()
