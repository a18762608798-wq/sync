# schur lemma

## Property

**如果一个算符 $F$ 与某一类操作 $U(p)$ 都交换，那么在 $U(P)$ 的每个不可约子空间上，
它只能是“常数乘单位算符”**.

从整个空间上来看, 改算符在每个子空间中是对此子空间的常数倍投影算符. 也即

$$
F = \sum_i \lambda_i P_i
$$

其中 $\lambda$ 为常数, $P_i$ 为对子空间的投影算符.

## main body

此证明中有:

$$
\tau_j^{(2)} (w) = \mathbb E_{V_j}[(V_j^\dagger)^{\otimes 2} w_j V_j^{\otimes 2}]
$$

又有:

$$
(U_j^\dagger)^{\otimes 2} \tau_j(\omega_j) U_j^{\otimes 2} = \tau_j^{(2)}(\omega_j)
$$

只是更换了一下幺正平均的符号, Viz.,

$$
[\tau_j^{(2)}(\omega_j), U \otimes U] = 0
$$

Ref to [tc_irreducible_subspacce](./tc_irreducible_subspace.md),
这里的不可约子空间是SWAP空间, 也即:

$$
\tau^{(2)}_j(\omega_j) = a P_+ + b P_- = cI + dS_j
$$

其中 $\hat P_\pm$ 是SWAP投影算符.
