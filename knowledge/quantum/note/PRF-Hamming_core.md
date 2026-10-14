# Hamming core

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
a = 1\\
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
