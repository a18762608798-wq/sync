# Independent Julia state/energy references for every Exp07 circuit, zero QPU calls.
push!(LOAD_PATH, joinpath(@__DIR__, "..", "src"))
using LinearAlgebra, NPZ
BLAS.set_num_threads(1)
using Shared01, Exp02, Exp04

function main()
    length(ARGS) == 1 || error("usage: export_exp07_validation.jl <output.npz>")
    root = normpath(joinpath(@__DIR__, ".."))
    source = NPZ.npzread(joinpath(root, "data", "exp04", "exp04_S06.npz"))
    @assert Exp04.decode_protocol(source["optimization_protocol"]) == OPTIMIZATION_PROTOCOL
    psi = zeros(ComplexF64, 90, 256)
    energies = zeros(90)
    indices = zeros(Int, 90, 3)
    row = 0
    for si in 1:7:99, di in (2, 1), li in 1:3
        row += 1
        delta, tag = di == 1 ? (-2.0, "dm2") : (0.85, "d085")
        @assert source["$(tag)_conv"][si, li, 2] && !source["$(tag)_stagn"][si, li, 2]
        leg = LEG_LABELS[li]
        meta = build_meta(8, leg)
        theta = Vector{Float64}(vec(source["$(tag)_theta_leg"][si, li, 2, 1:16]))
        state = apply_circuit!(zeros(ComplexF64, 256), psi_init(leg, 8), theta, meta, 2, delta)
        H = build_hamiltonian(8, si / 100, delta)
        energy = real(dot(state, H * state))
        @assert abs(energy - source["$(tag)_leg_E"][si, li, 2]) < 1e-8
        psi[row, :] .= state
        energies[row] = energy
        indices[row, :] .= (di, si, li)
    end
    @assert row == 90
    NPZ.npzwrite(ARGS[1], Dict("psi" => psi, "energy" => energies, "indices" => indices))
    println("EXP07-REFERENCE-OK: 90 independently checked Julia states and energies")
end
main()
