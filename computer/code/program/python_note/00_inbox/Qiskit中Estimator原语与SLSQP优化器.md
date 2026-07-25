# Qiskit 中 Estimator 原语与 SLSQP 优化器

## 背景/动机

在 Qiskit 中实现 VQE 时，核心工作包括两部分：用量子电路估计能量期望值（由 Estimator 原语完成），以及用经典优化器调参（如 SLSQP）。Qiskit 1.0 后引入了基于原语（Primitives）的标准化 API。

## 核心内容

### Estimator 原语

`Estimator` 是 Qiskit 中估计期望值的标准接口，替代了旧版 `VQE` 类中的手动计算方式。典型用法：

```python
from qiskit_aer.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp

# 构建哈密顿量的 Pauli 表示
hamiltonian = SparsePauliOp.from_list([
    ("ZZ", -1.05),
    ("IZ",  0.39),
    ("ZI",  0.39),
    ("XX",  0.40),
])

# 实例化 Estimator
estimator = Estimator()

# 运行：传入参数化电路和可观测量
job = estimator.run(
    circuits=[ansatz],       # 参数化电路
    observables=[hamiltonian], # 可观测量（H 的 Pauli 展开）
    parameter_values=[params], # 当前参数值
)
result = job.result()
energy = result.values[0]  # <H> 的期望值
```

Estimator 内部自动完成：
1. Pauli 串分组（逐比特对易分组，减少 measurement settings）
2. 基变换（对 X、Y 分量插入旋转门）
3. 采样并计算各 Pauli 串期望值，加权求和得到 $\langle H \rangle$

> **注**：实际部署到量子硬件时，应使用 `qiskit_runtime.Estimator` 而非 `qiskit_aer.primitives.Estimator`，后者仅用于本地模拟。

### SLSQP 优化器

SLSQP（Sequential Least Squares Programming）是一种基于梯度的序列二次规划算法，支持约束优化。在 VQE 场景中使用无约束形式：

```python
from scipy.optimize import minimize

def cost_function(params):
    # 将参数绑定到 ansatz 电路并在 Estimator 上求期望
    job = estimator.run([ansatz], [hamiltonian], [params])
    return job.result().values[0]

initial_params = [0.0] * num_params  # 初始参数

result = minimize(
    cost_function,
    initial_params,
    method="SLSQP",
    options={"maxiter": 200, "ftol": 1e-8},
)
optimal_params = result.x
optimal_energy = result.fun
```

或在 Qiskit 生态中使用内置包装：

```python
from qiskit_algorithms.optimizers import SLSQP

optimizer = SLSQP(maxiter=200, tol=1e-8)
result = optimizer.minimize(cost_function, initial_params)
```

SLSQP 在 VQE 中选择的原因：收敛较快（利用梯度信息），适合低到中等维度的无噪声/低噪声优化问题。

### 完整 VQE 工作流示意

```python
# 1. 构造分子哈密顿量
# 2. 设计 ansatz 电路（如 UCCSD）
# 3. 用 Estimator 评估 cost_function
# 4. 用 SLSQP 迭代优化参数
# 5. 得到近似基态能量
```

## 注意事项/常见误区

- `Estimator` 期望值基于有限 shot 采样，有统计误差——需根据精度需求设置 `shots` 参数
- SLSQP 需要梯度信息，VQE 中通过参数偏移（parameter shift rule）估计梯度，每次迭代需多次调用 Estimator（成本较高）
- 无噪声模拟器上 `qiskit_aer.primitives.Estimator(approximation=True)` 会直接计算精确期望值（也即通过 `Statevector`），这适合算法验证但无法体现采样噪声的影响
- 参数初始化对收敛至关重要——全零初始化或随机初始化可能导致陷入不良局部极值
