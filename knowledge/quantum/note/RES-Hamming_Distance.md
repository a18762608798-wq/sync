# Hamming Distance

记号：$M$ 为随机幺正设置数，$K$ 为每设置 shots 数，$D$ 为 Hamming 距离（逐比特差之和）。

## purity

$$
\hat P_2 = \frac{2^N}{MK(K-1)} \sum\limits_{m=1}^M\sum\limits_{k,k'=1;k\neq k'}^K (-2)^{-D[s^{(m, k)}, s^{(m, k')}]},
$$

$$
D[s^{(m, k)}, s^{(m, k')}] = \sum_i |s^{(m, k)}_i - s_i^{(m, k')}|,
$$

$i$ 为比特标号。$\mathbb E_{U, s, s'} [\hat P_2] = tr(\rho^2)$。

## ZR

$$
\hat Z_R = \frac{2^n}{MK} \sum\limits_{m=1}^M\sum\limits_{k=1}^K (-2)^{-D[s^{(m, k)}, \mathcal R(s^{(m, k)})]},
$$

$$
D[s^{(m, k)}, \mathcal R(s^{(m, k)})] = \sum_{i=1}^n |s^{(m, k)}_i - s^{(m, k)}_{\bar i}|,
$$

$i$ 为对标号，$\bar i$ 为镜像对应，$n$ 为对数。$\mathbb E_{U, s} [\hat Z_R] = tr(\rho \mathcal R) = Z_{\mathcal R}$。

## ZT

$$
\hat Z_T = \frac{2^{2n}}{MK^2} \sum\limits_{m=1}^M\sum\limits_{k, k' = 1}^K (-2)^{-D[s^{(m, k)}, s^{(m, k')}]},
$$

$$
D[s^{(m, k)}, s^{(m, k')}] = \sum_{i \in I} |s^{(m, k)}_i - s^{(m, k')}_i|,
$$

$I = I_1 \cup I_2$ 为两次实验共用的 $2n$ 比特区间，$k$（$k'$）为实验 1（实验 2）的 shot 标记；实验 1 在 $I_1$ 上先作用 $u_{\mathcal T} = \bigotimes_{i \in I_1} \sigma^y_i$；$I_1$ 上随机幺正取共轭配对，$I_2$ 上取相同。$\mathbb E_{U, s, s'} [\hat Z_T] = Z_{\mathcal T}$（含 $I_1$ 上部分转置与 $u_{\mathcal T}$ 的时间反演 MBTI）。

**BY:**

[Hamming Twirling](../note/PRF-Hamming_Twirling.md)
