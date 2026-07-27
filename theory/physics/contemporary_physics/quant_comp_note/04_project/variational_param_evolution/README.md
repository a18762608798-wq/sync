# README

## Description

此项目用于探讨 SSH 模型的基态在量子计算机上制备和拓扑 $Z_R$ 分类的可能性.

## Concept

### 哈密顿量

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
i, j \le N\\
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

**疑问：对于一般比特数，应该取多大的子系统求 ZR?**, 代码中暂取 $N/2$.

可以确定的是，对于8比特系统，N = 4, 子系统 1 为 $(3, 6)$, 子系统 2 为 $(4, 5)$.

## 思路流程

1. 数值相图绘制.
2. 绝热演化模拟和对称性初态选择.
3. 变分参数电路实验.
