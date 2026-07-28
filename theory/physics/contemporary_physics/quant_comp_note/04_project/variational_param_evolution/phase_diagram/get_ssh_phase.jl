using QuantumToolbox
using NPZ
using ProgressMeter
include("get_ssh_ZR.jl")

function save_ssh_phase(path::String, qubit_num::Int, N::Int)
    s_grid = collect(range(0, 1; length=N))
    δ_grid = collect(range(0, 1; length=N))
    ZR_vals = zeros(Float64, N, N)
    @showprogress Threads.@threads for s_idx = 1:N
        for δ_idx = 1:N
            ZR_vals[s_idx, δ_idx] = get_ssh_ZR(qubit_num, s_grid[s_idx], δ_grid[δ_idx])
        end
    end
    npzwrite(
        path,
        Dict(
            "s" => s_grid,
            "delta" => δ_grid,
            "ZR" => ZR_vals,
        ),
    )
end

if abspath(PROGRAM_FILE) == @__FILE__
    path = joinpath(@__DIR__, "./data/phase.npz")
    save_ssh_phase(path, 16, 2)
end

