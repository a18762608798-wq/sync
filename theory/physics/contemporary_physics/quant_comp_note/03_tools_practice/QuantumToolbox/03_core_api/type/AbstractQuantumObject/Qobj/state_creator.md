# state creator

```julia
using QuantumToolbox
```

---

## basis(fock)

```julia
dims = (2, 2, 2)
ψ = basis(ComplexF32, 2, 0; sparse=Val(true))
ψ = basis(ComplexF32, 2^3, 7; dims=dims, sparse=Val(true))
```

### basis method

basis([T::Type=ComplexF64,] N::Int, j::Int=0; dims::Union{Int,AbstractVector{Int},Tuple}=N, sparse::Union{Bool,Val}=Val(false))

> 创造单位态.

### fields

```julia
print(ψ.dims) # The dims of subsystems(指标1和指标2)
```

---

## fock_dm

```{julia}
dims = (2, 2, 2)
ψ = fock_dm(ComplexF32, 2^3, 0; dims=dims, sparse=Val(true))
```

### fock method

fock_dm([T::Type=ComplexF64,] N::Int, j::Int=0; dims::Union{Int,AbstractVector{Int},Tuple}=N, sparse::Union{Bool,Val}=Val(false))

>Density matrix representation of a Fock state with element type T = ComplexF64 (default).

---

## rand

```julia
dims = (2, 2, 2)
rand_ket(ComplexF32, dims) 
```

### rand method

```julia
rand_ket([T::Type=ComplexF64,] dims)
```

---

## dm

```julia
dims = (2, 2, 2)
rand_dm(ComplexF32, dims) # the room: 2 * 3 * 3
```

### dm method

```julia
rand_dm([T::Type=ComplexF64,] dims; rank::Int=get_hilbert_size[dims](1))
```

---

## zero

```julia
dims = (2, 2, 2)
zero_ket(ComplexF32, (2, 3, 3)) # the room: 2 * 3 * 3
```

### zero method

```julia
zero_ket([T::Type=ComplexF64,] dims)
```

>Returns a zero Ket vector with given argument dimensions and element type T = ComplexF64
(default).

## conherent

>Fock basis 里构造的单模态. 暂时不用管他.

## conherent_dm

## thermal_dm

## thermal_dm(N, nbar)

## maximally_mixed_dm(N)
