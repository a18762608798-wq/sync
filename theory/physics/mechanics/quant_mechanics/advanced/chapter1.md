---
bibliography: references.bib
collection:
  - book
---
# chapter1

## The interpertation of density operator

Ref to [@Noauthor-d, 5]

There are two interpertations:

* Proper mixture:

在自身表象下, 密度矩阵总可以写成:

$$
\rho = p_i P_i
$$

Where $P_i$ is the projector of self-representation.
Meaning: **系统客观上属于某个纯态 $\psi^i$, 但是无法区分, 只能做统计平均.**

NOTE: 对于任何力学量的测量单次测量结构是eigenval, 统计分布只影响概率权重.

* Inproper mixture

$$
[\rho_A]^{i_a}_{j_a} = [\rho_{AB}]^{i_a i_b}_{j_a i_b}
$$

**密度矩阵是更大系统的约化.**

使用这个形式是因为它是保证任意 local mechanical quantity 期望不变的必要条件.

$$
\begin{split}
&tr[(\rho_{AB} (F_A \otimes I_B)] \\
&= [\rho_{AB}]^{i_ai_b}_{j_aj_b}[F_A]^{j_a}_{i_a} \delta^{j_b}_{i_b} \\
&= [\rho_{AB}]^{j_a i_b}_{j_a i_b} [F_A]^{j_a}_{i_a} \\
&= tr[\rho_A F_A]
\end{split}
$$

## maximally mixed state

简单来说就是:

$$
I/d
$$

表示子系统出现什么态的概率都是相同的.

其有一些等价性质:

* 纯度最小: $tr(\rho^2) = 1/d$.
* 本征值全相等.
* von Neumann 的熵最大.

## semidefinite

定义: 对于任何态有:

$$
\langle F \rangle \ge 0
$$

其等价性质为本征vals都大于0:

$$
\lambda_i \ge 0
$$

特例是对于 $2 \times 2$ 矩阵, 这个问题等价于:

$$
\begin{cases}
tr(\rho) = \lambda_1 + \lambda_2 \ge 0 \\
det \rho = \lambda_1\lambda_2 \ge 0
\end{cases}
$$
