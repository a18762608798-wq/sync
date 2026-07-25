# Julia 多重派发（Multiple Dispatch）原理

## 背景/动机

多重派发是 Julia 最核心的语言范式。在单派发（single dispatch）语言（如 Python、C++ 的虚函数）中，方法调用仅根据第一个参数（接收者）的类型来选择；Julia 的多重派发则根据**所有位置参数的类型**联合决定调用哪个方法。

## 核心内容

### 基本概念

Julia 中，函数（function）和方法（method）是分离的：
- **函数**：一个泛化的名称，如 `+`、`push!`、`foo`
- **方法**：函数针对特定类型组合的具体实现

每次调用函数时，Julia 会根据所有参数的具体类型，在方法表中查找最匹配的方法。

### 单派发 vs 多重派发

```julia
# 定义函数 f，参数为 (x, y)
function f(x::Int, y::Int)
    "int-int"
end

function f(x::Int, y::Float64)
    "int-float"
end

function f(x::Float64, y::Int)
    "float-int"
end

f(1, 2)       # "int-int"
f(1, 2.0)     # "int-float"
f(1.0, 2)     # "float-int"
```

在单派发语言中，你无法根据第二个参数的类型来选择不同实现——必须在函数内部手动判断。

### 方法选择规则

Julia 按以下顺序选择方法：
1. 检查所有方法中参数类型的匹配度
2. 选择最具体（most specific）的匹配——即参数类型更"窄"的那个
3. 如果无法决出唯一最具体的方法，抛出 `MethodError`

### 动态性

由于 Julia 的方法表在运行时可以修改，你可以随时为已有函数添加新的类型组合的方法——这对从已有库扩展行为非常自然。

## 关键代码

```julia
# 通用实现
collide(x, y) = "generic collision"

# 为具体类型特化
collide(x::Circle, y::Circle)    = "two circles"
collide(x::Circle, y::Rectangle) = "circle and rect"
collide(x::Rectangle, y::Circle) = "rect and circle"
```

## 注意事项/常见误区

- **类型标注不等于性能优化**：Julia 编译器对 `f(x)` 和 `f(x::Int)` 通常生成相同的机器码（只要能推断出实际类型）。类型标注主要用于**方法派发**，而非性能提示。
- **不要用 Python/C++ 的思维**：在 Julia 中，你应该把 "把操作放在它所属的参数组合" 上，而不是 "把方法挂在类上"。
- **与方法表过多无关的性能影响**：如果方法数量极大，查找开销可能显著，但通常应用中达不到这个量级。
