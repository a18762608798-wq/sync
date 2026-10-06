---
bibliography: references.bib
collection:
  - intensive 
---
# twiring channel of random measurement

## Core thinking

此方法的核心思路为下, 构建形如:

$$
\mathbb E_U [\hat {\mathcal{P_2}}] = tr[(\rho_1 \otimes \rho_2) SWAP]
$$

> 当估计量为一阶估计量的时候, 取 $\rho_2 = I$.

Where

$$
SWAP = \tau^{(2)}(W)
= \mathbb E_{U} [(U^\dagger)^{\otimes 2} W U^{\otimes 2}]
$$

> $W$ 是对 $s, s'$ 求和后的结果（不含 $U$），
> $\tau^{(2)}$ 是对 $U$ 求期望的三明治结构。
> 不需要额外的 $\Phi$：twirl 是投影算符，
> $\tau^{(2)}(W)$ 已落在 $\{I, S\}$ 里，
> 再平均一次不变（$\tau^2 = \tau$）。

SWAP, U, $\tau^{(2)}(W)$ 一般可以分解到每一对pair的子空间, 也即:

$$
\tau^{(2)}(W) = \otimes_j \tau_j(w_j) = S_j
$$

> 这里的符号是抽象表示, 纯粹按照 $\rho_1 \otimes \rho_2$ 空间顺序
无法直接写成直积形式.

由于所谓 **Schur 引理**(ref to [schur_lemma](./schur_lemma.md)),
$\tau^{(2)}(w_j)$ 的结构是固定的, 必然有

$$
\tau_j^{(2)}(w_j) = a I + bS_j
$$

由此根据估计器 $w_j$ 的具体形式
(ref to [the_params_solution](./the_params_solution.md))可以调整

$$
\begin{split}
a = 0\\
b = 1
\end{split}
$$

即可构建估计器.
