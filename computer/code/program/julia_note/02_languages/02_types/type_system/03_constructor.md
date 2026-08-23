# constructor

| 类型 | 位置 | 特点 | 何时用 |
| ------ | ------ | ------ | -------- |
| **Inner constructor** | `struct` 内部 | 调用 `new()` 创建对象，可做验证/转换 | **谨慎**，只在需要强制不变量时 |
| **Outer constructor** | `struct` 外部 | 调用 inner constructor 的便利包装，不能访问 `new()` | 提供默认值、类型转换 |
| **普通方法** | `struct` 外部 | 操作已有实例 | 所有非构造逻辑 |

> **尽量少写 inner constructor——只做必要的参数校验和不变量强制**。便利构造（默认值、类型转换等）写成 outer constructor。

## internal constructor

> **实际上是在接管对象创建过程, 给默认的innner construct 增加更复杂的构造**

```julia
abstract type Biology end
abstract type Animal <: Biology end
struct Cat <: Animal
    name::String
    function Cat(name::String) # NOTE: inner constructor must use new to construct an instance.
        return new(name)
    end

    function Cat(name::Char)
        return new(string(name))
    end
end

c = Cat(1) # wrong construct
c = Cat('c')
```

## Outer constructor

```julia
get_cat(name::Union{String, Char}) = Cat(name)
get_cat("Tuantuan")
```
