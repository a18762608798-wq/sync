include("../src/var_param_evolution.jl")

function get_ssh_group_state(qubit_num::Int, s::Real, δ::Real)
    H = get_ssh_H(qubit_num, s, δ)
    energies, states, _ = eigsolve(
        H;
        eigvals=1,
        sortby=real,
        rev=false,
    )
    return real(energies[1]), states[1]
end

function get_ssh_ZR(qubit_num::Int, s::Real, δ::Real)
    @assert iszero(rem(qubit_num, 4)) && (qubit_num ≥ 8) "The number of qbits must be in 4N^+ and is 8 at least."
    # Params settings
    sub_num = qubit_num - 4
    sub_system = ntuple(i -> i + 2, sub_num)
    # Get sub_ρ
    _, ψ0 = get_ssh_group_state(qubit_num, s, δ)
    sub_ρ = ptrace(ψ0, sub_system)
    # Get ZR_val
    ZR_val = get_ZR_val(sub_ρ)

    return ZR_val
end
