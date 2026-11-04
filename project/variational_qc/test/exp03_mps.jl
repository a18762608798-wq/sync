# Standalone or included by runtests.jl. Small exact references test the science.
push!(LOAD_PATH,joinpath(@__DIR__,"..","src"))
using Shared01, Exp03, ITensors, ITensorMPS, LinearAlgebra, Random, Test, JSON3

@testset "exp03 MPS exact Hamiltonian and reflection" begin
    L = 6
    @test mps_chi_ladder(64) == [64]
    @test mps_chi_ladder(128) == [128]
    @test mps_chi_ladder(512) == [128,256,512]
    for s in (0.2,0.5,0.8)
        sys = mps_system(L,s)
        full = reduce(*,sys.H)
        dense = reshape(Array(full,prime.(sys.sites)...,sys.sites...),2^L,2^L)
        @test norm(dense-build_hamiltonian(L,s,DELTA_FIXED)) < 1e-11
        Random.seed!(735)
        psi = random_mps(ComplexF64,sys.sites; linkdims=4)
        v = vec(Array(reduce(*,psi),sys.sites...))
        reflected = reflect_mps(psi,sys.sites)
        rv = vec(Array(reduce(*,reflected),sys.sites...))
        reference = [v[Int(reflect_bits(UInt64(i),L))+1] for i in 0:(2^L-1)]
        @test norm(rv-reference) < 1e-12
        @test abs(inner(psi,reflected)-dot(v,reference)) < 1e-12
    end
    @test_throws ArgumentError mps_system(7,0.5)
    @test_throws ArgumentError mps_params(64; eigsolve_maxiter=0)
end

@testset "exp03 MPS lowest two states and provenance" begin
    L,s = 6,0.5
    p = mps_params(64)
    r = solve_gap_mps(L,s,64; params=p)
    ed = solve_gap(L,s)
    @test abs(r.E0-ed.E0) < 1e-6
    @test abs(r.E1-ed.E1) < 1e-6
    @test abs(r.delta_gap-ed.delta_gap) < 1e-6
    @test mps_point_valid(r)
    record = mps_point_dict(r)
    @test mps_record_valid(record)
    @test mps_record_matches(record,L,s,p)
    @test !mps_record_matches(record,L,s,mps_params(64; seed=p.seed+1))
    @test !mps_record_matches(record,L,0.6,p)
    corrupted = copy(record)
    corrupted["E1"] += 1.0
    @test !mps_record_valid(corrupted)
    @test !mps_pair_valid(Dict("low"=>record,"high"=>record))
    # Preserve the record and check JSON round-trip under the same runtime.
    dir = joinpath(@__DIR__,"..","data","validation","exp03-mps-unit-20261104",mps_source_fingerprint()[1:12])
    path = joinpath(dir,"L6_s0p5_chi64.json")
    save_mps_point_json(path,r)
    saved = open(JSON3.read,path)
    @test mps_record_valid(saved)
    @test mps_record_matches(saved,L,s,p)
    @test PAPER_LS == (8,16,24,32)
    @test ED_LS == (8,12,16,20,24)
end
