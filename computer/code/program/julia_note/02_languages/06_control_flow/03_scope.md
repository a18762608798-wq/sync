# scope

## begin...end 块

> `begin...end` 的作用只有一个：**把多条表达式合并成一条表达式**，并返回最后一条的值。
> **不创建作用域** — 这一点和 `let`、函数体、`@testset` 不同，它内部没有新的变量作用域，变量直接落在外层

```julia
x = begin
    a = 1
    b = 2
    a + b
end
# x = 3
```
