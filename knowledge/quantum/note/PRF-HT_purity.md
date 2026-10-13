# HT purity

**INTERPRET:**

利用 twirling channel 思想可以构建 hamming distance 结构.

## Phase 1

**INTERPRET:**

This phase give the SUFFICES condition.

**ASSUME:**

不妨设hamming 估计器形式为:

$$
\hat{\mathcal{P}} = f(s, s') = \prod_i f(s_i, s'_i)
$$

**GOAL:**

$$
\forall \rho, \quad \mathbb E_{U, s, s'}[\hat{\mathcal{P}}] = tr(\rho^2)
$$

**GIVEN:**

- $tr(\rho^2) = tr[(\rho \otimes \rho)S] \quad (1)$
- U 是 Haar / Clifford 均匀分布 $(2)$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}]
&= \mathbb E_{U} [\sum_{s, s'}\prod_i f(s_i, s_i') P(s|U)P(s'|U)]\\
&= \mathbb E_{U} [\sum_{s, s'}\prod_i f(s_i, s_i') tr(\sigma|s\rangle \langle s|) tr(\sigma |s'\rangle \langle s'|)]\\
\end{split}
$$

**WHERE:**

$$
\sigma = U\rho U^\dagger
$$

**CONSIDER:**

$$
tr(\sigma|s\rangle \langle s|) tr(\sigma |s'\rangle \langle s'|)
$$

**HAVE:**

$$
\begin{split}
tr(\sigma|s\rangle \langle s|) tr(\sigma |s'\rangle \langle s'|) &= tr(\rho U^\dagger|s\rangle\langle s|U)tr(\rho U^\dagger|s'\rangle\langle s'|U)\\
&= tr[\rho^{\otimes 2}(U^\dagger)^{\otimes 2} |s\rangle\langle s|\otimes |s'\rangle \langle s'| U^{\otimes 2}]
\end{split}
$$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}] &= tr[(\rho \otimes \rho) \mathbb E_U[(U^\dagger)^{\otimes 2}
(\sum_{s, s'} f(s, s') |s\rangle\langle s| \otimes |s'\rangle \langle s'|)U^{\otimes 2}]]\\
\end{split}
$$

**LET:**

$$
\begin{split}
&V = U^\dagger \\
&\tau(\cdot) = \mathbb E_V[V^{\otimes 2} (\cdot) (V^\dagger)^{\otimes 2}] \\
&W = \sum_{s, s'} \prod_i f(s_i, s'_i) |s\rangle\langle s| \otimes |s'\rangle \langle s'|
\end{split}
$$

**NOTE:**

这里$\tau(\cdot)$的形式是否可以使用依赖于$U^\dagger$依然属于U原本的分布.

**HAVE**:

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}] &= tr[(\rho \otimes \rho)\tau(W)] \tag{3}
\end{split}
$$

**SUFFICES:**

$\forall \rho$, (1) $\land$ (3) is true, therefore:

$$
\tau(W) = S, \tag{4}
$$

**HAVE:**

$$
\begin{split}
&PWP^\dagger = \bigotimes_i w_i = \bigotimes_i \sum_{s_i, s_i'} f(s_i, s_i)|s\rangle \langle s|\otimes |s'\rangle \langle s'| \\
&PSP^\dagger = \bigotimes_i S_i \tag{5}
\end{split}
$$

**WHERE:**

$P$ 交换空间顺序, 从 $(\bigotimes_i H_i) \otimes (\bigotimes H_i') \rightarrow \bigotimes_i (H_i \otimes H_i')$

**SUFFICES:**

According to (4), (5),

$$
\tau_i(w_i) = S_i \tag{6}
$$

## Phase 2

**GIVEN:**

$$
\begin{cases}
u = 2\\
t = 4
\end{cases}
$$

and

$$
w_i = \sum_{s_i, s_i'}f_i(s_i, s_i')|s_i\rangle \langle s_i| \otimes |s_i'\rangle \langle s_i'|
$$

**WHERE:**

$$
\begin{cases}
u = tr(w_i)\\
t = tr(Sw_i)
\end{cases}
$$

**BY:**

[Hamming core](PRF-Hamming_core.md)

**ASSUME:**

$$
\begin{cases}
x_i = f_i(0, 0) = f_i(1, 1)\\
y_i = f_i(0, 1) = f_i(1, 0)\\
\end{cases}
$$

**INTERPRET:**

我们称之为*对称因子假设*, 这是因为两个自由度足够满足无偏核构造.

**HAVE:**

$$
u = tr(w_i) = 2x_i + 2y_i
$$

and

$$
t = tr(Sw_i) = 2x_i
$$

**THEREFORE:**

$$
\begin{cases}
x_i = 2\\
y_i = -1\\
\end{cases}
$$

also, we could coding the result:

$$
f(s, s') = 2*(-2)^{-D[s, s']}
$$

**QED**
