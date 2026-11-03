# topological_op

$Z_{m}$ 为第 $m$ 格点上的 Pauli $Z$。

## 计算基对角观测量

### string 原始形式

$$
O_{\rm str}(d)=(Z_{1}+Z_{2})\left[\prod_{l=1}^{d-1}(-Z_{2l+1}Z_{2l+2})\right](Z_{2d+1}+Z_{2d+2})
$$

$$
O_{\rm str}=\langle O_{\rm str}(d=L/2-1)\rangle
$$

该算符由多体 $Z$ 乘积构成，其期望取决于联合分布，通常不能分解为单比特均值之积。

### AFM 结构因子原始形式

$$
S(q)=\frac{1}{L}\sum_{i=1}^{L}\sum_{j=1}^{L}e^{iq(i-j)}\langle Z_{i}Z_{j}\rangle
$$

$q=\pi$ 时：

$$
S(\pi)=\frac{1}{L}\sum_{i=1}^{L}\sum_{j=1}^{L}(-1)^{i-j}\langle Z_{i}Z_{j}\rangle
$$

### 样本均值与标准误

对独立同分布样本，记第 $\nu$ 个样本的观测量取值为 $x_\nu$，
$\bar X=N^{-1}\sum_{\nu=1}^{N}x_\nu$，样本均值的标准误估计为

$$
{\rm std}(\bar X)={\rm std}(X)/\sqrt{N}
$$

其中 ${\rm std}(X)$ 为单次观测值的样本标准差：

$$
{\rm std}(X)=\sqrt{\frac{1}{N-1}\sum_{\nu=1}^{N}(x_\nu-\bar X)^{2}}
$$

* string：$x_\nu$ 为该样本中 $O_{\rm str}$ 算符的整体取值；
* AFM：$x_\nu=L^{-1}\sum_{i,j}(-1)^{i-j}z_i^{(\nu)}z_j^{(\nu)}$，$z_i^{(\nu)}=\pm1$ 为各格点的观测值。

### 归一化可测观测量

$$
\hat S(\pi)=\frac{S(\pi)}{L},
\qquad
\hat O_{\rm str}=-O_{\rm str}.
$$

* $S(\pi)$ 的最大量级随链长 $L$ 线性增长，除以 $L$ 后满足 $0\leq\hat S(\pi)\leq1$；其取值仍可有有限尺寸依赖。
* $\hat O_{\rm str}=-O_{\rm str}$ 是符号约定，在拓扑参考态中为 $1$；对任意态并不保证落在 $[0,1]$。

定义晶胞自旋 $T_r^z=(Z_{2r-1}+Z_{2r})/2$。由
$\exp(i\pi T_r^z)=-Z_{2r-1}Z_{2r}$，string 算符等价地写为

$$
O_{\rm str}(d)=4T_1^z\exp\left(i\pi\sum_{r=2}^{d}T_r^z\right)T_{d+1}^z.
$$

### 线性组合 $Q$

$$
Q=\frac{4}{3}-2\hat O_{\rm str}-\frac{4}{3}\hat S(\pi)
$$

$Q$ 是以三个参考态标定的有限链关联诊断。
在 $L=8$ 的平庸、拓扑和 AFM 参考态上，$(\hat S,\hat O)$ 依次为
$(1/4,0)$、$(1/4,1)$、$(1,0)$，对应 $Q$ 为 $1$、$-1$、$0$。
对一般态，该组合不等同于 $\tilde Z_{\mathcal R}$，也不普遍量子化。

## 部分反射不变量

$$
Z_{\mathcal R}={\rm Tr}(\rho_{I}{\mathcal R}_{I})
$$

$$
\tilde Z_{\mathcal R}=Z_{\mathcal R}/\sqrt{[{\rm Tr}(\rho_{I_{1}}^{2})+{\rm Tr}(\rho_{I_{2}}^{2})]/2}
$$

* $I=I_{1}\cup I_{2}$ 取中间 $2n$ 比特，$I_{1},I_{2}$ 为左右连续块，各 $n$ 比特，${\mathcal R}_{I}$ 为中央键镜像交换；一般取 $2n=L/2$，即 $n=L/4$（$L$ 为 4 的倍数），$L=8$ 时 $n=2$。
