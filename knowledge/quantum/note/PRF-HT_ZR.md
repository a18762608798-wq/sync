# HT ZR

**INTERPRET:**

利用 twirling channel 思想可以构建 ZR 的 hamming distance 结构, 与 purity 同一套核, 只是 $i$ 读成镜像对.

## Phase 1

**INTERPRET:**

This phase give the SUFFICES condition.

**ASSUME:**

不妨设 ZR 估计器形式为:

$$
\hat Z_{\mathcal R} = f(s) = \prod_{i=1}^n f(s_i, s_{\bar i})
$$

$i$ is the subscript of mirror pair, $\bar i$ is its reflection counterpart, $n$ is the number of pairs.

**GOAL:**

$$
\forall \rho, \quad \mathbb E_{U, s}[\hat Z_{\mathcal R}] = tr(\rho \mathcal R)
$$

**WHERE:**

$$
\mathcal R = \bigotimes_{i=1}^n S_{i, \bar i}
$$

**GIVEN:**

- $tr(\rho \mathcal R) = Z_{\mathcal R} \quad (1)$
- $U_{\mathcal R} = \bigotimes_{i=1}^n (U_i \otimes U_i)$ 是反射对称的 Haar / Clifford 均匀分布, 每对共用同一个 $U_i \quad (2)$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s}[\hat Z_{\mathcal R}]
&= \mathbb E_{U} [\sum_{s}\prod_{i=1}^n f(s_i, s_{\bar i}) P(s|U)]\\
&= \mathbb E_{U} [\sum_{s}\prod_{i=1}^n f(s_i, s_{\bar i}) tr(\sigma|s\rangle \langle s|)]\\
\end{split}
$$

**WHERE:**

$$
\sigma = U_{\mathcal R}\rho U_{\mathcal R}^\dagger
$$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s}[\hat Z_{\mathcal R}] &= tr[(\rho) \mathbb E_U[(U_{\mathcal R}^\dagger)
(\sum_{s} f(s) |s\rangle\langle s|)U_{\mathcal R}]]\\
\end{split}
$$

**LET:**

$$
\begin{split}
&V = U_{\mathcal R}^\dagger \\
&\tau(\cdot) = \mathbb E_V[V (\cdot) V^\dagger] \\
&O_{\mathcal R} = \sum_{s} \prod_{i=1}^n f(s_i, s_{\bar i}) |s\rangle\langle s|
\end{split}
$$

**HAVE**:

$$
\begin{split}
\mathbb E_{U, s}[\hat Z_{\mathcal R}] &= tr[\rho\tau(O_{\mathcal R})]
\end{split}
$$

**SUFFICES:**

$$
\tau(O_{\mathcal R}) = \mathcal R
$$

**HAVE:**

$$
\begin{split}
&O_{\mathcal R} = \bigotimes_{i=1}^n o_i = \bigotimes_{i=1}^n \sum_{s_i, s_{\bar i}} f(s_i, s_{\bar i})|s_i\rangle \langle s_i| \otimes |s_{\bar i}\rangle \langle s_{\bar i}| \\
&\mathcal R = \bigotimes_{i=1}^n S_{i, \bar i}
\end{split}
$$

**NOTE:**

这里希尔伯特空间顺序已按 mirror pair 定义为 $\bigotimes_{i=1}^n (H_i \otimes H_{\bar i})$,
因此 $o_i$ 与 $\mathcal R$ 直接写成局域直积即可, 不需要 purity 情形里那样的空间交换算符 $P$.

**SUFFICES:**

$$
\tau_i(o_i) = S_{i, \bar i}
$$

where $\tau_i(\cdot) = \mathbb E_{U_i}[(U_i \otimes U_i)^\dagger (\cdot) (U_i \otimes U_i)]$.

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
o_i = \sum_{s_i, s_{\bar i}}f_i(s_i, s_{\bar i})|s_i\rangle \langle s_i| \otimes |s_{\bar i}\rangle \langle s_{\bar i}|
$$

**WHERE:**

$$
\begin{cases}
u = tr(o_i)\\
t = tr(S_{i, \bar i}o_i)
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

我们称之为*对称因子假设*, 这是因为两个自由度足够满足无偏核构造. 这里 $i$ 是对标号, 不是比特标号.

**HAVE:**

$$
u = tr(o_i) = 2x_i + 2y_i
$$

and

$$
t = tr(S_{i, \bar i}o_i) = 2x_i
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
f(s) = 2^n(-2)^{-D[s, \mathcal R(s)]}
$$

where $D[s, \mathcal R(s)] = \sum_{i=1}^n |s_i - s_{\bar i}|$ counts over pairs.

**QED**
