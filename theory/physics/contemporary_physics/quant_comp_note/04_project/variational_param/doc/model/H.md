# AHC 哈密顿量

$$
H(s,\delta)=\sum_{i=0}^{d}\left[(1-s)h_{2i,2i+1}(\delta)+sh_{2i+1,2(i+1)}(\delta)\right]
$$

$$
\begin{cases}
d = L/2-1 \\
h_{k,l}(\delta)=e^{-\delta}(X_{k}X_{l}+Y_{k}Y_{l})+e^{+\delta}Z_{k}Z_{l}
\end{cases}
$$

* $L$ 取 4 的倍数，$k=0,\cdots,L-1$，周期边界即 $L\equiv 0$；
* $2i$ 和 $2i+1$ 组成 unitcell $i$；
* $s\in[0,1]$，$1-s=J^{\prime}$，$s=J$；$s=0$ 为平庸 dimer 端，$s=1$ 为 SPT 端；
* $\delta\in[-3,3]$，等效 $\Delta=e^{2\delta}$，$\delta=0$ 回到各向同性点。
