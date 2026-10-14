# Hamming core

## Phase 1

**GOAL:**

Calculate:

$$
\begin{cases}
u = tr(w_i)\\
t = tr(Sw_i)
\end{cases} \tag{1}
$$

**WHERE:**

$$
w_i = \sum_{s_i, s_i'}f(s_i, s_i')|s\rangle \langle s| \otimes |s'\rangle \langle s'|
$$

**MOTIVATION:**

Which related to the form of hamming core.

**GIVEN**

$$
\tau_i (w_i) = \mathbb E_{V_i}[(V_i^\dagger)^{\otimes 2} w_i V_i^{\otimes 2}] \tag{2}
$$

**REQUIRE:**

$$
\tau_i(w_i) = S_i \tag{3}
$$

**HAVE:**

$$
\forall U_i, \quad [U_i \otimes U_i, \tau_i(w_i)] = 0\\ \Rightarrow \tau_i(w_i) = aI + bS_i \tag{4}
$$

**BY:**

[Schur Lemma](CON-Schur_Lemma.md)

**HAVE:**

$$
tr(\tau_i(\omega_i)) = tr(w_i) \tag{5}
$$

by(2), and

$$
tr(\tau_i(w_i)) = 4a + 2b \tag{6}
$$

by(4).

**HAVE:**

$$
tr(\tau_i(Sw_i)) = tr(Sw_i) \tag{7}
$$

and

$$
tr(\tau_i(Sw_i)) = tr(S\tau_i(w_i)) = 2a + 4b \tag{8}
$$

**BY:**

(1), (3), (5), (6), (7), (8)

**THEREFORE:**

$$
\begin{cases}
a = 0\\
b = 1
\end{cases}
$$

and,

$$
\begin{cases}
u = 2\\
t = 4
\end{cases}
$$

## Phase 2

**GOAL:**

Calculate:

$$
\begin{cases}
u = tr(w_i)\\
t' = tr(T_iw_i)
\end{cases} \tag{9}
$$

**WHERE:**

$$
w_i = \sum_{s_i, s_i'}f(s_i, s_i')|s\rangle \langle s| \otimes |s'\rangle \langle s'|, \quad T_i = S_i^{T_2}
$$

**GIVEN**

$$
\tau^\Psi_i (w_i) = \mathbb E_{V_i}[(V_i^\dagger \otimes V_i^T) w_i (V_i \otimes V_i^\ast)] \tag{10}
$$

$I_1$ 上的共轭配对 twirl 通道.

**REQUIRE:**

$$
\tau^\Psi_i(w_i) = T_i \tag{11}
$$

**HAVE:**

$$
\forall U_i, \quad [U_i \otimes U_i^\ast, \tau^\Psi_i(w_i)] = 0\\ \Rightarrow \tau^\Psi_i(w_i) = aI + bT_i \tag{12}
$$

**BY:**

[Schur Lemma](CON-Schur_Lemma.md)

**HAVE:**

$$
tr(\tau^\Psi_i(w_i)) = tr(w_i) \tag{13}
$$

by(10), and

$$
tr(\tau^\Psi_i(w_i)) = 4a + 2b \tag{14}
$$

by(12), $tr(T_i) = 2$.

**HAVE:**

$$
tr(\tau^\Psi_i(T_iw_i)) = tr(T_iw_i) \tag{15}
$$

and

$$
tr(\tau^\Psi_i(T_iw_i)) = tr(T_i\tau^\Psi_i(w_i)) = 2a + 4b \tag{16}
$$

by $tr(T_i^2) = 4$.

**BY:**

(9), (11), (13), (14), (15), (16)

**THEREFORE:**

$$
\begin{cases}
a = 0\\
b = 1
\end{cases}
$$

and,

$$
\begin{cases}
u = 2\\
t' = 4
\end{cases}
$$
