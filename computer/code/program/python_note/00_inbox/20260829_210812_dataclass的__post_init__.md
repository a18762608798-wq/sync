# dataclass 的 `__post_init__`

```python
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    output_dir: str = "./data"
    group_num: int = 2

    def __post_init__(self) -> None:
        self.output_dir = Path(self.output_dir)
        self.params = [f"p{i}" for i in range(self.group_num)]
        if self.group_num <= 0:
            raise ValueError("group_num must be positive")
```

## 作用

`@dataclass` 自动生成的 `__init__` 在给所有字段赋完值后，会再调用一次 `__post_init__(self)`，用于初始化后的后处理：

- **归一化输入**：如把 `str` 转成 `Path`
- **派生属性**：计算不对外暴露的辅助属性（上面例子里 `self.params` 不是 dataclass 字段，靠 `__post_init__` 挂上去）
- **校验**：检查字段组合是否合法，不合法抛异常

## 关键行为

- **只有 dataclass 下才会自动调用**。普通类里 `__post_init__` 只是一个普通方法，没人会调它；除非手写 `__init__` 自己调，或继承自某个 dataclass。
- **`frozen=True` 的 dataclass 里赋值要绕过冻结**：用 `object.__setattr__(self, "output_dir", ...)`，直接赋值会抛 `FrozenInstanceError`。
- 签名只收 `self`，此时所有字段已赋好值，可以放心读取。

## 实例

qmeas 项目 `src/qmeas/random/config.py` 中的 `RandomMeasConfig`（未 frozen，直接赋值即可）：

```python
@dataclass
class RandomMeasConfig:
    qc: QuantumCircuit
    setting_runs: list[SettingRun]
    meas_indices: list[tuple[int, ...]]
    output_dir: Path = field(default_factory=lambda: Path("./data"))

    def __post_init__(self) -> None:
        self.output_dir = Path(self.output_dir)          # 归一化
        self.params = [ParameterVector("theta", len(self.meas_indices)),
                       ParameterVector("phi", len(self.meas_indices))]  # 派生
        if not self.setting_runs:                          # 校验
            raise ValueError("setting_runs cannot be empty")
```
