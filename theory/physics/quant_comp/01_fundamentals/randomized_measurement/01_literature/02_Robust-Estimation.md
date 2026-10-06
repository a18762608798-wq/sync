---
bibliography: references.bib
collection:
  - intensive 
---
# Robust Estimation

## CS shadow

## Asummption

- shadow

| # | 内容 | 出处 |
| --- | --- | --- |
| 1 | 门无关：$\Lambda$ 不依赖 $U$（弱门依赖可被 twirl 抹掉） | 原文 |
| 2 | 局域：$\Lambda=\otimes_j\Lambda_j$（附录 E 可验） | 原文 |
| 3 | Markovian + iteration 内平稳；噪声在幺正之后、测量之前；$\rho$ 制备干净、$\|0\rangle$ 可高保真制备；漂移靠交错 iteration 跟踪 | 原文 |
| 4 | 保迹 TP（等价于伴随保单位元 $\Lambda^*(I)=I$；式 (3) 只到此为止） | 原文（隐含） |

- hamming

hamming 有两个而外假设:

| # | 内容 | 出处 |
| --- | --- | --- |
| 5 | Pair 同分布(在求纯度时只是操作要求)：同一 $U$ 下 pair 两腿看同一个 $\Lambda$，且 $m\ne m'$ 独立 | 名义原文也有（单 $U$ 下多 shots 默认 i.i.d.），但 Hamming 更严：漂移在这里变 bias 而不只是方差，且 calibration 必须同结构配对 |
| 6 | Unital $\Lambda(I)=I$（至少对角元相等）：$t$ 方程和 calibration 的 $\mathrm{tr}D_j=2$ 要用；$T_1$ 型需多标 $\delta$ | **Hamming 新增**，原文靠 $\beta\mathbb{1}$ 躲掉 |

> Hamming 误差缓解相对 robust shadow，**物理假设只多半条**

 **关于 #6**：本推导默认 unital
（至少 $\Lambda(I)$ 对角元相等），
$t$ 方程与 calibration 的 $\mathrm{tr}D_j=2$ 都依赖它。
若去掉该假设（如 $T_1$ 型非 unital 噪声），
则 $\Lambda(I) = (1 + \gamma)|0\rangle \langle 0| + (1 - \gamma)|1\rangle \langle 1|$
需每比特多标一个 $\delta_j$(只考虑$T_1$噪声作用非unital那就是$\gamma$)，

## hamming distance

> 我目前没有看见明显的要求噪声通道相同的约束.

### revised noise hamming core

The version of noiseless ref to [hamming_noiseless](./00_proofs/twirling/hamming_noiseless.md),

Now we try to give the mitigation of hamming distance.

The ideal noise Born rule is

$$
\begin{split}
P_\Lambda(s|U)=\langle s|\Lambda(U\rho U^\dagger)|s\rangle
=\mathrm{tr}\bigr(\rho\,U^\dagger\Lambda^*(|s\rangle\langle s|)U\bigr).
\end{split}
$$

参考无噪声情况, 同理噪声估计器有:

