# PEB

如果你主要问的是 **Python 变量/函数/类的命名规范**，最常见的一套就是 PEP 8。实战里可以记下面这些。

| 类型       | 推荐写法               | 示例                             |
| -------- | ------------------ | ------------------------------ |
| 普通变量     | `snake_case`       | `user_name`, `learning_rate`   |
| 函数       | `snake_case`       | `get_user_info()`              |
| 方法       | `snake_case`       | `calculate_loss()`             |
| 类        | `PascalCase`       | `QuantumCircuit`, `DataLoader` |
| 常量       | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `DEFAULT_PORT`     |
| 模块 `.py` | 小写 + 下划线           | `quantum_utils.py`             |
| 包名       | 简短小写               | `numpy`, `torchvision`         |
| 私有成员     | `_` 开头             | `_hidden_state`                |
| 特殊方法     | 双下划线               | `__init__`, `__len__`          |
