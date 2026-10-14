# Hamming Distance

## purity

**DEFINITE:**

纯度的无偏估计器为,

$$
\hat P_2 = \frac{2^N}{MK(K-1)} \sum\limits_{m=1}^M\sum\limits_{k,k'=1;k\neq k'}^K (-2)^{-D[s^{(m, k)}, s^{(m, k')}]},
$$

where

$$
D[s^{(m, k)}, s^{(m, k')}] = \sum_i |s^{(m, k)}_i - s_i^{(m, k')}|.
$$

$i$ is the subscript of qubit.

**PROPERTY**:

$$
\mathbb E_{U, s, s'} [\hat P_2] = tr(\rho^2)
$$

**BY:**

[Hamming Twirling](../note/PRF-Hamming_Twirling.md)

## ZR

**DEFINITE:**

反射不变量的无偏估计器为,

$$
\hat Z_R = \frac{2^n}{MK} \sum\limits_{m=1}^M\sum\limits_{k=1}^K (-2)^{-D[s^{(m, k)}, \mathcal R(s^{(m, k)})]},
$$

where

$$
D[s^{(m, k)}, \mathcal R(s^{(m, k)})] = \sum_{i=1}^n |s^{(m, k)}_i - s^{(m, k)}_{\bar i}|.
$$

$i$ is the subscript of mirror pair, $\bar i$ is its reflection counterpart, **$n$ is the number of pairs**.

**PROPERTY**:

$$
\mathbb E_{U, s} [\hat Z_R] = tr(\rho \mathcal R) = Z_{\mathcal R}
$$

**BY:**

[Hamming Twirling](../note/PRF-Hamming_Twirling.md)

## ZT

**DEFINITE:**

时间反演不变量的无偏估计器为,

$$
\hat Z_T = \frac{2^{2n}}{MK^2} \sum\limits_{m=1}^M\sum\limits_{k, k' = 1}^K (-2)^{-D[s^{(m, k)}, s^{(m, k')}]},
$$

where

$$
D[s^{(m, k)}, s^{(m, k')}] = \sum_{i \in I} |s^{(m, k)}_i - s^{(m, k')}_i|.
$$

- $I = I_1 \cup I_2$ 是两次实验共用的 **$2n$ 比特区间**, $k$ ($k'$) 是实验 1 (实验 2) 的 shot 标记.
- 实验 1 在 $I_1$ 上先作用 $u_{\mathcal T} = \bigotimes_{i \in I_1} \sigma^y_i$;
- 测量方面, 两组实验在 $I_1$ 上的随机幺正取共轭配对, 在 $I_2$ 上取相同.

**PROPERTY**:

$$
\mathbb E_{U, s, s'} [\hat Z_T] = Z_{\mathcal T}
$$

$Z_{\mathcal T}$ 是含 $I_1$ 上部分转置与 $u_{\mathcal T}$ 的时间反演 MBTI.

**BY:**

[Hamming Twirling](../note/PRF-Hamming_Twirling.md)
