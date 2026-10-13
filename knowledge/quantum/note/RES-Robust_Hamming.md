# Robust Hamming

## ASSUME

**REQUIRE:**

(1) 门无关: $\Lambda$ 不依赖 $U$.

(2) 噪声通道在iteration内视为不变.

(3) 噪声在随机U之后测量之前.

(4) $|0\rangle$ 制备高保真.

(5) 噪声局域: $\Lambda=\otimes_i\Lambda_i$.

(6) TP: $tr(\Lambda(\rho)) = tr(\rho) \rightarrow \Lambda^*(I) = I$

**BY:**

[Robust Shadow](RES-Robust_Shadow.md)

**ASSUME:**

(7) $\Lambda_k(I) = (1+\delta_k)|0\rangle\langle 0| + (1-\delta_k)|1\rangle\langle 1|,\quad k=1,2$

**WHERE:**

阻尼偏置

$$
\delta_k = \gamma_k = 1-e^{-t_k/T_1}
$$

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
- $\hat{f}_{0, i}$ 需要在 $|0\rangle$ 后接随机 $U_i$.
- $\hat{g}$ 具体选择 $x_i$ 还是 $y_i$ 取决于态制备电路; $x_i$ 和 $y_i$ 的具体形式(也即 $\hat R$ 和 $\hat f$)取决于 $|0\rangle$ 电路.

**PROPERTY:**

$$
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}] = tr(\rho^2)
$$
