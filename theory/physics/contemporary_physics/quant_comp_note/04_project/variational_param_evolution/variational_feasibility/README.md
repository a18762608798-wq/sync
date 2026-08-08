# README

此项目用来验证变分电路在量子计算机的可行性.

## 变分电路

### 核心思想

采用 `../variational_outline/README.md` 描述的策略，按代码实现:

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

这里 $ϵ$ 暂且取1（代码 `create_op.py::get_ssh_constrained_H` 默认 `ϵ=1`）.

### 变分参数编码

**不妨设外层 trotter 分解阶数为 $K$, 步数为 $N$, 内层离散分支 $pidx$ 已在 $inner\_optimize$ 内部循环**, 底层 `optimize_branch` 固定 $K$, $N$, $pidx$，优化以下连续参数:

* 演化起点 $v_0$
* 二次 Bezier 曲线的控制参数（线性换元后的 $(u_s, u_\delta)$）
* 时间步长 $Δt_n$
* 分解时间点 $d_n$ (相对当前步长百分比)

底层优化变量按如下顺序编码（对应 `var_optimization.py::objective`，共 $2N+3$ 个）:

$$
x = [\,v_0,\; u_s,\; u_\delta,\; \Delta t_1,\dots,\Delta t_N,\; d_1,\dots,d_N\,]
$$

默认初值（`_default_x0`）为 $v_0 = u_s = u_\delta = d_n = 0.5,\; \Delta t_n = 5$.

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
Δt_n \in (10^{-3}τ, τ)
$$

代码中暂取 $τ = 10$（**trotter分解误差一定抵消绝热优势影响点**，待我在模拟机上看一下）. 对很小的 $Δt_n$ 默认根本不需要这一步.

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

注意: 当 $pidx=-1$ 时 $s_0=1 > s_1$，如果直接用 $[s_0, s_1]$ 会得到空集（约束不可行），
这正是之前 `pidx=-1` 分支 SLSQP 失败的根因。

#### 线性换元（推荐, 已实现）

为避免 `min/max` 动态约束（尤其是 `pidx=-1` 时依赖另一个优化变量 $v_0$ 导致的麻烦），
将控制点换元为两个 $[0,1]$ 自由参数 $(u_s, u_\delta)$:

$$
\boxed{
\begin{aligned}
s_p &= s_0 + u_s\,(s_1 - s_0)\\
δ_p &= δ_0 + u_\delta\,(δ_1 - δ_0)
\end{aligned}}
\qquad
u_s, u_\delta \in [0, 1]
$$

**优点:**

* $u_s, u_\delta \in [0,1]$ 自动保证 $s_p \in [\min(s_0,s_1),\max(s_0,s_1)]$，即使 $s_0 > s_1$（如 $pidx=-1$）也成立，无需 `min/max`。
* 原来的 4 条动态不等式约束全部删除，只需保留对每个变量的 box 约束。实际代码（`optimize_branch`）因 `COBYLA` 忽略 `Bounds`，会把每个变量的上下界转成显式不等式约束。
* 线性插值（Bezier 控制点在中点方向）语义直观，$u_s=u_\delta=0.5$ 即区间中点，初始值可直接取 $0.5$。

**代价:** 优化后的 `result.x[1]`, `result.x[2]` 是 $(u_s, u_\delta)$ 而非 $(s_p, δ_p)$。
若要输出真实路径控制参数，需做逆变换:

$$
s_p = s_0 + u_s\,(s_1 - s_0), \qquad
δ_p = δ_0 + u_\delta\,(δ_1 - δ_0)
$$

## 具体内容

### 对比范围

暂取 $δ_1 = 0.3$, $N = 8$, 扫描 $s_1 \in \{0.1, \dots, 0.8\}$（`save_qc_spectrum.py` 中 `slist = np.arange(0.1, 0.9, 0.1)`），外层 `orders = [1, 2]`, `max_steps = [3, 2]`. 底层优化方法为 `COBYLA`，对 quafu 量子计算机和 qiskit 模拟机对比变分结果与所用步长.

### 变分结果评估

#### 能量

绘制理论能谱 $E_0, E_1$, 由于:

$$
\sum_i P_i E_i = 1 \Rightarrow P_0 \ge \frac{\hat E - (1 - p_0) E_1}{E_0}
$$

其中 $\hat E$ 为能量估计量, 也就是非常容易给出 $P_0$ 下界，只要优化结果在 $E_0$ 和 $E_1$ 之间.

#### 保真度

代价较高，待定.

## 真机优化

### 优化起点（已实现）

已实现从模拟机结果作真机初值: 先在 qiskit_aer 上跑完整个 $s$ 扫描，保存每个 `(order, step, phase_idx)` 的最优参数 `x0_map` 到 `data/aer_qc_spectrum.npz`，再以该初值在真机（如 `Baihua`）上重新优化（`save_qc_spectrum.py` 的 `main`）。真机 `maxiter` 较小（2000 vs 模拟机 20000）。
