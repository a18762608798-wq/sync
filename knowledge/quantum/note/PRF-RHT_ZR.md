# RHT ZR

## Phase 1

**INTERPRET:**

This phase give the SUFFICES condition.

**REQUIRE:**

- (1) 噪声局域: $\Lambda=\otimes_i\Lambda_i$.
- (2) TP: $tr(\Lambda(\rho)) = tr(\rho) \rightarrow \Lambda^*(I) = I$
- (3) $\Lambda_{i}(I) = (1+\delta_{i})|0\rangle\langle 0| + (1-\delta_{i})|1\rangle\langle 1|$

**GOAL:**

$$
\forall \rho, \quad \mathbb E_{U, s}[\hat Z_{\mathcal R}] = tr(\rho \mathcal R)
$$

with noise $\Lambda$

**WHERE:**

$$
\hat Z_{\mathcal R} = g(s) = \prod_i g(s_i, s_{\bar i})
$$

**GIVEN:**

- $tr(\rho \mathcal R) = Z_{\mathcal R} \quad (1)$
- $U_{\mathcal R} = \bigotimes_i (U_i \otimes U_i)$ 是反射对称的 Haar / Clifford 均匀分布, 每对共用同一个 $U_i \quad (2)$
- 噪声在随机 U 之后测量之前, 每个位点独立作用 $\Lambda_{i}$.

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s}[\hat Z_{\mathcal R}]
&= \mathbb E_{U} [\sum_{s}\prod_i g(s_i, s_{\bar i}) P_{\Lambda_{i}}(s_i|U)P_{\Lambda_{\bar i}}(s_{\bar i}|U)]\\
&= \mathbb E_{U} [\sum_{s}\prod_i g(s_i, s_{\bar i}) tr(\sigma\Lambda^{\ast}_{i}(|s_i\rangle \langle s_i|)) tr(\sigma\Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle \langle s_{\bar i}|))]\\
\end{split}
$$

**CONSIDER:**

$$
tr(\sigma\Lambda^{\ast}_{i}(|s_i\rangle \langle s_i|)) tr(\sigma\Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle \langle s_{\bar i}|))
$$

**HAVE:**

$$
\begin{split}
&tr(\sigma\Lambda^{\ast}_{i}(|s_i\rangle \langle s_i|)) tr(\sigma\Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle \langle s_{\bar i}|))\\
&= tr[\rho U_{\mathcal R}^\dagger(\Lambda^{\ast}_{i}(|s_i\rangle\langle s_i|)\otimes \Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle\langle s_{\bar i}|))U_{\mathcal R}]
\end{split}
$$

**HAVE:**

$$
\mathbb E_{U, s}[\hat Z_{\mathcal R}] = tr[\rho \mathbb E_U[(U_{\mathcal R}^\dagger)
(\sum_{s} g(s) \Lambda^{\ast}_{i}(|s_i\rangle\langle s_i|) \otimes \Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle\langle s_{\bar i}|))U_{\mathcal R}]]
$$

**LET:**

$$
\begin{split}
&V = U_{\mathcal R}^\dagger \\
&\tau(\cdot) = \mathbb E_V[V (\cdot) V^\dagger] \\
&O = \sum_{s} \prod_i g(s_i, s_{\bar i}) \Lambda^{\ast}_{i}(|s_i\rangle\langle s_i|) \otimes \Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle\langle s_{\bar i}|)
\end{split}
$$

**NOTE:**

这里$\tau(\cdot)$的形式是否可以使用依赖于$U^\dagger$依然属于U原本的分布.

**HAVE**:

$$
\mathbb E_{U, s}[\hat Z_{\mathcal R}] = tr[\rho \tau(O)]
$$

**SUFFICES:**

$$
\tau(O) = \mathcal R
$$

**HAVE:**

$$
\begin{split}
&O = \bigotimes_i w_i = \bigotimes_i \sum_{s_i, s_{\bar i}} g_i(s_i, s_{\bar i}) \Lambda^{\ast}_{i}(|s_i\rangle \langle s_i|)\otimes \Lambda^{\ast}_{\bar i}(|s_{\bar i}\rangle \langle s_{\bar i}|) \\
&\mathcal R = \bigotimes_i S_{i, \bar i}
\end{split}
$$

**NOTE:**

这里希尔伯特空间顺序已按 mirror pair 定义为 $\bigotimes_i (H_i \otimes H_{\bar i})$, 不需要 purity 情形里那样的空间交换算符 $P$.

**SUFFICES:**

$$
\tau_i(w_i) = S_{i, \bar i}
$$

## CONCLUSION

**BY:**

[PRF-RHT_purity](PRF-RHT_purity.md), Phase 2, 3 的证明完全一致, 只需把 $i$ 读成对标号, $\Lambda_{1, i}, \Lambda_{2, i}$ 换成一发内的 $\Lambda_{i}, \Lambda_{\bar i}$, $S_i$ 换成 $S_{i, \bar i}$.

**HAVE:**

$$
\begin{split}
&x_i = \frac{p_i + q_i}{2}\\
&y_i = \frac{p_i - q_i}{2}
\end{split}
$$

where:

$$
\begin{split}
&p_i = 1 - \varepsilon_i q_i \\
&q_i = \frac{3}{A_i - 1 - \varepsilon_i}
\end{split}
$$

and

$$
\begin{split}
&\varepsilon_i = \delta_{i}\delta_{\bar i}\\
&A_i = 6R_i - 2 - 2\varepsilon_i
\end{split}
$$

**WHERE:**

$$
\begin{split}
&R_i = \mathbb E_{U_i}[\sum_{s_i} P_{\Lambda_{i}}(s_i|U_i) P_{\Lambda_{\bar i}}(s_{\bar i}|U_i)]\\
&\delta_{i} = 2f_{0, i} - 1, \quad \delta_{\bar i} = 2f_{0, \bar i} - 1
\end{split}
$$

**NOTE:**

这里 $i$ 是对标号, $f_{0,i}$ 与 $f_{0,\bar i}$ 分别是左右两点各自的单点计数.
