---
bibliography: references.bib
collection:
  - intensive 
---
# Robust Estimation

## CS shadow

## hamming distance

The version of noiseless ref to [hamming_noiseless](./00_proofs/twirling/hamming_noiseless.md),

Now we try to give the mitigation of hamming distance.

The ideal noise Born rule is

$$
\begin{split}
P_\Lambda(s|U)=\langle s|\Lambda(U\rho U^\dagger)|s\rangle
=\mathrm{tr}\bigr(\rho\,U^\dagger\Lambda^*(|s\rangle\langle s|)U\bigr).
\end{split}
$$

参考无噪声情况, 同理噪声估计器有:

$$
\mathbb E_{U} [\sum_{s, s'} g(s, s')
tr(\rho P_\Lambda(U, s))tr(\rho P_\Lambda(U, s'))]\\
$$

**其中 $g(s, s')$ 是无噪声下估计器 $f(s, s')$ 的变式,
用来保证噪声通道下估计器的无偏性**.
写成 twirling 通道格式:

$$
\begin{split}
expr
&= tr[(\rho \otimes \rho)
\mathbb E_U[U^{\otimes 2}
(\sum_{s, s'} g(s, s')
\Lambda^* (|s\rangle\langle s|)
\otimes \Lambda^*(|s'\rangle \langle s'|))
(U^\dagger)^{\otimes 2}]]\\
&= tr[(\rho \otimes \rho)\tau^{(2)}(\tilde W)]
\end{split}
$$

Where

$$
\begin{split}
&\tilde W = \sum_{s, s'} g(s, s')
\Lambda^*(|s\rangle\langle s|)
\otimes \Lambda^*(|s'\rangle\langle s'|)\\
&\tau^{(2)}[\cdot]
= \mathbb E_U[U^{\otimes 2}(\cdot)(U^\dagger)^{\otimes 2}]
\end{split}
$$

目标依然是 $\tau^{(2)}(\cdot)$ 项对应为 SWAP，
即 $\tau^{(2)}(\tilde W)=S$。
