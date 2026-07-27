using QuantumToolbox
using Test
include("get_ssh_ZR.jl")

@testset "get_ssh_ZR" begin
    @test get_ssh_ZR(8, 0, 1) ≈ 1 # topology
    @test get_ssh_ZR(8, 1, 1) ≈ -1 # trivial
    @test get_ssh_ZR(12, 0, 1) ≈ 1 # topology
    @test get_ssh_ZR(16, 1, 1) ≈ -1 # trivial
end
