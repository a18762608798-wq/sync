# eigenvalue decomposition

## 本征值

```julia
using QuantumToolbox
H = sigmaz() + sigmax()
Es = eigenenergies(
    H; 
    sparse=Val(true), 
    eigvals=3, # The number of eigenvalues to calculate.
)
```

### eigenenergies method

```julia
eigenenergies(A::QuantumObject; sparse::Union{Bool,Val}=Val(false), kwargs...)
```

> 计算力学量期望；可以选择稀疏与否, 并继承对应的eigenstates的关键字参数.

* A::QuantumObject: the QuantumObject(主要是力学量) to solve eigenvalues
* sparse::Union{Bool,Val}: if false call eigvals(A::QuantumObject; kwargs...), otherwise call eigsolve. Default to Val(false).
* kwargs: Additional keyword arguments passed to the solver.
    If sparse=true, the keyword arguments are passed to `eigsolve`,
        - `eigvals`（个数）、`krylovdim`、`tol`、`maxiter`（迭代精度类）
        - `sigma`（位移）、`v0`（初向量）
        - `sortby`、`rev`（排序）
        - `solver`（线性求解器）+ 其它传给 LinearSolve 的 kwargs（如 `abstol`、`reltol`）
    otherwise to `LinearAlgebra.eigen/eigvals`.
        - `sortby`(按照...排序) 等.

## 对角化

```julia
using QuantumToolbox
H = sigmaz() + sigmax()
Es, ψ, U = eigenstates(
    H;
    sparse=Val(true),
    eigvals=2, 
    sortby=real, # 按照实部排序.
    rev=false,
) 
```

### eigenstates method

```julia
eigenstates(A::QuantumObject; sparse::Union{Bool, Val}=Val(false), kwargs...)
```

> 相比于eigenenergies多返回本征向量(Qobj对象和array对象)

## 子空间对角化

```julia
# 子空间对角化
function get_subspace_op(H, states)
    n = length(states)
    op = zeros(ComplexF64, n, n)

    for a in 1:n
        for b in 1:n
            op[a, b] = matrix_element(states[a], H, states[b])
        end
    end

    return Qobj(Hermitian((op + op') / 2))
end
```
