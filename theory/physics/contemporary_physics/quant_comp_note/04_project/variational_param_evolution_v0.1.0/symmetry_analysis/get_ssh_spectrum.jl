using QuantumToolbox
using NPZ
include("../src/var_param_evolution.jl")

function get_ssh_spectrum(qubit_num::Int, eigvals::Int, slist, δlist; sparse=true)
    get_H(s, δ) = get_ssh_constrained_H(qubit_num, s, δ)
    spectrum, _ = get_spectrum(get_H, eigvals, slist, δlist; sparse=sparse)
    return spectrum
end

function save_ssh_spectrum(path::String, qubit_num::Int, eigvals::Int, grid_length::Int, param_num::Int; sparse=true)
    s_spectrum = Array{Float64,3}(undef, grid_length, eigvals, param_num)
    δ_spectrum = Array{Float64,3}(undef, grid_length, eigvals, param_num)
    grid = range(0, 1; length=grid_length)
    param_list = range(0, 1; length=param_num)
    # 扫描网络，对于s和δ扫描分别做子图
    # s
    for s_idx in eachindex(param_list)
        s_grid = fill(param_list[s_idx], grid_length)
        s_spectrum[:, :, s_idx] = get_ssh_spectrum(qubit_num, eigvals, s_grid, grid; sparse=sparse)
    end
    # δ
    for δ_idx in eachindex(param_list)
        δ_grid = fill(param_list[δ_idx], grid_length)
        δ_spectrum[:, :, δ_idx] = get_ssh_spectrum(qubit_num, eigvals, grid, δ_grid; sparse=sparse)
    end
    npzwrite(
        path,
        Dict(
            "param_list" => param_list,
            "s_spectrum" => s_spectrum,
            "delta_spectrum" => δ_spectrum,
        ),
    )
end

if abspath(PROGRAM_FILE) == @__FILE__
    path = joinpath(@__DIR__, "./data/spectrum.npz")
    save_ssh_spectrum(path, 8, 8, 50, 6; sparse=false)
end
