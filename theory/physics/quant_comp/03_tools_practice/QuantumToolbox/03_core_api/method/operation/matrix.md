# matrix

```julia
ψ1 = basis(ComplexF32, 2, 0; sparse=Val(true))
ψ2 = basis(ComplexF32, 2, 0; sparse=Val(true))
ρ = ψ1 * ψ1'
dot(ψ1, ψ2) # 内积
tensor(ψ1, ψ2) # 外积
ket2dm(ψ)        # ket -> density matrix
expect(O, ψ)     # 期望值
variance(O, ψ)   # 方差
ptrace(ρ, 1) # partial trace.
tr(ρ)            # trace
norm(ρ)          # 范数
normalize(ρ)
unit(ρ)          # normalize 的同义函数
matrix_element(ψ1, ρ, ψ2) # get the element of operator.
Hermitian((ρ + ρ') / 2) # Hermitianization
```

## ptrace

```julia
dims = ntuple(_ -> 2, 5)
ψ = basis(ComplexF32, 2^5, 0; dims=dims, sparse=Val(true))
ptrace(ψ, (1, 2))
```

### ptrace method

```julia
ptrace(QO::QuantumObject, sel)
```

* sel: **保留的**子系统的idx或者范围.
