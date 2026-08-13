# README

到此为止，我们已经完全质疑 quark 的量子计算机能不能测出任何有意义的结果了(ref to [hardware_test](./hardware_test/)。但事已至此，再挣扎一下.

## 方案改进

### 环形电路

对于 pidx = -1 情况线性电路会引入大量不必要交换门。采用环形减少交换门.

### 参数设置改进

我们发现在实际的量子硬件上压根不能采用超过2次时间点的演化路线。此时复杂的演化轨迹毫无意义, 采用直线即可. 参数编码如下:

#### 离散参数

(step, pidx, order)

#### 连续参数

##### 初始参数

* 演化起点 $p0$
* 分解位置 $x_i$ (而非时间点)
* 时间步长（换元后的 $\Delta t_i$）

其中

$$
\begin{cases}
0 \le p0 \le 1\\
0 \le x_1 \le x_2 \le ... \le 1\\
0 \le \Delta t_i \le \tau
\end{cases}
$$

**默认 $\tau = 10$**.

##### 去约束

稍加换元可以将参数范围限定在 $[0, 1]$:

$$
\begin{split}
&x_i = 1 - \prod_{j=1}^i (1 - {u_x}_j) \rightarrow\\
&{u_x}_i = \frac{x_i - x_{i-1}}{1 - x_{i - 1}}, \quad x_0 = 0
\end{split}
$$

此时若 ${u_x}_i \in [0, 1]$, 必然有 $x_i \ge x_{i - 1}$;

同理对于 $\Delta t_i$ 有:

$$
\Delta t_i = u_{\Delta} * \tau
$$

where $u_\Delta \in [0, 1]$, 综上:

$$
u_{p_0}, {u_x}_i, u_\Delta \in [0, 1]
$$

此外轨迹取直线则有参数方程:

$$
\begin{split}
s_i = s_0 + a {u_x}_i\\
δ_i = δ_0 + b {u_x}_i
\end{split}
$$

where:

$$
(a, b) = (s_1 - s_0, δ_1 - δ_0)
$$

##### 去边界

如果需要SPSA算法，边界也可以去除:

$$
u = \frac{1}{1 + e^{-t}} \quad t\in [-\infin, +\infin]
$$

### 优化算法

#### 优化目标

* 对于模拟机的优化对于输入参数增加随机噪声.
* 对于quark保留原本的cost function.

#### 优化算法

对于模拟机:

* 全局优化: DIRECT_L
* 局部优化: SPSA

对于量子计算机：

* SPSA

### 计算范围

穷极计算力计算一个点即可，暂以 $s=0.5, δ=0.3$ 为例. 计算quark可以给到的最低值.
