using Test
using QuantumToolbox
include("../src/op_creator.jl")

@testset "get_ZR_val" begin
    qubit_num = 4
    ψ0 = basis(2, 0) ⊗ basis(2, 0) ⊗ basis(2, 0) ⊗ basis(2, 0)
    ρ0 = ψ0 * ψ0'
    @test get_ZR_val(ρ0) ≈ 1.0

    ψ1 = basis(2, 0) ⊗ basis(2, 0) ⊗ basis(2, 1) ⊗ basis(2, 0)
    ρ1 = ψ1 * ψ1'
    @info get_ZR_val(ρ1)
    @test get_ZR_val(ρ1) ≈ 0.0

    dims = ntuple(_ -> 2, qubit_num)
    ρ_mixed = qeye(2^qubit_num; dims=dims) / 2^qubit_num # 最大混合态
    @info get_ZR_val(ρ_mixed)
    @test get_ZR_val(ρ_mixed) ≈ 0.25

    @test_throws AssertionError get_ZR_val(qeye(2^3; dims=(2, 2, 2)))
end

