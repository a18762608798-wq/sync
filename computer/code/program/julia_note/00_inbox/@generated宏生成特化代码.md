# @generated 宏生成特化代码

## 背景/动机

普通的 Julia 方法在定义时写死了实现。但有时我们希望**根据输入类型，在编译期生成不同的代码体**，以达到最高性能或绕过类型限制。`@generated` 宏正是为了这个目的：它允许函数体返回一个**表达式（Expr）**，该表达式将在编译期被替换为实际的函数体。

## 核心内容

### 基本用法

```julia
@generated function myfunc(x)
    # 此刻 x 的类型已知（编译期）
    T = x  # 注意：在 @generated 中，x 是类型而不是值！
    if T <: Integer
        return :( x + 1 )   # 返回表达式
    else
        return :( string(x) )
    end
end
```

`@generated` 函数体在编译期执行，其参数的值是**类型对象**（即 `Int`、`Float64` 等），而非运行时值。函数体必须返回一个 `Expr` 或字符串，这个表达式将成为该调用的实际方法体。

### 典型使用场景

**1. 跳过运行时开销**

```julia
@generated function ndims(x)
    return :( Val($(ndims(typeof(x)))) )
end
```

这会在编译期计算 `ndims`，而运行时直接返回编译常量。

**2. 根据数组元素类型选择算法**

```julia
@generated function sum_strided(x::AbstractArray{T}) where T
    if T <: Number
        quote
            s = zero($T)
            @simd for v in x
                s += v
            end
            s
        end
    else
        :( reduce(+, x) )
    end
end
```

## 关键代码/公式

核心模式：
```
@generated function f(args...)
    # 编译期：检查参数类型
    # 返回 :( 一个 Expr 表达式的引用 )
end
```

## 注意事项/常见误区

- **参数是类型，不是值**：在 `@generated body` 中，`x` 的类型是 `Type`（如 `Int` 本身），不是 `Int` 的实例。要拿到值的类型用 `typeof(x)`（虽然在函数体内部无效，因为此时没有值）。
- **必须是纯函数**：`@generated` 函数的代码生成部分必须是**纯的**，即对于相同的输入类型总是产生相同的输出表达式。由于 Julia 可能缓存生成结果并在不同场合复用，如果生成逻辑依赖全局可变状态，可能产生难以调试的错误。
- **返回值为 Expr**：`@generated` 函数体必须返回一个表达式对象，Julia 不会自动把最后一行包装成表达式。
- **过度使用导致编译变慢**：每遇到新的类型组合，Julia 都会调用一次生成函数并编译生成的结果。类型组合过多时编译时间会显著增长。
