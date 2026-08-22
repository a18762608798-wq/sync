using QuantumToolbox
using NPZ
include(joinpath(@__DIR__, "..", "..", "src", "var_param_evolution.jl"))

function get_Hc_spectrum(qubit_num::Int, eigvals::Int, slist, δlist; sparse=true)
    get_H(s, δ) = get_ssh_constrained_H(qubit_num, s, δ; ϵ=1)
    spectrum, _ = get_spectrum(get_H, eigvals, slist, δlist; sparse=sparse)
    return spectrum
end

# just save δ = 0.3
function save_ideal_spectrum(path::String, qubit_num::Int, eigvals::Int, s_length::Int; sparse=true)
    spectrum = Array{Float64,2}(undef, s_length, eigvals)
    slist = range(0, 1; length=s_length)
    # 扫描网络
    δlist = fill(0.3, s_length)
    spectrum = get_Hc_spectrum(qubit_num, eigvals, slist, δlist; sparse=sparse)
    npzwrite(
        path,
        Dict(
            "slist" => slist,
            "spectrum" => spectrum
        ),
    )
end

if abspath(PROGRAM_FILE) == @__FILE__
    ideal_path = joinpath(@__DIR__, "./data/ideal_spectrum.npz")
    save_ideal_spectrum(ideal_path, 8, 2, 100; sparse=false)
end
