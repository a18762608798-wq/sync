# hamming noiseless

利用 twirling channel 思想可以构建 hamming distance 结构.

不妨设hamming 估计器形式为:

$$
\hat{\mathcal{P}} = f(s, s') = \prod_i f(s_i, s'_i)
$$

需要证明:

$$
\mathbb E_{U, s, s'} [\hat{\mathcal{P}}] = tr(\rho^2) = tr[(\rho \otimes \rho)SWAP]
$$

这里我们把random U 放置在 $\rho$ 上, 显然有:

$$
\begin{split}
&\mathbb E_{U} [\sum_{s, s'} f(s, s') P(s|U)P(s'|U)]\\
&=\mathbb E_{U} [\sum_{s, s'} f(s, s') tr(\rho P(U, s))tr(\rho P(U, s'))]\\
&=\mathbb E_{U} [\sum_{s, s'} f(s, s')  tr[(\sigma \otimes \sigma)(|s\rangle \langle s| \otimes |s'\rangle \langle s'|)]]\\
\end{split} \tag{2}
$$

其中

$$
\sigma \otimes \sigma = (U^\dagger \rho U) \otimes (U^\dagger \rho U) = (U^\dagger)^{\otimes 2} \rho^{\otimes 2} U^{\otimes 2}
$$

所以 $tr[\cdot]$ 自然有:

$$
tr[\cdot] = tr[\rho^{\otimes 2} U^{\otimes 2}(|s\rangle \langle s| \otimes |s'\rangle \langle s'| (U^\dagger)^{\otimes 2}]
$$

所以 $(2)$ 也即:

$$
\begin{split}
expr
&= tr[(\rho \otimes \rho)
\mathbb E_U[U^{\otimes 2}
(\sum_{s, s'} f(s, s') |s\rangle\langle s| \otimes |s'\rangle \langle s'|)
(U^\dagger)^{\otimes 2}]]\\
&= tr[(\rho \otimes \rho)\tau^{(2)}(W)]
\end{split}
$$

Where

$$
\begin{split}
&W = \sum_{s, s'} f(s, s') |s\rangle\langle s| \otimes |s'\rangle \langle s'|\\
&\tau^{(2)}[\cdot] = \mathbb E_U[U^{\otimes 2} (\cdot) (U^\dagger)^{\otimes 2}]
\end{split}
$$

Ref to [twirling_channel](./twirling_channel.md),

$$
W = \otimes_j \omega_j
= \otimes_j (\sum_{s_j, s_j'}f(s_j, s_j')|s_j\rangle\langle s_j| \otimes |s_j'\rangle \langle s_j'|),
$$

$$
\tau^{(2)}(W) = \otimes_j \tau_j^{(2)}(\omega_j).
$$

Where

$$
\tau^{(2)}_j (\omega_j) = aI + bS_j
$$

Ref to [the_params_solution](./the_params_solution.md),

$$
\begin{split}
u &= tr(\omega_j) = \sum\limits_{s_j, s_j' \in \{0, 1\}} f(s_j, s_j') = 2\\
t &= tr(S_j \omega_j) = f(0, 0) + f(1, 1) = 4
\end{split}
$$

四个变量, 只有两个约束, 不妨设(**后称之为对称性因子化假设**):

$$
\begin{cases}
f(0, 0) = f(1, 1) = 2\\
f(0, 1) = f(1, 0) = -1
\end{cases}
$$

或者编码为:

$$
2 * (-2)^{-D[s_j, s_j']}
$$

