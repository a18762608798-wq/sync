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

Ref to:

1. [Hamming Twirling](../note/PRF-Hamming_Twirling.md)
