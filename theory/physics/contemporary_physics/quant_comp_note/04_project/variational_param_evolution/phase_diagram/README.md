# README

这个子项目用来绘制相图.

## 哈密顿量

$$
H = J_1 \sum_{i} (X_i X_{i+1} + \delta Y_i Y_{i+1}) + J_2 (\sum_j X_j X_{j+1} + \delta Y_j Y_{j+1}).
$$

其中,

$$
\begin{cases}
J_1 = 1 - s\\
J_2 = s\\
i \in 2N^+ - 1\\
j \in 2N^+\\
\end{cases}.
$$

### Z_R

对于拓扑量 $Z_R$ 定义有:

$$
\hat Z_R = \frac{tr(\rho S)}{\sqrt{tr(\rho_1^2)}tr(\rho_2^2)}.
$$

其中,

$$
S = \bigotimes_{i=1}^{N/2} SWAP_{i, N-i+1},
$$

对于8比特系统，N = 4, 子系统 1 为 $(3, 6)$, 子系统 2 为 $(4, 5)$.

## 图像内容

选择 $(s, \delta)$ 作为热力图参数空间，选择其基态作为量子态，绘制 $\langle \hat Z_R \rangle$
