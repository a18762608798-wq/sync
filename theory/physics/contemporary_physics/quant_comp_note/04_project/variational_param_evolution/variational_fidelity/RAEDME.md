# README

此项目用来验证变分电路在量子计算机的可行性.

## 变分电路

采用 `../variational_approach/README.md` 的一个改进版本:

外层对 **trotter分解阶数**, **步数**, 进行循环迭代.

内部对于**演化起点**, **二次 Bézier 曲线的控制参数**, **时间步长**, **分解时间点** 作为变分参数. cost function 是:

$$
\begin{split}
H_c &= (1-s) \sum_{i\text{ odd}} (X_i X_{i+1} + \delta Z_i Z_{i+1}) + s \sum_{j\text{ even}} (X_j X_{j+1} + \delta Z_j Z_{j+1}) \\
&- ϵ(\prod_{i=1}^{N} X_i + 2\prod_{i=1}^{N}Z_i) \\
\end{split}
$$

这里 $ϵ$ 暂且取1.
