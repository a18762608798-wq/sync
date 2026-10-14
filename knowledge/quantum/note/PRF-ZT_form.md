# ZT form

**INTERPRET:**

证明时间反演不变量的原始形式等价于 $(\tilde\rho \otimes \rho)$ 在 $T_{I_1} \otimes S_{I_2}$ 上的迹.

**GIVEN:**

$$
Z_{\mathcal T} = tr(\rho u_{\mathcal T} \rho^{T_1} u_{\mathcal T}^\dagger) \tag{1}
$$

$T_1$ 是 $I_1$ 上的部分转置, $u_{\mathcal T} = \bigotimes_{i \in I_1} \sigma^y_i$, $\rho$ 是 $I = I_1 \cup I_2$ 上的态.

**LET:**

$$
\tilde\rho = u_{\mathcal T}^\dagger \rho u_{\mathcal T}, \quad T_i = S_i^{T_2} = \sum_{s, s'} |s, s\rangle\langle s', s'|
$$

**HAVE:**

$$
Z_{\mathcal T} = tr(\tilde\rho \rho^{T_1}) \tag{2}
$$

by cyclicity of trace.

**CONSIDER:**

$$
tr[(A \otimes B)(T_{I_1} \otimes S_{I_2})]
$$

$A, B$ 是全 $I$ 上的任意算符 (按 copy 切), $T_{I_1} = \bigotimes_{i \in I_1} T_i$, $S_{I_2} = \bigotimes_{i \in I_2} S_i$ (按区域切).

**HAVE:**

$$
tr[(A_i \otimes B_i)T_i] = tr(A_iB_i^T) \tag{3}
$$

$(T_i)^{ab}_{cd} = \delta^a_b\delta^c_d$, 直接缩并即得.

**HAVE:**

$$
A = \sum_{s, t} A^s_t|s\rangle\langle t|, \quad B = \sum_{s', t'} B^{s'}_{t'}|s'\rangle\langle t'|
$$

$s, t$ 跑遍全 $I$ 计算基 ($A, B$ 不必分解).

**HAVE:**

$$
(T_{I_1} \otimes S_{I_2})^{tt'}_{ss'} = \prod_{i \in I_1}\delta^{t_i}_{t'_i}\delta^{s_i}_{s'_i} \prod_{i \in I_2}\delta^{t_i}_{s'_i}\delta^{t'_i}_{s_i}
$$

$(S_i)^{ab}_{cd} = \delta^a_d\delta^b_c$, 与 $T_i$ 一起按点相乘.

**HAVE:**

$$
tr[(A \otimes B)(T_{I_1} \otimes S_{I_2})] = tr(AB^{T_1}) \tag{4}
$$

by contracting the above: $I_1$ 上迫出 $t_i = t'_i$, $s_i = s'_i$, $I_2$ 上迫出 $t_i = s'_i$, $t'_i = s_i$, 拼起来正是 $(B^{T_1})^t_s$.

**NOTE:**

严格说两边张量顺序差一个腿重排 $Q$ (copy-major vs region-major, 和 purity 证明里的 $P$ 一回事), trace 展开对其不敏感, 故略去.

**THEREFORE:**

取 $A = \tilde\rho$, $B = \rho$, 由 (2), (4):

$$
Z_{\mathcal T} = tr[(\tilde\rho \otimes \rho)(T_{I_1} \otimes S_{I_2})] \tag{5}
$$

**QED**
