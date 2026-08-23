# @test 与 @test_throws

| 宏 | 测试目标 | 适用场景 |
| ---- | --------- | ---------- |
| `@test` | 正常路径 | 验证返回值正确 |
| `@test_throws` | 异常路径 | 验证非法输入能正确报错 |
| `@test_logs` | 日志输出 | 验证是否产生了特定日志级别/消息 |

## @test

断言表达式为真，用于测试正常路径。

## @test_throws

```julia
using Test

@test_throws ArgumentError parse(Int, "abc")
@test_throws MethodError foo("not_a_number")
```

> 断言错误专用, 断言 `expression` 执行时会抛出 `ExceptionType` 类型的异常，否则测试失败。
