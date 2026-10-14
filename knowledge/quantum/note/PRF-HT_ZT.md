# HT ZT

**INTERPRET:**

利用 twirling channel 思想可以构建 ZT 的 hamming distance 结构, 核与 purity 同一套, 差别只在 $I_1$ 上用共轭 twirl 打到部分转置交换子.

## Phase 1

**INTERPRET:**

This phase give the SUFFICES condition.

**ASSUME:**

不妨设 ZT 估计器形式为:

$$
\hat Z_{\mathcal T} = f(s, s') = \prod_{i \in I} f(s_i, s'_i)
$$

$I = I_1 \cup I_2$ 是两次实验共用的 $2n$ 比特区间, $s$ 来自实验 1, $s'$ 来自实验 2.

**GOAL:**

$$
\forall \rho, \quad \mathbb E_{U, s, s'}[\hat Z_{\mathcal T}] = Z_{\mathcal T}
$$

$Z_{\mathcal T}$ 是含 $I_1$ 上部分转置与 $u_{\mathcal T} = \bigotimes_{i \in I_1} \sigma^y_i$ 的时间反演 MBTI.

**GIVEN:**

- 实验 1 在 $I_1$ 上先作用已知的 $u_{\mathcal T}$, 再加随机幺正; 实验 2 直接加随机幺正 $\quad (1)$
- 两次实验在 $I_1$ 上的随机幺正取共轭配对 $U_i \otimes U_i^\ast$, 在 $I_2$ 上取相同配对 $U_i \otimes U_i$, 均为 Haar / Clifford 均匀分布 $\quad (2)$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat Z_{\mathcal T}]
&= \mathbb E_{U} [\sum_{s, s'}\prod_{i \in I} f(s_i, s'_i) P^{(1)}(s|U)P^{(2)}(s'|U)]\\
&= \mathbb E_{U} [\sum_{s, s'}\prod_{i \in I} f(s_i, s'_i) tr(\sigma^{(1)}|s\rangle \langle s|) tr(\sigma^{(2)}|s'\rangle \langle s'|)]\\
\end{split}
$$

**WHERE:**

$$
\sigma^{(1)} = U^{(1)}\tilde\rho (U^{(1)})^\dagger, \quad \sigma^{(2)} = U^{(2)}\rho (U^{(2)})^\dagger
$$

$\tilde\rho$ 是实验 1 中经 $u_{\mathcal T}$ 作用后的态, $\rho$ 是原态.

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat Z_{\mathcal T}] &= tr[(\tilde\rho \otimes \rho) \mathbb E_U[(U^{(1)\dagger} \otimes U^{(2)\dagger})
(\sum_{s, s'} f(s, s') |s\rangle\langle s| \otimes |s'\rangle \langle s'|) (U^{(1)} \otimes U^{(2)})]]\\
\end{split}
$$

**LET:**

$$
\begin{split}
&\tau(\cdot) = \mathbb E_U[(U^{(1)\dagger} \otimes U^{(2)\dagger}) (\cdot) (U^{(1)} \otimes U^{(2)})] \\
&W = \sum_{s, s'} \prod_{i \in I} f(s_i, s'_i) |s\rangle\langle s| \otimes |s'\rangle \langle s'|
\end{split}
$$

$\tau$ 在 $I_1$ 上是 $U \otimes U^\ast$ 型的 isotropic twirl $\Psi$, 在 $I_2$ 上是 $U \otimes U$ 型的 twirl $F$.

**HAVE**:

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat Z_{\mathcal T}] &= tr[(\tilde\rho \otimes \rho)\tau(W)]
\end{split}
$$

**BY:**

[ZT form](PRF-ZT_form.md), $Z_{\mathcal T}$ 已写成 $tr[(\tilde\rho \otimes \rho)(T_{I_1} \otimes S_{I_2})]$, 故只需 twirl 到 $T_{I_1} \otimes S_{I_2}$.

**SUFFICES:**

$$
\tau(W) = \mathbb T_{I_1} \otimes \mathbb S_{I_2}
$$

其中 $\mathbb T_{I_1} = \bigotimes_{i \in I_1} T_i$, $T_i = S_i^{T_2}$ 是交换子的部分转置; $\mathbb S_{I_2} = \bigotimes_{i \in I_2} S_i$.

**HAVE:**

$$
\begin{split}
&W = \bigotimes_{i \in I} w_i = \bigotimes_{i \in I} \sum_{s_i, s'_i} f(s_i, s'_i)|s_i\rangle \langle s_i| \otimes |s'_i\rangle \langle s'_i| \\
\end{split}
$$

**SUFFICES:**

$$
\tau^\Psi_i(w_i) = T_i \quad (i \in I_1), \qquad \tau^F_i(w_i) = S_i \quad (i \in I_2)
$$

**NOTE:**

$I_1$ 与 $I_2$ 的单点 twirl 通道不同, 但 $T_i$ 与 $S_i$ 满足同样的迹数 $tr(T_i) = tr(S_i) = 2$, $tr(T_i^2) = tr(S_i^2) = 4$, 故 Phase 2 的方程两边完全一致.

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
w_i = \sum_{s_i, s'_i}f_i(s_i, s'_i)|s_i\rangle \langle s_i| \otimes |s'_i\rangle \langle s'_i|
$$

**WHERE:**

$$
\begin{cases}
u = tr(w_i)\\
t = tr(S_iw_i) = tr(T_iw_i)
\end{cases}
$$

第二个等号成立是因为 $w_i$ 对角, $tr(T_iw_i) = tr(S_iw_i) = \sum_{s_i} f_i(s_i, s_i)$.

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

我们称之为*对称因子假设*, 这是因为两个自由度足够满足无偏核构造. 这里 $i$ 逐比特取遍 $I_1 \cup I_2$.

**HAVE:**

$$
u = tr(w_i) = 2x_i + 2y_i
$$

and

$$
t = tr(S_iw_i) = tr(T_iw_i) = 2x_i
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
f(s, s') = 2^{2n}(-2)^{-D[s, s']}
$$

where $D[s, s'] = \sum_{i \in I} |s_i - s'_i|$ counts over all $2n$ qubits in $I_1 \cup I_2$.

**QED**
