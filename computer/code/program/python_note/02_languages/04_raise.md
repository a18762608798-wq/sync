# raise

## basic

```python
raise Exception("消息") # 基类, 优先用具体的而不是这种.
raise ValueError("消息")
raise RuntimeError("消息")
raise TypeError("消息")
# ... 其他内置异常类型
```

```bash
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("余额不足")
    return balance - amount
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

- 优先使用具体异常类型（如 `ValueError`）而非基类 `Exception`。
- 自定义异常继承 `Exception` 即可。