$$
\mathbb E_{U} [\sum_{s, s'} g(s, s')
tr(\rho P_\Lambda(U, s))tr(\rho P_\Lambda(U, s'))]\\
$$

**其中 $g(s, s')$ 是无噪声下估计器 $f(s, s')$ 的变式,
用来保证噪声通道下估计器的无偏性**.
写成 twirling 通道格式:

$$
\begin{split}
expr
&= tr[(\rho \otimes \rho)
\mathbb E_U[U^{\otimes 2}
(\sum_{s, s'} g(s, s')
\Lambda^* (|s\rangle\langle s|)
\otimes \Lambda^*(|s'\rangle \langle s'|))
(U^\dagger)^{\otimes 2}]]\\
&= tr[(\rho \otimes \rho)\tau^{(2)}(\tilde W)]
\end{split}
$$

> 注意取对偶在 P(S|U) 内部.

Where

$$
\begin{split}
&\tilde W = \sum_{s, s'} g(s, s')
\Lambda^*(|s\rangle\langle s|)
\otimes \Lambda^*(|s'\rangle\langle s'|)\\
&\tau^{(2)}[\cdot]
= \mathbb E_U[U^{\otimes 2}(\cdot)(U^\dagger)^{\otimes 2}]
\end{split}
$$

目标依然是 $\tau^{(2)}(\cdot)$ 项对应为 SWAP，
即 $\tau^{(2)}(\tilde W)=S$。

Ref to [twirling_channel](./00_proofs/twirling/twirling_channel.md),

$$
W = \otimes_j \omega_j
= \otimes_j (\sum_{s_j, s_j'}g(s_j, s_j')\Lambda^*(|s_j\rangle\langle s_j|)\otimes \Lambda^*(|s_j'\rangle \langle s_j'|)),
$$

$$
\tau^{(2)}(W) = \otimes_j \tau_j^{(2)}(\omega_j).
$$

Where

$$
\tau^{(2)}_j (\omega_j) = aI + bS_j
$$

Ref to [the_params_solution](./00_proofs/twirling/the_params_solution.md)

变化为:

$$
\omega_j = \sum_{s, s'} g(s_j, s_j')\Lambda^*(|s_j\rangle\langle s_j|) \otimes \Lambda^*(|s_j'\rangle \langle s_j'|)
$$

Ref 中 $(1)$ 的等式依然成立, 和噪声无关,
重点在于 $tr(\omega_j)$ 和 $tr(S_j \omega_j)$.

对于 $tr(\omega_j)$:

$$
\begin{split}
tr(\omega_j) &=\sum_{s_j, s_j'}g(s_j, s_j')
tr(\Lambda^*(|s_j\rangle \langle s_j|))
tr(\Lambda^*(|s_j'\rangle \langle s_j'|)) \\
&= \sum_{s, s'} g(s, s') = 2g(0, 0) + 2g(0, 1) = 2
\end{split} \\
\Rightarrow x_j + y_j = 1 \tag{1}
$$

> 依然使用**对称因子假设**; 其中设$x_j = g(0, 0), y_j = g(0, 1)$

相对于无噪声这没有什么变化. 对于 $tr(S_j\omega_j)$:

$$
tr(S_j\omega_j) = \sum_{s_j, s_j'} g(s_j, s_j')
tr[\Lambda^*(|s_j\rangle \langle s_j|) \Lambda^*(|s_j'\rangle\langle s_j'|)]
$$

令

$$
M = tr[...]
$$

也即上式有:

$$
tr(S_j \omega_j) = x_j (M_{00} + M_{11}) + y_j (M_{01} + M_{10})
= A_jx_j + B_jy_j = 4 \tag{2}
$$

**注意到**:

$$
\sum_{s_j, s_j'} tr[\Lambda^*(|s_j\rangle\langle s_j|)\Lambda^*(|s_j'\rangle\langle s_j'|)]
= tr(\Lambda^*(I)^2) = 2 = A_j + B_j \tag{3}
$$

> 根据**假设4**, 由于 $tr(\Lambda(F)) = tr(F)$, 必然有: $tr(F \Lambda^*(I)) = tr(F)$,
也即 $\Lambda^*(I) = I$.

联立 $(1), (2), (3)$, 可以给出hamming core形式:

$$
\begin{split}
x_j = \frac{2 + A_j}{2A_j - 2} \\
y_j = \frac{A_j - 4}{2A_j - 2} \\
\end{split}
$$

Where:

$$
\begin{split}
&A_j = M_{00} + M_{11}\\
&= tr[\Lambda^*(|0\rangle \langle 0|)\Lambda^*(|0\rangle \langle 0|)]
+ tr[\Lambda^*(|1\rangle \langle 1|)\Lambda^*(|1\rangle \langle 1|)]\\
&B_j = M_{01} + M_{10}
\end{split}
$$

### survival rate estimator

我们需要给出 $A_j$ 或 $B_j$ 的 estimator, 
**这意味着我们需要建立 $A_j$ 和某些统计量关联.**

首先提出**一致率**概念, 一对 shots 在比特位相等的概率是:

$$
\begin{split}
&\sum_{s_j \in \{0, 1\}} P_{\Lambda}(s_j |U_j)^2\\
&= \sum_{s_j} tr(\sigma \Lambda^*(|s_j\rangle \langle s_j|))^2\\
&= tr[(\sigma \otimes \sigma)
\sum_{s_j} (\Lambda^*(|s_j\rangle\langle s_j|
\otimes \Lambda^*(|s_j\rangle \langle s_j|)))]\\
&= tr[\sigma^{\otimes 2} D_j]
\end{split}
$$

Where

$$
D_j = \sum_{s_j} \Lambda^*(|s_j\rangle \langle s_j|)^{\otimes 2}
$$

实际实验时初态取 $|0\rangle$
（即 $\sigma_j=U_j|0\rangle\langle0|U_j^\dagger$），
$s_j$ 仍遍历 $\{0,1\}$；
现在对 $U$ 做平均(**这个是一个可以直接统计的物理量!**), 有:

$$
\begin{split}
E_j^{(=)} &= \mathbb E_{U}[\sum_{s_j} P_{\Lambda}(s_j|U_j)^2] \\
&= \mathbb E_{U}[ tr[\sigma^{\otimes 2}D_j]]\\
&= tr[|00\rangle\langle00| \tau_j^{(2)}(D_j)]
\end{split} \tag{4}
$$

Ref to [the_params_solution](./00_proofs/twirling/the_params_solution.md),
依然有结构:

$$
\tau^{(2)}(D_j) = cI + dS_j \tag{5}
$$

结构固有属性:

$$
\begin{cases}
u_D = 4c + 2d = tr(D_j)\\
t_D = 2c + 4d = tr(S_jD_j)\\
\end{cases}
$$

等式右需要用到**假设6** $\Lambda(I) = I$; 其中:

$$
tr(D_j) = \sum\limits_{s_j} tr^2[\Lambda^*(|s_j\rangle\langle s_j|)]
$$

又有:

$$
tr[\Lambda^*(|s_j\rangle \langle s_j|)]
= tr(\Lambda(I) |s_j\rangle \langle s_j|)
= tr(|s_j\rangle \langle s_j|) = 1
$$

显然有:

$$
tr(D_j) = 2
$$

对于:

$$
tr(S_j D_j) = \sum_{s_j}tr(\Lambda^*(|s_j\rangle\langle s_j|)^2) = A_j
$$

真是注意力惊人. 由此得到

$$
\begin{cases}
4c + 2d = 2\\
2c + 4d = A_j
\end{cases} \Rightarrow
\begin{cases}
c = \frac{4 - A_j}{6}\\
d = \frac{A_j - 1}{3}\\
\end{cases} \tag{6}
$$

将 $(5), (6)$ 代入 $(4)$, 有:

$$
E_j^{(=)} = c + d = \frac{2 + A_j}{6} \rightarrow A_j = 6E_j^{(=)} - 2
$$

其中 $E_j^{(=)}$ 的统计量是:

$$
\hat E_j^{(=)}=\frac{1}{N_U}\sum_r
\frac{1}{N_M(N_M-1)}\sum_{m\ne m'}
\delta_{s_j^{(r,m)},\,s_j^{(r,m')}},\qquad
$$
