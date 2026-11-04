# multiple dispatch

## basics

> `Which is the key step to optimization of dynamic languages`

```julia
f(x::Int64, y::Int64) = x + y
f(x::Float64, y::Float64) = x - y
f(1, 1)
f(1., 1.)
```

## 派发规则

### 关键字参数不参与多重派发

 下面两个方法在 Julia 中只能存在一个（会报重定义错误或或者在repl中覆盖）

```julia
f(; flag::Val{1}) = flag
f(; flag::Val{2}) = flag

f(; flag=Val(1))
f(; flag=Val(2))
```

改成位置参数就可以了

```julia
f(flag::Val{1}) = flag
f(flag::Val{2}) = flag

f(Val(1))
f(Val(2))
```

## Tips

### 参数类型泛型（推荐）

**不推荐把参数类型完全实例化, 而是使用这种泛型.**

```julia
function test(A::Array{T}) where T <: Union{Float64, Int64}
    print(A)
end

A = zeros(2, 2)
B = Int64.(A)
test(A)
test(B)
```

### Val

`Val` 是 Julia 的**值类型**（value type），将运行时的值信息编码到类型系统中，使得编译器在编译时即可获知具体值，从而进行编译期优化。

常用于 `Val(true)` 作为区分.

```julia
f(x, ::Val{true}) = x + 1
f(x, ::Val{false}) = x

f(1, Val(true))
f(1, Val(false))
```
