# Positive Definite Matrices

## In math

矩阵所有特征值都是正数的矩阵称为正定矩阵。

## Hermite Matrices

实际上量子力学里面大多是Hermite半正定，也就是
在自身表象下的 Hermite operator 对角元非负实数(也就是本征值非负数)，可以写成向量的模方。

$$
\eta^i_i = \sum_k {a^k_i}^* a^k_i = \alpha^\dagger \alpha
$$

对于所有对角元，写成矩阵形式自然有

$$
\eta = A^\dagger A
$$

或者说在任何表象下有

$$
N = U^\dagger \eta U = (U^\dagger AU)^\dagger(U^\dagger A U) = B^\dagger B
$$

其对角元依然保证非负，

$$
N^i_i = \sum_k |B^k_{\;i}|^2 \ge 0
$$
