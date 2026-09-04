---
bibliography: references.bib
collection:
  - intensive 
---
# CS robust

详细论文参考 [@Vitale-etal-2024, p. 12], 本文给出关键证明点(C5).

## two-copy local unitary “twirling channel”

定义:

$$
\tau^{2}(X) := \int dU (U^\dagger)^{\otimes 2} X U^{\otimes 2}
$$

Target, 只需要证明单比特情况下有(独立U期望可以因子化):

$$
\tau^{2}(X) = \frac{1}{3} [(TrX - \frac{1}{2}Tr(SX))I + (Tr(SX) - \frac{1}{2}TrX)S]
$$

核心思想是将单bit情况分解为I和SWAP 基.

### $U^\otimes 2$ 的对称性分解

设U为单笔特幺正变换, 注意到:

$$
[SWAP, U \otimes U] = 0
$$

所以自然可以用SWAP去标记 $U^\otimes 2$ 本征态,
或者说 $U^\otimes 2$ 无法改变态的SWAP对称性扇区,
再或者说 **$U^\otimes U$ 操作只在SWAP算符每一个对称性子空间中**.

### Schur 引理

**如果一个算符与所有 $U⊗U$ 都交换，那么在每个不可约子空间上，它只能是“常数乘单位算符”**.

$\tau^{2}(X)$ 显然满足此性质, 不可约子空间单位算符为:

$$
\begin{split}
&\hat P_+ = \frac{I + S}{2}\\
&\hat P_- = \frac{I - S}{2}\\
\end{split}
$$

因此必然有:

$$
\tau(X) = a \hat P_+ + b \hat P_-
$$

### 待定系数求解

显然,

$$
\begin{split}
&tr(X) = tr(\tau (X)) = 3a + b\\
&tr(SX) = tr(S\tau (X)) = 3a - b
\end{split}
$$

注意 $\int dU = 1, trP_\pm = 3, 1, [S, U^{\otimes 2}] = 0$; 本质上是想用 $tr(X), tr(SX)$ 表示 $a, b$,

解出 $a, b$, 代入 $\tau(X) = a \hat P_+ + b \hat P_-$ 后提取 $I, S$ 即可.

> two-copy local unitary “twirling channel” [@Vitale-etal-2024, p. 12]
