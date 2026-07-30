# Python 异常抛出：用 raise 代替 error() 函数

**日期**: 2026-07-29 21:31
**分类**: 编程/Python
**标签**: #python #exception #error-handling

## 背景

对比 Julia 的 `error()` 函数，询问 Python 中是否有类似的直接抛出错误的函数。

## 内容

Python **没有**类似 Julia `error()` 的直接函数。等价写法是使用 `raise` 语句：

```python
raise Exception("消息")
raise ValueError("消息")
raise RuntimeError("消息")
raise TypeError("消息")
# ... 其他内置异常类型
```

### 常见内置异常类型

| 异常类型 | 适用场景 |
|----------|---------|
| `ValueError` | 参数值不合法 |
| `TypeError` | 类型不匹配 |
| `RuntimeError` | 运行时一般错误 |
| `KeyError` | 字典键不存在 |
| `IndexError` | 序列索引越界 |
| `Exception` | 通用异常基类 |

### 自定义异常

```python
class MyError(Exception):
    pass

raise MyError("自定义错误")
```

## 要点

- Python 用 `raise 异常类型("消息")` 抛出异常，没有类似 Julia `error()` 的单函数写法。
- 优先使用具体异常类型（如 `ValueError`）而非基类 `Exception`。
- 自定义异常继承 `Exception` 即可。
