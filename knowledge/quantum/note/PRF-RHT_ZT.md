# RHT ZT

## Phase 1

**INTERPRET:**

This phase give the SUFFICES condition.

**REQUIRE:**

- (1) 噪声局域: $\Lambda=\otimes_i\Lambda_i$.
- (2) TP: $tr(\Lambda(\rho)) = tr(\rho) \rightarrow \Lambda^*(I) = I$
- (3) $\Lambda_{k, i}(I) = (1+\delta_{k, i})|0\rangle\langle 0| + (1-\delta_{k, i})|1\rangle\langle 1|, \quad k = 1, 2$

$k = 1, 2$ 标记两次顺序实验, $i$ 逐比特取遍 $I = I_1 \cup I_2$.

**GOAL:**

$$
\forall \rho, \quad \mathbb E_{U, s, s'}[\hat Z_{\mathcal T}] = Z_{\mathcal T}
$$

with noise $\Lambda$

**WHERE:**

$$
\hat Z_{\mathcal T} = g(s, s') = \prod_{i \in I} g(s_i, s'_i)
$$

**GIVEN:**

- $Z_{\mathcal T} = tr[(\tilde\rho \otimes \rho)(T_{I_1} \otimes S_{I_2})] \quad (1)$
- 实验 1 在 $I_1$ 上先作用已知的 $u_{\mathcal T}$, 再加随机幺正; 实验 2 直接加随机幺正 $\quad (2)$
- 两次实验在 $I_1$ 上的随机幺正取共轭配对 $U_i \otimes U_i^\ast$, 在 $I_2$ 上取相同配对 $U_i \otimes U_i$, 均为 Haar / Clifford 均匀分布 $\quad (3)$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat Z_{\mathcal T}]
&= \mathbb E_{U} [\sum_{s, s'}\prod_{i \in I} g(s_i, s'_i) P_{\Lambda_1}(s|U)P_{\Lambda_2}(s'|U)]\\
&= \mathbb E_{U} [\sum_{s, s'}\prod_{i \in I} g(s_i, s'_i) tr(\tilde\rho U^{(1)\dagger}\Lambda^*_1(|s\rangle\langle s|)U^{(1)}) tr(\rho U^{(2)\dagger}\Lambda^*_2(|s'\rangle\langle s'|)U^{(2)})]\\
\end{split}
$$

$u_{\mathcal T}$ 已吸进 $\tilde\rho$, $U^{(1)}, U^{(2)}$ 是关联实验的两组 U.

**LET:**

$$
\begin{split}
&\tau(\cdot) = \mathbb E_U[(U^{(1)\dagger} \otimes U^{(2)\dagger}) (\cdot) (U^{(1)} \otimes U^{(2)})] \\
&W' = \sum_{s, s'} \prod_{i \in I} g(s_i, s'_i) \Lambda^*_1(|s\rangle\langle s|) \otimes \Lambda^*_2(|s'\rangle\langle s'|)
\end{split}
$$

$\tau$ 在 $I_1$ 上是 $\Psi$ 型, 在 $I_2$ 上是 $F$ 型.

**HAVE**:

$$
\mathbb E_{U, s, s'}[\hat Z_{\mathcal T}] = tr[(\tilde\rho \otimes \rho)\tau(W')]
$$

**SUFFICES:**

$$
\tau(W') = T_{I_1} \otimes S_{I_2}
$$

**HAVE:**

$$
W' = \bigotimes_{i \in I} w_i = \bigotimes_{i \in I} \sum_{s_i, s'_i} g_i(s_i, s'_i) \Lambda^*_{1, i}(|s_i\rangle \langle s_i|)\otimes \Lambda^*_{2, i}(|s'_i\rangle \langle s'_i|)
$$

**SUFFICES:**

$$
\tau^\Psi_i(w_i) = T_i \quad (i \in I_1), \qquad \tau^F_i(w_i) = S_i \quad (i \in I_2)
$$

**WHERE:**

$$
\tau^\Psi_i(\cdot) = \mathbb E_{U_i}[(U_i^\dagger \otimes U_i^T)(\cdot)(U_i \otimes U_i^\ast)], \quad
\tau^F_i(\cdot) = \mathbb E_{U_i}[(U_i^\dagger \otimes U_i^\dagger)(\cdot)(U_i \otimes U_i)]
$$

## CONCLUSION

**BY:**

[PRF-RHT_purity](PRF-RHT_purity.md),

**INTERPRET:**

Phase 2, 3 的证明完全一致, 只需把 $i$ 读成 $I_1 \cup I_2$ 上的逐比特标号, $\Lambda_{1, i}, \Lambda_{2, i}$ 读成两次实验在该比特的噪声通道.

$I_1$ 上第二个方程用 $t' = tr(T_iw_i)$, 其中 $T_i$ 使第二个通道带转置: $M_{s_i, s'_i} = tr(\Lambda^*_{1, i}(|s_i\rangle\langle s_i|)(\Lambda^*_{2, i}(|s'_i\rangle\langle s'_i|))^T)$, 但 $I^T = I$ 故 $A_i + B_i = 2$ 仍成立;

Phase 3 在 $I_1$ 上同样按共轭配对采样标定 $R_i$, twirl 到 $T_i$, 测出的恰好就是这个带转置的 $A_i$. 因此两边转置抵消, $A_i = 6R_i - 2 - 2\varepsilon_i$ 与 $x_i, y_i$ 公式完全不变.

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
&\varepsilon_i = \delta_{1, i}\delta_{2, i}\\
&A_i = 6R_i - 2 - 2\varepsilon_i
\end{split}
$$

**WHERE:**

$$
\begin{split}
&R_i = \mathbb E_{U_i}[\sum_{s_i} P_{\Lambda_{1, i}}(s_i|U_i) P_{\Lambda_{2, i}}(s'_i|U_i)]\\
&\delta_{1, i} = 2f_{0, i}^{(1)} - 1, \quad \delta_{2, i} = 2f_{0, i}^{(2)} - 1
\end{split}
$$

$f_{0, i}^{(1)}, f_{0, i}^{(2)}$ 分别是两次实验在该比特的单点计数.
