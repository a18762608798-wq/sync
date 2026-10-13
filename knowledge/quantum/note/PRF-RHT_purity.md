# RHT purity

## Phase 1

**INTERPRET:**

This phase give the SUFFICES condition.

**REQUIRE:**

- (1) 噪声局域: $\Lambda=\otimes_i\Lambda_i$.
- (2) TP: $tr(\Lambda(\rho)) = tr(\rho) \rightarrow \Lambda^{\ast}(I) = I$
- (3) $\Lambda_{l, i}(I) = (1+\delta_{l, i})|0\rangle\langle 0| + (1-\delta_{l, i})|1\rangle\langle 1|,\quad l = 1, 2$

**GOAL:**

$$
\forall \rho, \quad \mathbb E_{U, s, s'}[\hat{\mathcal{P}}] = tr(\rho^2)
$$

with noise $\Lambda$

**WHERE:**

$$
\hat{\mathcal{P}} = g(s, s') = \prod_i g_i(s_i, s'_i)
$$

**GIVEN:**

- $tr(\rho^2) = tr[(\rho \otimes \rho)S] \quad (1)$
- $tr(AB) = tr[(A \otimes B)S] \quad (2)$
- U 是 Haar / Clifford 均匀分布 $(3)$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}]
&= \mathbb E_{U} [\sum_{s, s'}\prod_i g_i(s_i, s'_i) P_{\Lambda_1}(s|U)P_{\Lambda_2}(s'|U)]\\
&= \mathbb E_{U} [\sum_{s, s'}\prod_i g_i(s_i, s'_i) tr(\Lambda_1(\sigma)|s\rangle \langle s|) tr(\Lambda_2(\sigma)|s'\rangle \langle s'|)]\\
&= \mathbb E_{U} [\sum_{s, s'}\prod_i g_i(s_i, s'_i) tr(\sigma\Lambda^{\ast}_{1}(|s\rangle \langle s|)) tr(\sigma\Lambda^{\ast}_{2}(|s'\rangle \langle s'|))]\\
\end{split}
$$

**CONSIDER:**

$$
tr(\sigma\Lambda^{\ast}_{1}(|s\rangle \langle s|)) tr(\sigma\Lambda^{\ast}_{2}(|s'\rangle \langle s'|))
$$

**HAVE:**

$$
\begin{split}
tr(\sigma\Lambda^{\ast}_{1}(|s\rangle \langle s|)) tr(\sigma\Lambda^{\ast}_{2}(|s'\rangle \langle s'|))
&= tr(\rho U^\dagger\Lambda^{\ast}_{1}(|s\rangle\langle s|)U)tr(\rho U^\dagger\Lambda^{\ast}_{2}(|s'\rangle\langle s'|)U)\\
&= tr[\rho^{\otimes 2}(U^\dagger)^{\otimes 2} \Lambda^{\ast}_{1}(|s\rangle\langle s|)\otimes \Lambda^{\ast}_{2}(|s'\rangle \langle s'|) U^{\otimes 2}]
\end{split}
$$

**HAVE:**

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}] &= tr[(\rho \otimes \rho) \mathbb E_U[(U^\dagger)^{\otimes 2}
(\sum_{s, s'} g(s, s') \Lambda^{\ast}_{1}(|s\rangle\langle s|) \otimes \Lambda^{\ast}_{2}(|s'\rangle \langle s'|))U^{\otimes 2}]]\\
\end{split}
$$

**LET:**

$$
\begin{split}
&V = U^\dagger \\
&\tau(\cdot) = \mathbb E_V[V^{\otimes 2} (\cdot) (V^\dagger)^{\otimes 2}] \\
&W' = \sum_{s, s'} \prod_i g_i(s_i, s'_i) \Lambda^{\ast}_{1}(|s\rangle\langle s|) \otimes \Lambda^{\ast}_{2}(|s'\rangle \langle s'|)
\end{split}
$$

**NOTE:**

这里$\tau(\cdot)$的形式是否可以使用，取决于$U^\dagger$是否依然属于U原本的分布（同 [HT purity](PRF-HT_purity.md)，逆不变已证).

