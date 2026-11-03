# One-time promotion of independently optimized results, with p=1 held fixed.
# Failed historical independent solves are recomputed under current PRE-003.
push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra, NPZ, JSON3, SHA
BLAS.set_num_threads(1)
using Shared01, Exp02, Exp04

const ROOT = normpath(joinpath(@__DIR__, ".."))
const FIELDS = ("theta_star", "E_star", "a_star", "spi", "ostr", "e0",
                "leg_E", "theta_leg", "conv", "stagn", "dtail", "einit", "sym")
const BRANCH_FIELDS = Set(("leg_E", "theta_leg", "conv", "stagn", "dtail"))
const EXTRA_FIELDS = ("seed_leg", "nsamples_leg", "iters_leg", "reused_leg")
const OUTPUT = joinpath(ROOT, "data", "exp04")

function preserve_p1!(payload, reference, tag)
    for key in FIELDS
        if key in BRANCH_FIELDS
            selectdim(payload[key], 3, 1:1) .= reference["$(tag)_$(key)"]
        elseif key in ("e0", "einit")
            payload[key] .= reference["$(tag)_$(key)"]
        else
            selectdim(payload[key], 2, 1:1) .= reference["$(tag)_$(key)"]
        end
    end
end

function fill_from_point!(payload, point, i)
    Exp04.decode_protocol(point["optimization_protocol"]) == OPTIMIZATION_PROTOCOL ||
        error("obsolete point protocol")
    for key in (FIELDS..., EXTRA_FIELDS...)
        selectdim(payload[key], 1, i:i) .= point[key]
    end
end

function build_line(delta, tag, global_tag, reference, global_data, checkpoint_dir)
    payload = Dict{String,Any}(key => copy(global_data["$(global_tag)_$(key)"]) for key in FIELDS)
    preserve_p1!(payload, reference, tag)
    payload["seed_leg"] = zeros(UInt64, 99, 3, 3)
    payload["nsamples_leg"] = fill(N_GLOBAL + 1, 99, 3, 3)
    payload["iters_leg"] = fill(-1, 99, 3, 3)  # not recorded in historical products
    payload["reused_leg"] = trues(99, 3, 3)
    mkpath(checkpoint_dir)
    completed = Threads.Atomic{Int}(0)
    Threads.@threads for i in 1:99
        point_path = joinpath(checkpoint_dir, "$(tag)_$(lpad(i, 3, '0')).npz")
        if isfile(point_path)
            fill_from_point!(payload, NPZ.npzread(point_path), i)
            Threads.atomic_add!(completed, 1)
            continue
        end
        s = i / 100
        H = build_hamiltonian(8, s, Float64(delta))
        for p in 1:3, (li, leg) in enumerate(LEG_LABELS)
            meta = build_meta(8, leg)
            psi0 = psi_init(leg, 8)
            n = nparams(meta, delta, p)
            theta = Vector{Float64}(vec(payload["theta_leg"][i, li, p, 1:n]))
            valid = Bool(payload["conv"][i, li, p]) && !Bool(payload["stagn"][i, li, p]) &&
                    all(isfinite, theta)
            actual = valid ? energy_of(theta, H, psi0, meta, p, delta, zeros(ComplexF64, 256)) : Inf
            valid &= isfinite(actual) && abs(actual - payload["leg_E"][i, li, p]) < 1e-8
            payload["seed_leg"][i, li, p] = Exp04._derive_seed(round(Int, 100delta), i, p, li)
            if !valid
                p == 1 && error("p=1 baseline failed at δ=$delta s=$s leg=$leg")
                step = run_leg_global(H, psi0, meta, delta, p, round(Int, 100delta), i, li)
                step.converged && !step.stagnant || error("independent solve unconverged")
                payload["leg_E"][i, li, p] = step.energy
                payload["theta_leg"][i, li, p, 1:n] .= step.theta
                payload["conv"][i, li, p] = true
                payload["stagn"][i, li, p] = false
                payload["dtail"][i, li, p] = step.dtail
                payload["seed_leg"][i, li, p] = step.seed
                payload["nsamples_leg"][i, li, p] = step.nsamples
                payload["iters_leg"][i, li, p] = step.iters
                payload["reused_leg"][i, li, p] = false
            end
            @assert payload["leg_E"][i, li, p] <= payload["einit"][i, li] + 1e-8
            @assert payload["leg_E"][i, li, p] >= payload["e0"][i] - 1e-8
        end
        for p in 2:3
            li = argmin(vec(payload["leg_E"][i, :, p]))
            leg = LEG_LABELS[li]
            meta = build_meta(8, leg)
            theta = Vector{Float64}(vec(payload["theta_leg"][i, li, p, 1:8p]))
            psi = apply_circuit!(zeros(ComplexF64, 256), psi_init(leg, 8), theta, meta, p, delta)
            payload["a_star"][i, p] = li
            payload["E_star"][i, p] = payload["leg_E"][i, li, p]
            payload["theta_star"][i, p, :] .= payload["theta_leg"][i, li, p, :]
            payload["spi"][i, p] = structure_factor(zz_correlators(psi), pi)
            payload["ostr"][i, p] = string_order(psi)
            payload["sym"][i, p, :] .= (abs(expect_ztot(psi, 8)),
                abs(overlap_xbar(psi, 8) - 1), abs(overlap_reflect(psi, 8) - 1))
            @assert maximum(payload["sym"][i, p, :]) < 1e-8
        end
        point = Dict{String,Any}(key => copy(selectdim(payload[key], 1, i:i)) for key in (FIELDS..., EXTRA_FIELDS...))
        point["optimization_protocol"] = Exp04.protocol_bytes()
        tmp = point_path * ".tmp"
        NPZ.npzwrite(tmp, point)
        mv(tmp, point_path; force=true)
        number_done = Threads.atomic_add!(completed, 1) + 1
        println("δ=$delta independent points $number_done/99; saved s=$s")
        flush(stdout)
    end
    @assert all(payload["conv"]) && !any(payload["stagn"])
    return payload
end

function main()
    length(ARGS) == 1 || error("usage: migrate_exp04_independent.jl <retirement-audit-directory>")
    audit = abspath(ARGS[1])
    reference_path = joinpath(audit, "p1-reference.npz")
    global_path = joinpath(ROOT, "data", "exp04_global", "exp04global_S06.npz")
    reference, global_data = NPZ.npzread(reference_path), NPZ.npzread(global_path)
    for (delta, tag, global_tag) in ((-2.0, "dm2", "gm2"), (0.85, "d085", "gd085"))
        if tag in completed_lines(OUTPUT)
            println("δ=$delta already completed under current protocol")
            continue
        end
        payload = build_line(delta, tag, global_tag, reference, global_data,
                             joinpath(OUTPUT, "independent_points"))
        save_line(OUTPUT, delta, payload)
    end
    s06, s03, manifest_path = assemble_S06_S03(OUTPUT)
    manifest = Dict{String,Any}(String(key) => value for (key, value) in pairs(open(JSON3.read, manifest_path)))
    manifest["migration"] = Dict("p1_reference_sha256" => bytes2hex(sha256(read(reference_path))),
        "independent_source_sha256" => bytes2hex(sha256(read(global_path))),
        "p1_preserved" => true, "retirement_record" => relpath(audit, ROOT))
    open(manifest_path, "w") do io
        JSON3.write(io, manifest)
    end
    build_D09(OUTPUT, joinpath(ROOT, "data", "shared01", "shared01_S01.npz"), s06)
    println("INDEPENDENT-MIGRATION-OK $s06 $s03")
end

main()
