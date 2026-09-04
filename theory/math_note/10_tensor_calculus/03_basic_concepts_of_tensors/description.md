# description

## Definition

### index

The properties of tensors include order and **type**.

For instance, 2 other include $(0, 2)$, $(1, 1)$, $(2, 0)$

Input of superscripts, output of subscripts, therefore, the components of vector is superscripts, the components of matrix is such as $a_i^j$, **But the higher-order types are unknown to me**.

### Vector

If

$$
\begin{cases}
\vec u = \sum_i u^i \hat e_i\\
\vec v = \sum_i u^i \hat f_i,
\end{cases}
$$

there

$$
[\vec u \otimes \vec v]^i_{j} = u^iv^j\hat e_i \hat f_j
$$

### Generally

If $A$ is an $r$-order tensor, $B$ is an $s$-order tensor, that is

$$
\begin{cases}
A_{i_1i_2...i_r}\hat e_{i_1} \hat e_{i_2} ...\hat e_{i_r}\\
B_{i_1i_2...i_s}\hat f_{j_1} \hat f_{j_2} ...\hat f_{j_s}\\
C = A \otimes B
\end{cases}
$$

where $C$ is an $r + s$ order tensor, Viz.,

$$
C_{t_1t_2...t_{r+s}} = A_{i_1i_2...i_r}B_{j_1j_2...j_s}\hat e_{i_1}\hat e_{i_2}...\hat e_{i_r}\hat f_{j_1}\hat f_{j_2}...\hat f_{j_s}
$$

### Cronbach's coefficient form

<!--克罗内克积形式-->
There are the form of 2 orders.

$$
[A \otimes B]^{ik}_{jl} = a^i_{j} b^k_{l} = T^{ij}_{kl}
$$

## Properties

### Tensorproduct

$$
(A \otimes B)(C \otimes D) = AC \otimes BD,
$$

proof as follow

### Disassemble to subspace

* $tr(\bigotimes_nA_n) = \prod_n tr(A_n)$
* $tr(A)B = tr_1(A\otimes B)$
* $(A \otimes B)(C \otimes D) = AC \otimes BD,$

### Commutative operations

* $(A \otimes B)^\dagger = A^\dagger \otimes B^\dagger$
* $(A \otimes B)^T = A^T \otimes B^T$
* $tr(\Pi A \Pi^\dagger) = tr(A)$, where $\Pi$ change the room order.
