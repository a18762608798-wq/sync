function get_ZR_val(ρ::Qobj)
    qubit_num = length(first(ρ.dims))
    @assert iszero(rem(qubit_num, 2)) && !iszero(qubit_num) "The number of qbits must in 2N^+."
    # Params settings
    pair_num = qubit_num ÷ 2
    part1 = ntuple(i -> i, pair_num)
    part2 = ntuple(i -> i + pair_num, pair_num)
    ρ1 = ptrace(ρ, part1)
    ρ2 = ptrace(ρ, part2)
    # Qobj preparation
    reflect_op = get_reflect_op(qubit_num)
    reflect_val = tr(ρ * reflect_op)
    P1 = tr(ρ1^2)
    P2 = tr(ρ2^2)
    # get ZR_val
    ZR_val = reflect_val / sqrt((P1 + P2)/2)
    return real(ZR_val)
end


