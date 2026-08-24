using QuantumToolbox
function get_xyz(qubit_num::Int)
    @assert iszero(rem(qubit_num, 4)) && !iszero(qubit_num) "The number of qbits must in 4N^+."
    # Params settings
    pair_num = qubit_num ÷ 2
    # Qobj preparation
    X = sigmax()
    Y = sigmay()
    Z = sigmaz()
    qubit_dims = ntuple(_ -> 2, qubit_num)
    Ho = 0 * qeye(2^qubit_num; dims=qubit_dims)
    He = 0 * qeye(2^qubit_num; dims=qubit_dims)
    # Get ssh op
    XX(i) = multisite_operator(
        Val(qubit_num),
        i => X, i + 1 => X,
    )
    YY(i) = multisite_operator(
        Val(qubit_num),
        i => Y, i + 1 => Y,
    )
    ZZ(i) = multisite_operator(
        Val(qubit_num),
        i => Z, i + 1 => Z,
    )
    # Δ = 1 (Heisenberg), 区分奇偶键: 返回 (H_odd, H_even)
    link(i) = XX(i) + YY(i) + ZZ(i)
    for pair_idx = 1:(pair_num-1)
        i = 2pair_idx - 1
        j = 2pair_idx
        Ho += link(i)
        He += link(j)
    end
    Ho += link(2pair_num - 1)

    return Ho, He
end


function get_ssh_H(qubit_num::Int, s::Real)
    Ho, He = get_xyz(qubit_num)
    ssh_op = Ho + s * He

    return ssh_op
end

function get_ssh_constrained_H(qubit_num::Int, s::Real; ϵ=1)
    H_c = get_ssh_H(
        qubit_num, s
    )
    H_c -= ϵ * (get_Ui(qubit_num, sigmax()) + 2 * get_Ui(qubit_num, sigmaz()))
    return H_c
end

function get_Ui(qubit_num::Int, op::Qobj)
    Ui = multisite_operator(
        Val(qubit_num),
        (i => op for i in 1:qubit_num)...
    )
    return Ui
end



