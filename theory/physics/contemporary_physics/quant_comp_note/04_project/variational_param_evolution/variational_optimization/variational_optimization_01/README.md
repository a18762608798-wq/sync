# README

> 本目录属于 `variational_optimization/` 系列实验，编号 **01**。

## 项目概览

**01 · 变分初始方案初验**: 给出一个通用的变分电路方案，并初步验证其在量子计算机（模拟机 + quark 真机）上的可行性。

主要内容:

* **三层优化框架**: 外层扫 trotter 阶数 `order` 与步数 `step`，内层扫三种演化起点分支 `pidx ∈ {1, 0, -1}`，底层（`optimize_branch`）优化连续变分参数.
* **二次 Bézier 演化路径**: 演化起点、曲线控制点、时间步长、分解时间点全部换元到 $[0,1]$（Sigmoid 无约束化），共 $2N+3$ 个变分参数.
* **三阶段真机流程**（`save_qc_spectrum.py`）: 模拟机 `DIRECT_L` 全局搜索 → 模拟机 `SLSQP` 精修 → 真机 `SPSA` 微调，逐阶段以 `t0_map` 热启动.
* **产物**: `data/` 下 `aer_qc_spectrum_direct.npz`（DIRECT_L）、`aer_qc_spectrum.npz`（SLSQP 精修）、`quark_qc_spectrum.npz`（真机）.

### 与 02 的区别

| | 01 · initial（本目录） | 02 · hardware（[`../variational_optimization_02/`](../variational_optimization_02/)） |
| --- | --- | --- |
| 目标 | 验证通用变分方案的可行性 | 针对 quark 真机噪声重设计方案，榨取真机最低能量 |
| 演化路径 | 二次 Bézier 曲线，path 与 $\Delta t$ 耦合 | 直线轨迹，path 与 $\Delta t$ 解耦 |
| 电路 | 线性链式电路 | 环形电路，减少交换门 |
| 步数 | 多步（真机上不现实） | $\le 2$ 个时间点（真机约束） |
| 关键结论 | 模拟机可行，真机结果不可信 | 真机噪声主导，优化趋向零参数/更浅电路 |

此项目用来初步验证变分电路在量子计算机的可行性. 或者说给出一个通用的变分方案.

## 变分电路

### 核心思想

采用 `../../variational_outline/README.md` 描述的策略，按代码实现:

优化分为三个层次:

* **外层**（`outer_optimize`）: 对每个 **trotter 分解阶数** `order ∈ orders`，对应 `max_steps[i]` 为步数上限，迭代 `step = 1..max_s`，调用 `inner_optimize` 取全局最优.
* **内层**（`inner_optimize`）: 对三种离散 **起始边界** `pidx ∈ {1, 0, -1}` 分别调用底层的 `optimize_branch`，取 cost 最小的分支；所有分支均失败则抛 `RuntimeError`.
* **底层**（`optimize_branch`）: 固定 `pidx`, `step`, `order`，优化连续变分参数.

内部对于**演化起点**, **二次 Bézier 曲线的控制参数**, **时间步长**(绝热演化长时间优势和trotter分解误差的均衡), **分解时间点** 作为变分参数, 全部换元到 $[0,1]$ 范围. cost function 是:

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
* 时间步长（换元后的 $u_{\Delta t_n}$）
* 分解时间点 $d_n$ (相对当前步长百分比)

底层优化变量经过**两层换元**（共 $2N+3$ 个）:

1. **Sigmoid 换元**：优化器直接操作的变量是**无约束实数向量** $t \in \mathbb{R}^{2N+3}$，通过
   $u = \sigma(t) = 1/(1+e^{-t})$ 映射到 $[0,1]$，无需任何显式约束。
2. **线性换元**：$[0,1]$ 变量再映射到物理参数域。

$$
t = [\,t_{v_0},\; t_{u_s},\; t_{u_\delta},\; t_{u_{\Delta t_1}},\dots,t_{u_{\Delta t_N}},\; t_{d_1},\dots,t_{d_N}\,]
$$

默认初值（`_default_t0`）为全零向量 $t=0$，对应 $u=\sigma(0)=0.5$。

> 此方案受到之前绝热烟花的思想将曲线path直接和Δt想干。这会引入完全不必要的参数依赖。在hardware optimization中将解藕这种依赖.

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
Δt_n \in (0, τ)
$$

代码中暂取 $τ = 10$（**trotter分解误差一定抵消绝热优势影响点**，这个值可大不可小).

