# Qiskit U3 gate 矩阵定义与 U† 构造

**日期**: 2026-07-20
**分类**: 编程/Python
**标签**: #qiskit #量子计算 #U3 #classical_shadow

## 背景

在 qmeas 随机测量项目中，需要在电路测量前施加随机 U3 旋转的逆（dagger），用于 classical shadow 协议中的 POVM 构造。Julia 后处理端也需要正确定义 U3 矩阵以重建 shadow snapshot。

## 内容

### Qiskit U3 矩阵定义

Qiskit 的 `QuantumCircuit.u(theta, phi, lam, qubit)` 实现以下矩阵：

$$
U_3(\theta, \phi, \lambda) =
\begin{pmatrix}
\cos\frac{\theta}{2} & -e^{i\lambda} \sin\frac{\theta}{2} \\
e^{i\phi} \sin\frac{\theta}{2} & e^{i(\phi+\lambda)} \cos\frac{\theta}{2}
\end{pmatrix}
$$

### U3† 的构造方式

在 qmeas 中，电路施加的不是 U3 本身而是其 dagger。通过给参数取反实现：

```python
def add_meas(qc, params, meas_indices):
    theta, llambda = params[0], params[1]
    for param_idx in range(len(meas_indices)):
        qubit_idx = meas_indices[param_idx]
        # U^dag: U3(theta, 0, lambda)^† = U3(-theta, -lambda, 0)
        qc.u(-theta[param_idx], -llambda[param_idx], 0, qubit_idx)
    qc.measure(meas_indices, range(len(meas_indices)))
    return qc
```

这是因为 $U_3(\theta, \phi, \lambda)^\dagger = U_3(-\theta, -\lambda, -\phi)$，当 $\phi=0$ 时简化为 $U_3(-\theta, -\lambda, 0)$。

### Classical shadow 中的用法

电路施加 $U^\dagger$ 后测 Z 基，POVM effect 为 $U^\dagger |s\rangle\langle s| U$。对于 Pauli 随机测量，classical shadow snapshot 为：

$$\hat{\rho}_s = \mathcal{M}^{-1}(U^\dagger |s\rangle\langle s| U) = 3\, U^\dagger |s\rangle\langle s| U - I$$

## 要点

- `qc.u(theta, phi, lam, qubit)` 是 Qiskit 的 U3 门便捷接口
- 构造 U3† 无需 `.inverse()` 方法，直接 `u(-θ, -λ, 0)` 即可
- 存储的参数 (θ, λ) 对应的是正变换 U，电路施加的是 U†，后处理时也应对应使用 U†
