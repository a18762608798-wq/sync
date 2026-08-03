# PauliEvolutionGate + SuzukiTrotter 构建时间演化电路

**日期**: 2026-08-03 16:52
**分类**: 编程/Python
**标签**: #qiskit #PauliEvolutionGate #SuzukiTrotter #时间演化

## 背景

在 SSH model 的变分演化模拟中，需要将哈密顿量 H 按 Suzuki-Trotter 分解插入量子电路，实现 `e^{-iHΔt}` 的近似演化。

## 内容

```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import SuzukiTrotter

# 构建演化门
synth = SuzukiTrotter(order=1, reps=1)
evo = PauliEvolutionGate(H, time=Δt, synthesis=synth)
qc.append(evo, range(qubit_num))
```

- `order`：Trotter 阶数（1 阶近似）
- `reps`：重复次数
- `PauliEvolutionGate` 接收 `SparsePauliOp` 类型的哈密顿量

## 要点

- `SuzukiTrotter` 是 synthesis 策略，传入 `PauliEvolutionGate` 自动分解 Pauli 演化
- `qc.append(evo, range(qubit_num))` 将演化门作用到全部量子比特
- 电路中的门名称显示为 `"PauliEvolution"`
