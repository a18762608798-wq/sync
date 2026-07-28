function get_ssh_H(qubit_num::Int, s::Real, δ::Real)
    @assert iszero(rem(qubit_num, 4)) && !iszero(qubit_num) "The number of qbits must in 4N^+."
    # Params settings
    J1 = 1 - s
    J2 = s
    pair_num = qubit_num ÷ 2
    # Qobj preparation
    X = sigmax()
    Z = sigmaz()
    qubit_dims = ntuple(_ -> 2, qubit_num)
    H1 = 0 * qeye(2^qubit_num; dims=qubit_dims)
    H2 = 0 * qeye(2^qubit_num; dims=qubit_dims)

    # Get ssh op
    XX(i) = multisite_operator(
        Val(qubit_num),
        i => X, i + 1 => X,
    )
    ZZ(i) = multisite_operator(
        Val(qubit_num),
        i => Z, i + 1 => Z,
    )
    link(i) = XX(i) + δ * ZZ(i)
    for pair_idx = 1:(pair_num-1)
        i = 2pair_idx - 1
        j = 2pair_idx
        H1 += link(i)
        H2 += link(j)
    end
    H1 += link(2pair_num - 1)
    ssh_op = J1 * H1 + J2 * H2

    return ssh_op
end

function get_SWAP(qubit_num::Int, i::Int, j::Int)
    # Qobj preparation
    X, Y, Z = sigmax(), sigmay(), sigmaz()
    I = eye(2)
    qubit_dims = ntuple(_ -> 2, qubit_num)
    # Create SWAP
    SWAP = 0 * qeye(2^qubit_num; dims=qubit_dims)
    for op in [X, Y, Z, I]
        SWAP += 0.5 * multisite_operator(
            Val(qubit_num),
            i => op, j => op,
        )
    end

    return SWAP
end

function get_reflect_op(qubit_num::Int)
    @assert iszero(rem(qubit_num, 2)) && !iszero(qubit_num) "The number of qbits must in 2N^+."
    pair_num = qubit_num ÷ 2
    qubit_dims = ntuple(_ -> 2, qubit_num)
    reflect_op = qeye(2^qubit_num; dims=qubit_dims)
    for i = 1:pair_num
        j = qubit_num - i + 1
        reflect_op *= get_SWAP(qubit_num, i, j)
    end

    return real(reflect_op)
end