**HAVE**:

$$
\begin{split}
\mathbb E_{U, s, s'}[\hat{\mathcal{P}}] &= tr[(\rho \otimes \rho)\tau(W')]
\end{split}
$$

**SUFFICES:**

$$
\tau(W') = S
$$

**HAVE:**

$$
\begin{split}
&\Pi W'\Pi^\dagger = \bigotimes_i w_i = \bigotimes_i \sum_{s_i, s_i'} g_i(s_i, s_i') \Lambda^{\ast}_{1, i}(|s_i\rangle \langle s_i|)\otimes \Lambda^{\ast}_{2, i}(|s_i'\rangle \langle s_i'|) \\
&\Pi S\Pi^\dagger = \bigotimes_i S_i
\end{split}
$$

**WHERE:**

$\Pi$ 交换空间顺序, 从 $(\bigotimes_i H_i) \otimes (\bigotimes H_i') \rightarrow \bigotimes_i (H_i \otimes H_i')$

**SUFFICES:**

$$
\tau_i(w_i) = S_i
$$

## Phase 2

**GIVEN:**

$$
\begin{cases}
u = 2\\
t = 4
\end{cases} \tag{4}
$$

and

$$
w_i = \sum_{s_i, s_i'}g_i(s_i, s_i')\Lambda^{\ast}_{1, i}(|s_i\rangle \langle s_i|) \otimes \Lambda^{\ast}_{2, i}(|s_i'\rangle \langle s_i'|)
$$

**WHERE:**

$$
\begin{cases}
u = tr(w_i)\\
t = tr(S_iw_i)
\end{cases}
$$

**BY:**

[Hamming core](PRF-Hamming_core.md)

**ASSUME:**

$$
\begin{cases}
x_i = g_i(0, 0) = g_i(1, 1)\\
y_i = g_i(0, 1) = g_i(1, 0)\\
\end{cases}
$$

**INTERPRET:**

我们称之为*对称因子假设*, 这是因为两个自由度足够满足无偏核构造.

**HAVE:**

$$
\begin{split}
u &= tr(w_i) \\
&= \sum_{s_i, s_i'}g_i(s_i, s_i')tr(\Lambda^{\ast}_{1, i}(|s_i\rangle \langle s_i|))tr(\Lambda^{\ast}_{2, i}(|s_i'\rangle \langle s_i'|))\\
&= \sum_{s_i, s_i'}g_i(s_i, s_i')tr(\Lambda_{1, i}(I)|s_i\rangle \langle s_i|)tr(\Lambda_{2, i}(I)|s_i'\rangle \langle s_i'|) \\
\end{split}
$$

**CONSIDER:**

$$
tr(\Lambda_{1, i}(I)|s_i\rangle \langle s_i|)
$$

**HAVE:**

$$
\begin{split}
tr(\Lambda_{1, i}(I)|s_i\rangle \langle s_i|) &= (1+\delta_{1, i})tr(|0\rangle\langle 0|s_i\rangle\langle s_i|) + (1-\delta_{1, i})tr(|1\rangle\langle 1|s_i\rangle \langle s_i|) \\
&= \begin{cases}
1 + \delta_{1, i} \quad s_i = 0\\
1 - \delta_{1, i} \quad s_i = 1
\end{cases}
\end{split}
$$

**HAVE:**

$$
\begin{split}
u &= g_i(0, 0)(1 + \delta_{1, i})(1 + \delta_{2, i}) + g_i(1, 1)(1 - \delta_{1, i})(1 - \delta_{2, i})\\
&+ g_i(0, 1)(1 + \delta_{1, i})(1 - \delta_{2, i}) + g_i(1, 0)(1 - \delta_{1, i})(1 + \delta_{2, i})\\
&= 2(1 + \delta_{1, i}\delta_{2, i})x_i + 2(1 - \delta_{1, i}\delta_{2, i})y_i
\end{split} \tag{5}
$$

**HAVE:**

$$
\begin{split}
t &= tr(S_iw_i) \\
&=\sum_{s_i, s_i'}g_i(s_i, s_i')tr(S_i(\Lambda^{\ast}_{1, i}(|s_i\rangle \langle s_i|) \otimes \Lambda^{\ast}_{2, i}(|s_i'\rangle \langle s_i'|))) \\
&=\sum_{s_i, s_i'}g_i(s_i, s_i')tr(\Lambda^{\ast}_{1, i}(|s_i\rangle \langle s_i|)\Lambda^{\ast}_{2, i}(|s_i'\rangle \langle s_i'|))
\end{split}
$$

**LET:**

$$
\begin{cases}
M_{s_i, s'_i} = tr(\Lambda^{\ast}_{1, i}(|s_i\rangle \langle s_i|)\Lambda^{\ast}_{2, i}(|s_i'\rangle \langle s_i'|))\\
A_i = M_{00} + M_{11} \\
B_i = M_{01} + M_{10}
\end{cases} \tag{6}
$$

**HAVE:**

$$
t = A_ix_i + B_iy_i \tag{7}
$$

**HAVE:**

$$
\begin{split}
A_i + B_i &= \sum_{s_i, s_i'}M_{s_i, s_i'}\\
&= tr(\Lambda^{\ast}_{1, i}(\sum_{s_i}|s_i\rangle\langle s_i|)\Lambda^{\ast}_{2, i}(\sum_{s_i'}|s_i'\rangle\langle s_i'|))\\
&= tr(\Lambda^{\ast}_{1, i}(I)\Lambda^{\ast}_{2, i}(I))\\
& = tr(I) = 2
\end{split} \tag{8}
$$

**BY:**

(4), (5), (6), (7), (8)

**THEREFORE:**

$$
\begin{split}
&x_i = \frac{p_i + q_i}{2}\\
&y_i = \frac{p_i - q_i}{2}
\end{split} \tag{9}
$$

**WHERE:**

$$
\begin{cases}
p_i = 1 - \varepsilon_i q_i \\
q_i = \frac{3}{A_i - 1 - \varepsilon_i}
\end{cases} \tag{10}
$$

where

$$
\begin{split}
&\varepsilon_i = \delta_{1, i}\delta_{2, i}\\
&A_i = tr(\Lambda^{\ast}_{1, i}(|0\rangle \langle 0|)\Lambda^{\ast}_{2, i}(|0\rangle \langle 0|)) + tr(\Lambda^{\ast}_{1, i}(|1\rangle \langle 1|)\Lambda^{\ast}_{2, i}(|1\rangle \langle 1|))
\end{split} \tag{11}
$$

## Phase 3

**INTERPRET:**

这个阶段给出用于标定 $A_i$ 和 $\varepsilon_i$ 对应的估计量.

**DEFINE:**

定义所谓**一致率**(这个和shadow的$C_j$很类似):

$$
R_i = \mathbb E_{U_i}[\sum_{s_i} P_{\Lambda_{1, i}}(s_i|U_i) P_{\Lambda_{2, i}}(s_i|U_i)]
$$

**HAVE:**

$$
\begin{split}
R_i &= \mathbb E_{U_i}[\sum_{s_i} tr(\sigma_i \Lambda^{\ast}_{1, i}(|s_i\rangle\langle s_i|)) tr(\sigma_i \Lambda^{\ast}_{2, i}(|s_i\rangle\langle s_i|))]\\
&= \mathbb E_{U_i} [tr[\sigma_i^{\otimes 2}D_i]]\\
&= tr[\rho_i^{\otimes 2}\tau_i(D_i)]
\end{split}
$$

**NOTE:**

这里依然需要 $U^\dagger$ 依然在U分布内. $\rho_i$ 作为**校准电路**一般取 $|0\rangle$.

**WHERE:**

$$
D_i = \sum_{s_i} \Lambda^{\ast}_{1, i}(|s_i\rangle\langle s_i|) \otimes \Lambda^{\ast}_{2, i}(|s_i\rangle\langle s_i|)
$$

**ASSUME:**

$$
\tau_i(D_i) = \alpha_i I + \beta_i S_i
$$

**HAVE:**

$$
R_i = tr[\rho_i^{\otimes 2}(\alpha_i I + \beta_i S_i)] = \alpha_i + \beta_i \tag{12}
$$

**BY:**

[PRF-Hamming_core](./PRF-Hamming_core.md)

**HAVE:**

$$
\begin{split}
&tr(D_i) = tr(\tau_i(D_i)) = 4\alpha_i + 2\beta_i \\
&tr(S_iD_i) = tr(S_i\tau_i(D_i)) = 2\alpha_i + 4\beta_i \\
\end{split} \tag{13}
$$

$$
\begin{split}
tr(D_i) &= \sum_{s_i} tr(\Lambda^{\ast}_{1, i}(|s_i\rangle\langle s_i|))tr(\Lambda^{\ast}_{2, i}(|s_i\rangle\langle s_i|))\\
&= \sum_{s_i} [(1+\delta_{1, i})tr(|0\rangle\langle 0|s_i\rangle\langle s_i|) + (1-\delta_{1, i})tr(|1\rangle\langle 1|s_i\rangle\langle s_i|)] \times\\
&[(1+\delta_{2, i})tr(|0\rangle\langle 0|s_i\rangle\langle s_i|) + (1-\delta_{2, i})tr(|1\rangle\langle 1|s_i\rangle\langle s_i|)]\\
&=(1 + \delta_{1, i})(1 + \delta_{2, i}) + (1 - \delta_{1, i})(1 - \delta_{2, i})\\
&= 2(1 + \varepsilon_i)
\end{split} \tag{14}
$$

and

$$
\begin{split}
tr(S_iD_i) &= \sum_{s_i}tr[\Lambda^{\ast}_{1, i}(|s_i\rangle\langle s_i|)\Lambda^{\ast}_{2, i}(|s_i\rangle\langle s_i|)] \\
&= A_i
\end{split} \tag{15}
$$

**BY:**

(12), (13), (14), (15).

**THEREFORE:**

$$
A_i = 6R_i - 2 - 2\varepsilon_i \tag{16}
$$

**INTERPRET:**

现在需要给出 $\varepsilon_i$ 的估计量.

**HAVE:**

$$
\begin{split}
f_{0, l, i} = \mathbb E_{U_i}[P_{\Lambda_{l, i}}(0|U_i)] &= tr(\mathbb E_{U_i}[\sigma_i]\Lambda^{\ast}_{l, i}(|0\rangle \langle 0|))\\
&= \frac{1}{2}tr[\Lambda^{\ast}_{l, i}(|0\rangle\langle 0|)]\\
&= \frac{1 + \delta_{l, i}}{2} \tag{17}
\end{split}
$$

Similarly,

$$
f_{1, l, i} = \mathbb E_{U_i}[P_{\Lambda_{l, i}}(1|U_i)] = \frac{1 - \delta_{l, i}}{2}
$$

**THEREFORE:**

$$
\delta_{l, i} = f_{0, l, i} - f_{1, l, i} = 2f_{0, l, i} - 1 \tag{18}
$$

## SUMMARY

**BY:**

(9, 10, 11, 12, 16, 17, 18)

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
&R_i = \mathbb E_{U_i}[\sum_{s_i} P_{\Lambda_{1, i}}(s_i|U_i) P_{\Lambda_{2, i}}(s_i|U_i)]\\
&\delta_{l, i} = f_{0, l, i} - f_{1, l, i} = 2f_{0, l, i} - 1
\end{split}
$$
