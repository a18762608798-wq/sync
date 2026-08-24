using QuantumToolbox
using NPZ
include(joinpath(@__DIR__, "src", "get_op.jl"))
include(joinpath(@__DIR__, "src", "get_spectrum.jl"))

function get_Hc_spectrum(qubit_num::Int, eigvals::Int, slist; sparse=true)
    get_H(s) = get_ssh_constrained_H(qubit_num, s; ϵ=1)
    spectrum, _ = get_spectrum(get_H, eigvals, slist; sparse=sparse)
    return spectrum
end

# Δ = 1 (Heisenberg)
function save_ideal_spectrum(path::String, qubit_num::Int, eigvals::Int, s_length::Int; sparse=true)
    slist = range(0, 1; length=s_length)
    spectrum = get_Hc_spectrum(qubit_num, eigvals, slist; sparse=sparse)
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

