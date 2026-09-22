# initial state

条件：$H'$ 基态（用 $H'$ 而非 $H$ 以区分简并）+ 易在电路上制备。$|s\rangle=(|01\rangle-|10\rangle)/\sqrt{2}$，格点 $0$-indexed。

## 平庸 $s=0,\delta=-3$：intra 单态乘积

$$
|\psi_{\rm triv}\rangle=\bigotimes_{(0,1),(2,3),(4,5),(6,7)}|s\rangle
$$

* 与 $H'$ 基态保真度 $1$；每对局域 $H+{\rm CNOT}+Z$ 制备。

## 拓扑 $s=1,\delta=-3$：bulk 单态 + 首尾单态

$$
|\psi_{\rm topo}\rangle=|s\rangle_{0,7}\bigotimes_{(1,2),(3,4),(5,6)}|s\rangle
$$

* 裸 $H$ 四重简并，$H'$ 打开 gap 并选出 $P=-1$ 分支，与上式保真度 $1$；
* 中间三对局域制备，$(0,7)$ 对需长程 ${\rm CNOT}$ 或 SWAP 链。

## 反铁磁 $s\approx 0.5,\delta=3$：Neel GHZ

> 理论上不是必须 s=0.5，相内两边都可以；实际取中间只是为了效果最好.

$$
|\psi_{\rm AFM}\rangle=(|01010101\rangle+|10101010\rangle)/\sqrt{2}
$$

* $s=0.5,\delta=3$ 处与 $H'$ 基态保真度 $\approx 1$；注意 $s=0,1$ 处即使 $\delta=3$ 仍是单态乘积，不是反铁磁；
* 制备：奇数位 $X$ + $H$ + 链式 ${\rm CNOT}$，深度 $O(L)$。
