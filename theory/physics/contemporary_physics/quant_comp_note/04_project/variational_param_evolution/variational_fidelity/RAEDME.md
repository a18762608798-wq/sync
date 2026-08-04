# README

此项目用来验证变分电路在量子计算机的可行性.

## 变分电路

### 核心思想

采用 `../variational_approach/README.md` 的一个改进版本:

优化分为三个层次:

* **外层**（`outer_optimize`）: 对每个 **trotter 分解阶数** `order ∈ orders`，对应 `max_steps[i]` 为步数上限，迭代 `step = 1..max_s`，调用 `inner_optimize` 取全局最优.
* **内层**（`inner_optimize`）: 对三种离散 **起始边界** `pidx ∈ {1, 0, -1}` 分别调用底层的 `optimize_branch`，取 cost 最小的分支；所有分支均失败则抛 `RuntimeError`.
* **底层**（`optimize_branch`）: 固定 `pidx`, `step`, `order`，优化连续变分参数.

内部对于**演化起点**, **二次 Bézier 曲线的控制参数**, **时间步长**(绝热演化长时间优势和trotter分解误差的均衡), **分解时间点** 作为变分参数. cost function 是:

$$
\begin{split}
H_c &= (1-s) \sum_{i\text{ odd}} (X_i X_{i+1} + \delta Z_i Z_{i+1}) + s \sum_{j\text{ even}} (X_j X_{j+1} + \delta Z_j Z_{j+1}) \\
&- ϵ(\prod_{i=1}^{N} X_i + 2\prod_{i=1}^{N}Z_i) \\
\end{split}
$$

这里 $ϵ$ 暂且取1.

### 变分参数编码

**不妨设外层 trotter 分解阶数为 $K$, 步数为 $N$, 内层离散分支 $pidx$ 已在 $inner\_optimize$ 内部循环**, 底层 `optimize_branch` 固定 $K$, $N$, $pidx$，优化以下连续参数:

* 演化起点 $v_0$
* 二次 Bezier 曲线的控制参数 $(s_p, δ_p)$
* 时间步长 $Δt_n$
* 分解时间点 $d_n$ (相对当前步长百分比)

#### 演化起点

演化起点有三种, 由外层离散分支 $pidx \in \{1, 0, -1\}$ 选定, 对应三种不同的 initial state. 内层用一个自由参数 $v_0 \in [0, 1]$ 表示起点中非固定的分量:

若 $pidx = 1$, 有:

$$
\begin{cases}
\text{phase idx} = 1\\
s_0 = 0\\
δ_0 = v_0
\end{cases}
$$

若 $pidx = 0$, 有:

$$
\begin{cases}
\text{phase idx} = 0\\
s_0 = v_0\\
δ_0 = 0
\end{cases}
$$

若 $pidx = -1$, 有:

$$
\begin{cases}
\text{phase idx} = -1\\
s_0 = 1\\
δ_0 = v_0
\end{cases}
$$

即 $v_0$ 在 $pidx = 1, -1$ 时表示 $δ_0$, 在 $pidx = 0$ 时表示 $s_0$.

#### 二次 Bezier 曲线的控制参数

控制点应落在两端点之间（注意 `pidx=-1` 时 $s_0 > s_1$，不能假设大小顺序）:

$$
\begin{aligned}
s_p &\in [\min(s_0, s_1), \max(s_0, s_1)] \\
δ_p &\in [\min(δ_0, δ_1), \max(δ_0, δ_1)]
\end{aligned}
$$

#### 时间步长

$$
Δt_n \in (10^{-6}, τ)
$$

代码中暂取 $τ = 10$（**trotter分解误差一定抵消绝热优势影响点**，待我在模拟机上看一下）.

#### 分解时间点

$$
d_n \in [0, 1]
$$

### 变分参数约束

主要是不等式约束，有:

$$
\begin{cases}
s_p \in [\min(s_0, s_1), \max(s_0, s_1)] \\
δ_p \in [\min(δ_0, δ_1), \max(δ_0, δ_1)] \\
\end{cases}
$$

实际会在两端留出一定冗余: 代码中约束统一加 $10^{-6}$ 松弛, 避免初始点落在约束边界上导致 SLSQP 找不到可行下降方向.

注意: 当 $pidx=-1$ 时 $s_0=1 > s_1$，如果直接用 $[s_0, s_1]$ 会得到空集（约束不可行），
这正是之前 `pidx=-1` 分支 SLSQP 失败的根因。





