# readout_mitigation

## 分配矩阵与比特顺序

以经典分配矩阵描述读出误判：

$$
\mathbf p_{\rm meas}=\mathsf A\mathbf p_{\rm ideal}.
$$

这里的理想分布仅指移除该读出误判后的分布，仍可包含门误差与态制备误差。
对逻辑比特 $q$，行表示测量结果，列表示制备态：

$$
M_q=
\begin{pmatrix}
P_q(0|0)&P_q(0|1)\\
P_q(1|0)&P_q(1|1)
\end{pmatrix}.
$$

取计算基 $|b_{L-1}\cdots b_0\rangle$，以 $b=\sum_{q=0}^{L-1}2^q b_q$ 编号。
在各比特读出误差相互独立的近似下，联合分配矩阵为

$$
\mathsf A=M_{L-1}\otimes\cdots\otimes M_0.
$$

每个单比特矩阵有两个独立误判概率，故该模型共有 $2L$ 个独立参数，
联合概率向量的维数仍为 $2^L$。该近似不描述一般关联读出误差。

## 线性求逆与欧氏概率投影

设各结果的观测频数构成向量 $\mathbf n$，总样本数为 $N=\sum_b n_b>0$。
归一化频率与线性反演向量为

$$
\widehat{\mathbf p}_{\rm meas}=\mathbf n/N,
\qquad
\mathbf v=\mathsf A^{-1}\widehat{\mathbf p}_{\rm meas}.
$$

假设 $\mathsf A$ 可逆。有限统计和模型失配可使 $\mathbf v$ 出现负分量。
将联合反演向量投影到概率单纯形，定义欧氏概率投影：

$$
\mathbf p_{\rm mit}
=\underset{\mathbf p\in\Delta_d}{\operatorname{argmin}}
\frac12\lVert\mathbf p-\mathbf v\rVert_2^2,
\qquad
\Delta_d=\left\{\mathbf p\in\mathbb R^d:
p_b\ge0,\ \sum_{b=0}^{d-1}p_b=1\right\},
\quad d=2^L.
$$

其解可由一个共同阈值表示：

$$
p_{{\rm mit},b}=\max(v_b-\tau,0),
\qquad
\sum_b\max(v_b-\tau,0)=1.
$$

由最优性条件，共同阈值可通过排序表示。将 $\mathbf v$ 降序排列为 $u_1,\ldots,u_d$，令

$$
c_k=\sum_{j=1}^k u_j,
\qquad
\rho=\max\left\{k:u_k-\frac{c_k-1}{k}>0\right\},
\qquad
\tau=\frac{c_\rho-1}{\rho}.
$$

投影作用于联合分布。对计算基对角观测量 $O$，若其本征值为 $o_b$，则

$$
\langle O\rangle_{\rm mit}=\sum_b o_b p_{{\rm mit},b}.
$$

## 统计性质

线性求逆可能放大统计误差，近奇异分配矩阵尤其不利。
欧氏投影是非线性映射；即使反演向量无偏，投影后的估计也不一定无偏。
