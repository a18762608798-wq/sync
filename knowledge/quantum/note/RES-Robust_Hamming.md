# Robust Hamming

## ASSUME

**REQUIRE:**

(1) 门无关: $\Lambda$ 不依赖 $U$.

(2) 噪声通道在iteration内视为不变.

(3) 噪声在随机U之后测量之前.

(4) $|0\rangle$ 制备高保真.

(5) 噪声局域: $\Lambda=\otimes_i\Lambda_i$.

(6) TP: $tr(\Lambda(\rho)) = tr(\rho) \rightarrow \Lambda^{\ast}(I) = I$

**BY:**

[Robust Shadow](RES-Robust_Shadow.md)

**ASSUME:**

(7) $\Lambda_k(I) = (1+\delta_k)|0\rangle\langle 0| + (1-\delta_k)|1\rangle\langle 1|,\quad k=1,2$

**WHERE:**

阻尼偏置

$$
\delta_k = \gamma_k = 1-e^{-t_k/T_1}
$$

$\delta_k$ 由 $t_k$ 决定, 假设(2)噪声不变即假设同一发内 $t_k$ 不变.

## purity

**BY:**

[PRF-RHT_purity](PRF-RHT_purity.md)

**CONCEPT:**

$$
\hat{\mathcal{P}} = \frac{1}{MK(K-1)} \sum_{m}\sum_{k, k', k\neq k'}\prod_i \hat{g}_i(s_i^{(m, k)}, s_i^{(m, k')})
$$

where

$$
\begin{cases}
\hat{g}_i(0, 0) = \hat{g}_i(1, 1) = \hat{x}_i\\
\hat{g}_i(0, 1) = \hat{g}_i(1, 0) = \hat{y}_i
\end{cases}
$$

**WHERE:**

$$
\begin{split}
&\hat{x}_i = \frac{\hat{p}_i + \hat{q}_i}{2}, \quad \hat{y}_i = \frac{\hat{p}_i - \hat{q}_i}{2}\\
&\hat{p}_i = 1 - \hat{\varepsilon}_i \hat{q}_i, \quad \hat{q}_i = \frac{3}{\hat{A}_i - 1 - \hat{\varepsilon}_i}\\
&\hat{\varepsilon}_i = \hat{\delta}_{1, i}\hat{\delta}_{2, i}, \quad \hat{A}_i = 6\hat{R}_i - 2 - 2\hat{\varepsilon}_i\\
&\hat{\delta}_{1, i} = \hat{\delta}_{2, i} = \hat{\delta}_{i} = 2\hat{f}_{0, i} - 1\\
&\hat{R}_i = \frac{1}{MK(K-1)} \sum_{m}\sum_{k, k', k\neq k'} \delta_{s_i^{(m, k)}, s_i^{(m, k')}}, \quad \hat{f}_{0, i} = \frac{1   }{MK} \sum_{m, k} \delta_{0, s_i^{(m, k)}}
\end{split}
$$

**INTERPRET:**

- 纯度的hamming公式pair位于同一个比特, 噪声通道是相等的.
- $\hat{g}$ 具体选择 $x_i$ 还是 $y_i$ 取决于态制备电路; $x_i$ 和 $y_i$ 的具体形式(也即 $\hat R$ 和 $\hat f$)取决于 $|0\rangle$ 电路.

**PROPERTY:**

$$
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}] = tr(\rho^2)
$$

**CHECK:**

无噪声时,

$\delta_{i} = 0$, $\varepsilon_{i} = 0$.

$\rho_{i} = |0\rangle\langle 0|$,
$\sigma_{i} = U_{i}\rho_{i}U_{i}^{\dagger}$:

$$
R_{i} = \mathbb E_{U_{i}}[\sum_{s_{i}}P(s_{i}|U_{i})^{2}]
$$

$$
= \sum_{s_{i}}tr(\mathbb E_{U_{i}}[\sigma_{i}^{\otimes 2}]\,|s_{i}\rangle\langle s_{i}|^{\otimes 2})
$$

**CONSIDER:**

$$
\mathbb E_{U_{i}}[\sigma_{i}^{\otimes 2}] = \frac{I + S_{i}}{6}
$$

**BY:**

[PRF-Hamming_core](./PRF-Hamming_core.md), 相同的计算方式, 可以计算出系数都为 $\frac{1}{6}$.

**HAVE:**

$$
R_i = \frac{1}{6}tr((I + S)|00\rangle \langle 00| + (I + S)|11\rangle \langle 11|) = \frac{2}{3}
$$

**THEREFORE:**

$A_{i} = 6 \times \frac{2}{3} - 2 - 0 = 2$,

$q_{i} = 3$, $p_{i} = 1$,

$x_{i} = 2$, $y_{i} = -1$, 回到标准 Hamming 核.

## ZR

**BY:**

[RHT ZR](PRF-RHT_ZR.md)

**CONCEPT:**

$$
\hat Z_{\mathcal R} = \frac{1}{MK} \sum_{m}\sum_{k}\prod_{i=1}^n \hat g_i(s_i^{(m, k)}, s_{\bar i}^{(m, k)})
$$

where

$$
\begin{cases}
\hat g_i(0, 0) = \hat g_i(1, 1) = \hat x_i\\
\hat g_i(0, 1) = \hat g_i(1, 0) = \hat y_i
\end{cases}
$$

$i$ is the subscript of mirror pair, $\bar i$ is its reflection counterpart, $n$ is the number of pairs.

**WHERE:**

$$
\begin{split}
&\hat x_i = \frac{\hat p_i + \hat q_i}{2}, \quad \hat y_i = \frac{\hat p_i - \hat q_i}{2}\\
&\hat p_i = 1 - \hat \varepsilon_i \hat q_i, \quad \hat q_i = \frac{3}{\hat A_i - 1 - \hat \varepsilon_i}\\
&\hat \varepsilon_i = \hat \delta_{i}\hat \delta_{\bar i}, \quad \hat A_i = 6\hat R_i - 2 - 2\hat \varepsilon_i\\
&\hat \delta_{i} = 2\hat f_{0, i} - 1, \quad \hat \delta_{\bar i} = 2\hat f_{0, \bar i} - 1\\
&\hat R_i = \frac{1}{MK} \sum_{m, k} \delta_{s_i^{(m, k)}, s_{\bar i}^{(m, k)}}, \quad \hat f_{0, i} = \frac{1}{MK} \sum_{m, k} \delta_{0, s_i^{(m, k)}}, \quad \hat f_{0, \bar i} = \frac{1}{MK} \sum_{m, k} \delta_{0, s_{\bar i}^{(m, k)}}
\end{split}
$$

**INTERPRET:**

- ZR 的 hamming formula pair 位于同一发的镜像对上, 噪声通道是两点各自一个.
- 这里的 $i$ 读成对标号, 不是比特标号; $\hat f_{0, i}$ 与 $\hat f_{0, \bar i}$ 由对内左右两点各自的单点计数分别估计.

**PROPERTY:**

$$
\mathbb E_{U, s}[\hat Z_{\mathcal R}] = tr(\rho \mathcal R) = Z_{\mathcal R}
$$

## ZT

**BY:**

[RHT ZT](PRF-RHT_ZT.md)

**CONCEPT:**

$$
\hat Z_{\mathcal T} = \frac{1}{MK^2} \sum_{m}\sum_{k, k'}\prod_{i \in I} \hat{g}_i(s_i^{(m, k)}, s_i^{\prime(m, k')})
$$

where

$$
\begin{cases}
\hat{g}_i(0, 0) = \hat{g}_i(1, 1) = \hat{x}_i\\
\hat{g}_i(0, 1) = \hat{g}_i(1, 0) = \hat{y}_i
\end{cases}
$$

$I = I_1 \cup I_2$ 是两次实验共用的 $2n$ 比特区间, $k$ ($k'$) 是实验 1 (实验 2) 的 shot 标记, 两发天然独立故无 $k \neq k'$ 约束.

**WHERE:**

$$
\begin{split}
&\hat{x}_i = \frac{\hat{p}_i + \hat{q}_i}{2}, \quad \hat{y}_i = \frac{\hat{p}_i - \hat{q}_i}{2}\\
&\hat{p}_i = 1 - \hat{\varepsilon}_i \hat{q}_i, \quad \hat{q}_i = \frac{3}{\hat{A}_i - 1 - \hat{\varepsilon}_i}\\
&\hat{\varepsilon}_i = \hat{\delta}_{1, i}\hat{\delta}_{2, i}, \quad \hat{A}_i = 6\hat{R}_i - 2 - 2\hat{\varepsilon}_i\\
&\hat{\delta}_{1, i} = 2\hat{f}_{0, i}^{(1)} - 1, \quad \hat{\delta}_{2, i} = 2\hat{f}_{0, i}^{(2)} - 1\\
&\hat{R}_i = \frac{1}{MK^2} \sum_{m}\sum_{k, k'} \delta_{s_i^{(m, k)}, s_i^{\prime(m, k')}}, \quad \hat{f}_{0, i}^{(a)} = \frac{1}{MK} \sum_{m, k} \delta_{0, s_i^{(m, k, a)}}
\end{split}
$$

**INTERPRET:**

- ZT 的 hamming formula pair 位于两次实验的同一比特, $i$ 逐比特取遍 $I_1 \cup I_2$.
- 实验 1 在 $I_1$ 上先作用 $u_{\mathcal T}$; 两次实验在 $I_1$ 上的随机幺正取共轭配对, 在 $I_2$ 上取相同, 但标定量 $\hat R_i, \hat f$ 只用读出计数, 形式与 purity 相同.
- $\hat{g}$ 具体选择 $x_i$ 还是 $y_i$ 取决于态制备电路; $x_i$ 和 $y_i$ 的具体形式(也即 $\hat R$ 和 $\hat f$)取决于 $|0\rangle$ 电路.
- 标定 trivial 取共轭配对：exp1 用 plain，exp2 用共轭绑定；两份实验共用同一积分变量 $U_i$，实验二在 $I_1$ 区的 Born 概率实际按 $U_i^{\ast}$ 计算。

**PROPERTY:**

$$
\mathbb E_{U, s, s'}[\hat Z_{\mathcal T}] = Z_{\mathcal T}
$$

## VERIFY

- 状态: 已通过
- 目录: `VER-Robust_Hamming/`
- 内容:
  - `purity`: 验证同设置跨发配对下 $R_i, f_{0,i} \to x_i, y_i$ 标定链、$\tau^F_i(w_i) = S_i$ 及 $\hat{\mathcal P}$ 无偏性.
  - `ZR`: 验证单发内镜像对配对下 $R_i, f_{0,i}, f_{0,\bar i} \to x_i, y_i$ 标定链及 $\hat Z_{\mathcal R}$ 无偏性.
  - `ZT`: 验证跨实验共轭/相同配对下 $\tau^\Psi_i(w_i) = T_i$, $\tau^F_i(w_i) = S_i$ 标定链及 $\hat Z_{\mathcal T}$ 无偏性.
