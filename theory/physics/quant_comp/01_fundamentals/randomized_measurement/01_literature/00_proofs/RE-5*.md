# RE-5*：$T_1$ 型非 unital 下的 Hamming 核重证

本文档对应假设 5*：只考虑 $T_1$ 型非 unital 噪声，$\Lambda(I)$ 为对角形。
主文档见 [02_Robust-Estimation](../02_Robust-Estimation.md)，记号沿用该文档
（pair 两腿通道分别记为 $\Lambda_1,\Lambda_2$，单比特下标为 $j$）。

## 设定

$T_1$（振幅阻尼）下每条腿的 $\Lambda(I)$ 为

$$
\Lambda_k(I) = (1+\delta_k)|0\rangle\langle 0| + (1-\delta_k)|1\rangle\langle 1|,\quad k=1,2
$$

其中 $\delta_k = \gamma_k = 1-e^{-t_k/T_1}$ 为阻尼偏置。
于是单比特迹为

$$
c_0^{(k)} = tr[\Lambda_k^*(|0\rangle\langle 0|)] = 1+\delta_k
$$

$$
c_1^{(k)} = tr[\Lambda_k^*(|1\rangle\langle 1|)] = 1-\delta_k
$$

仍假设门无关、局域、保迹（$\Lambda_k^*(I)=I$，即 $\Lambda_k$ 保迹），
twirl 结构 $\tau_j^{(2)}(\omega_j)=aI+bS_j$ 保持不变。
$\Lambda(I)$ 的非对角元不进入下面的 $c_s$，
其余噪声结构被 $A_j$ 吸收后直接标定。

记 $x_j=g(0,0)=g(1,1)$，$y_j=g(0,1)=g(1,0)$，$\varepsilon=\delta_1\delta_2$。

## $u$ 方程（含 $\delta$）

$$
\begin{split}
tr(\omega_j) &= \sum_{s_j,s_j'}g(s_j,s_j')
tr(\Lambda_1^*(|s_j\rangle\langle s_j|))
tr(\Lambda_2^*(|s_j'\rangle\langle s_j'|)) \\
&= x_j(c_0^{(1)}c_0^{(2)}+c_1^{(1)}c_1^{(2)})
+ y_j(c_0^{(1)}c_1^{(2)}+c_1^{(1)}c_0^{(2)}) = 2
\end{split}
$$

直接计算得

$$
c_0^{(1)}c_0^{(2)}+c_1^{(1)}c_1^{(2)} = 2(1+\varepsilon)
$$

$$
c_0^{(1)}c_1^{(2)}+c_1^{(1)}c_0^{(2)} = 2(1-\varepsilon)
$$

故 $u$ 方程变为

$$
(1+\varepsilon)x_j + (1-\varepsilon)y_j = 1 \tag{1*}
$$

$\delta_1=\delta_2=0$ 时回到 $x_j+y_j=1$。

## $t$ 方程（形式不变）

$$
tr(S_j\omega_j) = A_jx_j + B_jy_j = 4 \tag{2}
$$

其中 $A_j,B_j$ 为 cross-overlap。
保迹仍给出

$$
A_j+B_j = tr(\Lambda_1^*(I)\Lambda_2^*(I)) = 2 \tag{3}
$$

## 求解

记 $s=x_j+y_j$，$d=x_j-y_j$，则 $(1*)$ 化为 $s+\varepsilon d=1$，
$(2)$ 化为 $s+(A_j-B_j)d/2=4$。联立得

$$
d = \frac{3}{(A_j-B_j)/2-\varepsilon}
$$

$$
s = 1-\varepsilon d
$$

$$
x_j = \frac{s+d}{2},\quad y_j = \frac{s-d}{2}
$$

用 $A_j+B_j=2$ 消去 $B_j$（即 $A_j-B_j=2A_j-2$），得

$$
d = \frac{3}{A_j-1-\varepsilon}
$$

$$
s = 1-\frac{3\varepsilon}{A_j-1-\varepsilon}
$$

检验：$\varepsilon=0$ 时 $d=3/(A_j-1)$，$s=1$，
即 $x_j=(2+A_j)/(2A_j-2)$，$y_j=(A_j-4)/(2A_j-2)$，回到主文档公式。

平稳 pair（$\delta_1=\delta_2=\delta_j$）时 $\varepsilon=\delta_j^2$，
只需在 $A_j$ 之外每比特多标一个 $\delta_j$。

## Calibration（含 $\delta$）

$$
D_j = \sum_{s_j}\Lambda_1^*(|s_j\rangle\langle s_j|)\otimes\Lambda_2^*(|s_j\rangle\langle s_j|)
$$

$$
tr(D_j) = c_0^{(1)}c_0^{(2)}+c_1^{(1)}c_1^{(2)} = 2(1+\varepsilon)
$$

$$
tr(S_jD_j) = A_j
$$

设 $\tau_j^{(2)}(D_j)=cI+dS_j$，则

$$
\begin{cases}
4c+2d = 2(1+\varepsilon)\\
2c+4d = A_j
\end{cases}
\Rightarrow
\begin{cases}
c = \frac{4(1+\varepsilon)-A_j}{6}\\
d = \frac{A_j-(1+\varepsilon)}{3}
\end{cases}
$$

一致率 $E_j^{(=)}=c+d$ 给出

$$
E_j^{(=)} = \frac{2+A_j+2\varepsilon}{6}
\rightarrow
A_j = 6E_j^{(=)}-2-2\varepsilon
$$

$\delta$ 本身由单 shots 频率的 Haar 平均读出：
$E_U[P(s_j|U_j)]=c_s/2$，故

$$
\hat\delta_j = \bar f_{0,j}-\bar f_{1,j} = 2\bar f_{0,j}-1
$$

$\bar f$ 为 calibration 数据中该比特出现 $0$ 的总体频率
（两腿分别统计即得 $\delta_1,\delta_2$；平稳时取同一值）。

## 小结

$T_1$ 型下框架不塌：目标仍是 $\tau_j^{(2)}(\omega_j)=S_j$（按主文档归一化），
代价是每比特标定量从单个 $A_j$ 增加为 $(A_j,\delta_j)$，
$\delta_j\to 0$ 时所有公式回到主文档。
