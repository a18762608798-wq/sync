# Julia `@test_throws` 测试异常宏

**日期**: 2026-07-20 22:50
**分类**: 编程/Julia
**标签**: #Julia #测试 #异常

## 背景

在测试代码中，除了用 `@test` 断言正常结果，还需要测试非法输入是否会抛出正确的异常。`@test_throws` 来自 `using Test`，用于验证代码的异常路径。

## 内容

### 基本语法

```julia
@test_throws ExceptionType expression
```

断言 `expression` 执行时会抛出 `ExceptionType` 类型的异常，否则测试失败。

### 实际用例

```julia
# 解析非法字符串
@test_throws ArgumentError parse(Int, "abc")

# 下标越界
@test_throws BoundsError A[100]

# 方法不存在
@test_throws MethodError foo("not_a_number")

# 自定义错误
@test_throws ErrorException error("出错了")
```

### 等价的手写版本

```julia
# 一行
@test_throws BoundsError A[100]

# 等价于
try
    A[100]
    @test false   # 没抛异常 → 测试失败
catch e
    @test e isa BoundsError  # 确认异常类型
end
```

### `@test` vs `@test_throws`

| 宏 | 测试目标 | 适用场景 |
|----|---------|----------|
| `@test` | 正常路径 | 验证返回值正确 |
| `@test_throws` | 异常路径 | 验证非法输入能正确报错 |
| `@test_logs` | 日志输出 | 验证是否产生了特定日志级别/消息 |

## 要点

- `@test_throws` 测试"期望这里出这个错"，属于负面测试
- 常用于测试边界条件、非法参数、文件不存在、格式错误等
- 与 `@test` 互补，覆盖正常路径和异常路径
