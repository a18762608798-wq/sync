# Fresh, non-hardware smoke calculations with isolated validation outputs.
# Does not submit hardware jobs or overwrite production data/figures.
# Usage: julia --project=. --startup-file=no scripts/smoke_simulation.jl [output-dir]

push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra, Test, NPZ, JSON3, Dates
using Shared01, Exp02, Exp03, Exp04
BLAS.set_num_threads(1)

function main()
    length(ARGS) <= 1 || error("usage: smoke_simulation.jl [output-dir]")
    root = normpath(joinpath(@__DIR__, ".."))
    out = isempty(ARGS) ? joinpath(root, "data", "validation", "non-hardware") : abspath(only(ARGS))
    production = joinpath(root, "data")
    out_real = realpath(mkpath(out))
    protected = [joinpath(production, name) for name in ("shared01", "exp02", "exp03", "exp04")]
    for path in protected
        relative = relpath(out_real, realpath(path))
        (relative == "." || !(first(splitpath(relative)) == "..")) &&
            error("validation output must not be inside a production directory: $path")
    end

    archived, _ = Shared01.load_shared01(joinpath(production, "shared01"))
    panels = NPZ.npzread(joinpath(production, "exp02", "exp02_D04.npz"))
    gap_archive = NPZ.npzread(joinpath(production, "exp03", "exp03_D02.npz"))
    rows = Dict{String,Any}[]
    @testset "fresh shared-01 and exp02 representative points" begin
        for label in Shared01.REP_LABELS
            s, delta = Shared01.REP_POINTS[label]
            solution = Shared01.solve_point(s, delta)
            H = Shared01.build_hamiltonian(8, s, delta)
            i, j = round(Int, 100s), round(Int, 20(delta + 3)) + 1
            residual = norm(H * solution.psi0 - solution.E0 * solution.psi0) / max(1.0, norm(H))
            @test norm(solution.psi0) ≈ 1.0 atol=1e-12
            @test residual < 1e-8
            @test abs(solution.E0 - archived["E0"][i, j]) < 1e-10
            panel = Exp02.panel_point(solution.psi0)
            for key in ("s_hat_pi", "o_hat_str", "q_val", "z_tilde")
                @test abs(getproperty(panel, Symbol(key)) - panels[key][i, j]) < 1e-9
            end
            NPZ.npzwrite(joinpath(out, "representative_$label.npz"),
                         Dict("psi" => solution.psi0, "E0" => solution.E0, "E1" => solution.E1))
            push!(rows, Dict("label" => label, "s" => s, "delta" => delta,
                             "E0" => solution.E0, "residual" => residual))
        end
    end

    gaps = Dict{String,Any}[]
    gap_dir = joinpath(out, "gap-chunks")
    # Keep all five exact ED baselines even when the paper selects only three
    # of them. The CPU MPS backend has its own full validation entry point.
    @testset "fresh exp03 ED baselines and checkpoint IO" begin
        for L in Exp03.ED_LS
            started = time()
            result = Exp03.solve_gap(L, 0.5)
            r = findfirst(==(L), vec(gap_archive["Ls"]))
            reference, source = if r === nothing
                ib = cld(50, Exp03.BLOCK)
                file = Exp03._chunkpath(joinpath(production,"exp03"),L,ib)
                chunk = NPZ.npzread(file)
                i = findfirst(s -> abs(s-0.5) < 1e-12, vec(chunk["s"]))
                i === nothing && error("missing ED reference for L=$L s=0.5")
                (chunk["Delta"][i], file)
            else
                (gap_archive["Delta"][r,50], "published D02 ED row")
            end
            difference = abs(result.delta_gap - reference)
            @test result.delta_gap >= Exp03.GAP_MIN_TOL
            @test difference < 1e-8
            path = Exp03.save_chunk(gap_dir, L, 1, [0.5], [result])
            @test Exp03.chunk_exists(gap_dir, L, 1)
            @test NPZ.npzread(path)["Delta"][] == result.delta_gap
            push!(gaps, Dict("L" => L, "s" => 0.5, "gap" => result.delta_gap,
                             "archive_difference" => difference, "reference_source" => source,
                             "seconds" => time() - started))
            println("fresh exp03 L=$L: gap=$(result.delta_gap), archive difference=$difference")
            flush(stdout)
        end
        @test length(Exp03.completed_chunks(gap_dir)) == length(Exp03.ED_LS)
    end

    winners = Dict{String,Any}[]
    @testset "fresh exp04 optimization, both production lines and all depths" begin
        for delta in Exp04.DELTAS
            s = 0.5
            H = Shared01.build_hamiltonian(8, s, delta)
            E0 = minimum(eigvals(Hermitian(H)))
            result = Exp04.run_point(delta, s, H, E0)
            for leg in Exp04.LEG_LABELS, p in 1:3
                step = result.steps[leg][p]
                @test step.converged || step.stagnant
                @test step.energy >= E0 - 1e-8
                p > 1 && @test step.energy <= result.steps[leg][p - 1].energy + 1e-8
            end
            for p in 1:3
                leg, theta, energy = result.best[p]
                meta = Exp04.build_meta(8, leg)
                psi0 = Exp04.psi_init(leg, 8)
                psi = Exp04.apply_circuit!(zeros(ComplexF64, 256), psi0, theta, meta, p, delta)
                @test abs(real(dot(psi, H * psi)) - energy) < 1e-10
                @test norm(psi) ≈ 1.0 atol=1e-10
                @test abs(Exp04.expect_ztot(psi, 8)) < 1e-8
                @test abs(Exp04.overlap_xbar(psi, 8) - 1) < 1e-8
                @test abs(Exp04.overlap_reflect(psi, 8) - 1) < 1e-8
                NPZ.npzwrite(joinpath(out, "vqe_delta$(delta)_p$p.npz"),
                             Dict("theta" => theta, "psi" => psi, "energy" => energy, "E0" => E0))
                push!(winners, Dict("delta" => delta, "s" => s, "p" => p,
                                    "leg" => leg, "energy" => energy, "E0" => E0))
            end
        end
    end

    # Audit the existing archive separately; do not relax its spec tolerance or rewrite it.
    fit = Exp03.quadratic_fit(vec(gap_archive["fit_x"]), vec(gap_archive["fit_y"]))
    differences = Dict(string(key) => abs(getproperty(fit, key) - gap_archive["fit_$key"][])
                       for key in (:a, :b, :c))
    summary = Dict("kind" => "validation-only, not formal experiment products",
                   "julia" => string(VERSION), "created_utc" => string(now(UTC)),
                   "fresh_calculations_pass" => true, "representative_points" => rows,
                   "gap_spot_checks" => gaps, "vqe_winners" => winners,
                   "existing_exp03_fit_differences" => differences,
                   "existing_exp03_fit_tolerance" => Exp03.FIT_TOL,
                   "existing_exp03_fit_pass" => all(v < Exp03.FIT_TOL for v in values(differences)))
    open(joinpath(out, "summary.json"), "w") do io
        JSON3.write(io, summary)
    end
    println("SMOKE-SIMULATION-OK: ", out)
    summary["existing_exp03_fit_pass"] || println("WARNING: existing exp03 fit fails strict cross-platform recomputation; archive unchanged")
end

main()
