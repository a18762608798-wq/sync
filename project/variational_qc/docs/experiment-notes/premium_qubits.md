# premium_qubits

稳定子期望值和计算基读出概率可作为量子比特及其连接的质量指标。

## cluster 态和其稳定子

### 态

cluster 态是制备电路的理想输出，全 $H$ 加 $CZ$ 链：

$$
|C\rangle=\prod_{\langle ij\rangle}CZ_{ij}|+\rangle^{\otimes n}
$$

其中 $|+\rangle$ 为 $X$ 本征值 $+1$ 态，$\langle ij\rangle$ 取遍链（环）的每条边。

### 稳定子

cluster 态是其稳定子的共同 $+1$ 本征态：

$$
S_{i}|C\rangle=+1|C\rangle
$$

对含 $n$ 个格点的开链，端点稳定子为 $S_0=X_0Z_1$、
$S_{n-1}=Z_{n-2}X_{n-1}$，内部稳定子为

$$
S_i=Z_{i-1}X_iZ_{i+1},\qquad i=1,\ldots,n-2.
$$

对周期环，稳定子取相同形式，指标按模 $n$ 解释。
这些稳定子彼此对易，满足 $[S_i,S_j]=0$。

## 稳定子均值

各 $\langle S_i\rangle$ 的平均定义为

$$
\bar{S}=\frac{1}{n}\sum_{i}\langle S_{i}\rangle
$$

理想簇态满足 $\bar S=1$。
对链或偶数环，按指标奇偶分组时，同组稳定子在各比特上的局域 Pauli 测量基相容。
两个组使用不同的局域测量基，但稳定子之间仍然对易。

## 读出保真度

用全零、全一制备下读回相同位串的条件概率，定义

$$
F_{\rm ro}=\frac12\left[
P(0^n\mid0^n)+P(1^n\mid1^n)\right].
$$

该量反映计算基制备与读出的综合质量。

## 加权质量指标

$$
{\rm score}=w\bar S+(1-w)F_{\rm ro},\qquad 0\le w\le1.
$$

权重 $w$ 控制两类指标的相对贡献。该加权值是质量指标，不等同于簇态保真度。
