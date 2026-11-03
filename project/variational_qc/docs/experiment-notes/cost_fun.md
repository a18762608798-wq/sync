# cost_fun

记参考态指标 $a\in\{{\rm triv},{\rm topo},{\rm AFM}\}$。
在固定模型参数 $(s^*,\delta^*)$ 下，能量代价函数为

$$
C_{a}(\theta)=\langle\psi_{a}(\theta)|H(s^{*},\delta^{*})|\psi_{a}(\theta)\rangle
$$

* $|\psi_{a}(\theta)\rangle = U(\theta)\,|\psi_{\mathrm{init},a}\rangle$，即 [orbit 拟设](./ansatz.md)电路作用在[初态](./psi0.md) $a$ 上的态；
多参考态变分族的最优能量定义为

$$
C^{*}(s^{*},\delta^{*})=\min_{a}\min_{\theta}C_{a}(\theta)
$$

由变分原理，任意归一化试探态均满足 $C_a(\theta)\ge E_0$，其中 $E_0$ 为目标哈密顿量的基态能量。
