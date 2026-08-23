# @testset

来自 `using Test`，将一组 `@test` 断言嵌套在一个逻辑分组中。

## 作用

1. **逻辑分组**：为测试块命名，方便阅读和定位
2. **局部作用域**：`@testset` 内的变量不会泄露到外部，每个 testset 是独立的 soft local scope
3. **报告汇总**：运行后输出按 testset 层级汇总的结果

```julia
using Test

@testset "Test1" begin
    @testset "Test1.1" begin
        @test 1.0 ≈ 1.0
    end
end
```
