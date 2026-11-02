# topological_op

$Z_{m}$ 为第 $m$ 格点上的 Pauli $Z$。

## 轻采样物理量

### string 原始形式

$$
O_{\rm str}(d)=(Z_{1}+Z_{2})\left[\prod_{l=1}^{d-1}(-Z_{2l+1}Z_{2l+2})\right](Z_{2d+1}+Z_{2d+2})
$$

$$
O_{\rm str}=\langle O_{\rm str}(d=L/2-1)\rangle
$$

**这意味着真机的时候需要用整体shot估计这个非局域量.**

### AFM 结构因子原始形式

$$
S(q)=\frac{1}{L}\sum_{i=1}^{L}\sum_{j=1}^{L}e^{iq(i-j)}\langle Z_{i}Z_{j}\rangle
$$

$q=\pi$ 时：

$$
S(\pi)=\frac{1}{L}\sum_{i=1}^{L}\sum_{j=1}^{L}(-1)^{i-j}\langle Z_{i}Z_{j}\rangle
$$

### shot 平均标准差

string 与 AFM 均按样本平均估计，单次 shot 先算整体值 $x_{i}$，再平均。记 $N=N_{\rm shots}$，$\bar X=N^{-1}\sum_{i=1}^{N}x_{i}$，则

$$
{\rm std}(\bar X)={\rm std}(X)/\sqrt{N}
$$

其中 ${\rm std}(X)$ 为单次 shot 值的样本标准差：

$$
{\rm std}(X)=\sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(x_{i}-\bar X)^{2}}
$$

* string：$x_{i}$ 为该 shot 下 $O_{\rm str}$ 算符的整体取值；
* AFM：$x_{i}=L^{-1}\sum_{i,j}(-1)^{i-j}z_{i}z_{j}$，$z_{i}=\pm1$ 为该 shot 下各格点 $Z$ 测量值。

### 归一化可测观测量

$$
\hat S(\pi)=\frac{S(\pi)}{L},
\qquad
\hat O_{\rm str}=-O_{\rm str}.
$$

* $S(\pi)$ 的量级随链长 $L$ 线性增长，除以 $L$ 后与 $L$ 无关，可直接跨尺寸比较。
* $O_{\rm str}$ 在拓扑相关联态中取负值；取负号后与 $\hat S(\pi)$ 同向，数值增大对应拓扑序增强。

### 线性组合 $Q$

$$
Q=\frac{4}{3}-2\hat O_{\rm str}-\frac{4}{3}\hat S(\pi)
$$

$Q$ 是 $\tilde Z_{\mathcal R}$ 的线性代理。

## 重采样物理量: 归一化 ZR

$$
Z_{\mathcal R}={\rm Tr}(\rho_{I}{\mathcal R}_{I})
$$

$$
\tilde Z_{\mathcal R}=Z_{\mathcal R}/\sqrt{[{\rm Tr}(\rho_{I_{1}}^{2})+{\rm Tr}(\rho_{I_{2}}^{2})]/2}
$$

* $I=I_{1}\cup I_{2}$ 取中间 $2n$ 比特，$I_{1},I_{2}$ 为左右连续块，各 $n$ 比特，${\mathcal R}_{I}$ 为中央键镜像交换；一般取 $2n=L/2$，即 $n=L/4$（$L$ 为 4 的倍数），$L=8$ 时 $n=2$。