为统一到 $[0,1]$ 约束，将 $Δt_n$ 换元为一个自由参数 $u_{\Delta t_n} \in [0,1]$:

$$
\boxed{Δt_n = τ\,u_{\Delta t_n}}
\qquad
u_{\Delta t_n} \in [0,1]
$$

当 $u_{\Delta t_n}=0$ 时 $Δt_n=0$，$u_{\Delta t_n}=1$ 时 $Δt_n=τ$，$u_{\Delta t_n}=0.5$ 时 $Δt_n=0.5τ$（区间中点）.

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

#### Sigmoid 换元（推荐, 已实现）

为避免显式约束（尤其是 COBYLA 等部分优化器需手动列出每个变量的上下界），
将所有 $2N+3$ 个参数换元为无约束实数向量 $t \in \mathbb{R}^{2N+3}$，
再经 sigmoid 映射到 $[0,1]$，以此自动满足所有物理边界:

$$
\boxed{u = \sigma(t) = \frac{1}{1+e^{-t}}}
\qquad
t \in \mathbb{R},\; u \in [0,1]
$$

**优点:**

* $t$ 无限范围，任何无约束优化器（SLSQP/SPSA/DIRECT_L）均可直接使用，无需 bounds/constraints。
* $\sigma(t)$ 光滑可导，数值梯度法稳定。
* $\sigma(0)=0.5$，默认初值 $t_0=0$ 自然对应各参数的区间中点。

**代价:** 优化结果 $t^*$ 需要逆变换 $u = \sigma(t^*)$ 得到 $[0,1]$ 参数，再经下文的线性换元得到物理参数。

#### 线性控制点换元

控制点 $s_p, δ_p$ 已用 $[0,1]$ 变量 $(u_s, u_\delta)$ 线性换元（配合 sigmoid 外层包裹）:

$$
\boxed{
\begin{aligned}
s_p &= s_0 + u_s\,(s_1 - s_0)\\
δ_p &= δ_0 + u_\delta\,(δ_1 - δ_0)
\end{aligned}}
\qquad
u_s, u_\delta \in [0, 1]
$$

同理 $Δt_n = T\,u_{\Delta t_n}$，$T=10$（代码中 `T = 10`）。

### 优化算法

* 模拟机: 使用全局优化算法(DIRECT_L)后，用局部优化算法(SLSQP)精修.
* 量子计算机: 使用局部优化算法(真机计算速度会导致收敛很慢), SPSA

## 尝试效果

### 对比范围

暂取 $δ_1 = 0.3$, $N = 8$, 扫描 $s_1 \in \{0.1, \dots, 0.8\}$（`save_qc_spectrum.py` 中 `slist = np.arange(0.1, 0.9, 0.1)`），外层 `orders = [1, 2]`, `max_steps = [3, 2]`. 底层优化使用 qiskit_algorithms 优化器（`SLSQP`/`SPSA`/`DIRECT_L`），对 quafu 量子计算机和 qiskit 模拟机对比变分结果与所用步长.

### 变分结果评估

#### 能量

绘制理论能谱 $E_0, E_1$, 由于:

$$
\sum_i P_i E_i = 1 \Rightarrow P_0 \ge \frac{\hat E - (1 - p_0) E_1}{E_0}
$$

其中 $\hat E$ 为能量估计量, 也就是非常容易给出 $P_0$ 下界，只要优化结果在 $E_0$ 和 $E_1$ 之间.

> 这个方案quark不可用，因为结果过于离谱压根不在基态和激发态之间.

#### 保真度

代价较高，待定.

## 真机优化

### 优化起点（已实现）

采用三阶段优化流程（`save_qc_spectrum.py` 的 `main`），每段都会把每个 `(order, step, phase_idx)` 的 `t0_map` 与 `history` 存成 npz:

1. **模拟机全局搜索**: `DIRECT_L` 在整个 $s$ 扫描上全局优化，得到初始 `t0_map`。
2. **模拟机精修**: `SLSQP` 以 DIRECT_L 结果为初值精细优化，覆盖 `t0_map`。
3. **真机微调**: `SPSA` 以模拟机 SLSQP 结果为初值，在真机（如 `Baihua`）上重新优化。

`t0_map` 通过 `load_t0_maps` 从上一阶段 npz 读出，作为下一阶段初值（热启动）。

### 比特选择

全是 "[138, 125, 126, 127, 128, 129, 142, 141]"。

没有选择成环状电路，如果 qidx = -1 结果明显差于其他，可以考虑环状电路.
