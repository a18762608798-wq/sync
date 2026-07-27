# QuantumToolbox 中量子对象操作基础：eigenstates、ptrace、dims

**日期**: 2026-07-27 20:09
**分类**: 编程/Julia
**标签**: #Julia #QuantumToolbox #API #量子计算

## 背景

在 SSH 模型变分参数演化项目中，使用 QuantumToolbox 库求解哈密顿量的基态和计算零点关联值，涉及 `eigenstates`、`ptrace`、`tr` 等函数的正确用法。

## 内容

### eigenstates 的 sortby 参数

```julia
eigenstates(H; sparse=true, eigvals=1, sortby=real, rev=false)
```

- `sortby=real`：按特征值的**实部**升序排序
- `eigvals=1`：返回实部最小的 1 个本征值（即基态）
- 对于 Hermitian 哈密顿量（如 SSH），所有特征值都是实数，但数值误差可能产生微小虚部，`sortby=real` 确保排序正确
- 如果不指定，默认可能按复数的 **magnitude** 排序，导致结果错误
- **注意**：`eigenstates` 返回的第二个返回值是 **`Vector{Ket}`**，即使 `eigvals=1` 也是向量，需要用 `states[1]` 取出

### ptrace 的参数语义

```julia
ρ1 = ptrace(ρ, (1, 2))  # 保留子系统 1、2，trace out 其余
```

- `ptrace` 的第二个参数是**要保留的子系统索引**
- 索引从 1 开始
- 要求 `ρ` 具有正确的子系统维数（dims）信息

### 从 Qobj 提取子系统数目

```julia
# 错误：返回矩阵维数（如 16 表示 16×16 矩阵）
qubit_num = first(size(ρ))   # ×

# 正确：返回子系统个数（如 4 表示 4 比特）
qubit_num = length(first(ρ.dims))   # ✓
```

- `ρ.dims` 存储了量子对象的子系统结构
- 对于算符（密度矩阵），`ρ.dims[1]` 是行空间的子系统维数向量

### 计算期望值

```julia
# 错误
tr(ρ, op)   # ×

# 正确
tr(ρ * op)   # ✓
```

- QuantumToolbox 中 `tr(ρ)` 计算迹，`tr(ρ * op)` 计算 $\text{tr}(\rho \hat{O})$，没有 `tr(ρ, op)` 这种两参数形式

## 要点

- `eigenstates` 的 `sortby=real` 确保按实部排序本征值，防止数值虚部干扰
- `ptrace` 的第二个参数是**保留**的子系统索引
- 从 `ρ.dims` 而不是 `size(ρ)` 获取子系统数目
- 期望值用 `tr(ρ * op)` 而非 `tr(ρ, op)` 计算
