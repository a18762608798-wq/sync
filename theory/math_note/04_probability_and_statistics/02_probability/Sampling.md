# Sampling

## uniform sampling

the core step is to broken the room in Infinite element product, and make their probability density is a constant.

$$
\int_\Omega g(\Omega) f(\Omega)d\Omega = C\int_0^{2\pi}\int_{-1}^{1} g(\arccos u, \varphi) du d\varphi
$$

NOTE:  **本质上是同一个概率测度 / 同一个联合分布**，只是换了参数化方式，所以积分变量、积分区间、密度形式会跟着变。

其中：

1. 积分是几重，确实主要由样本空间的维数决定
2. 如果能找到一组坐标，使联合密度分解为各边缘密度的乘积，那么这些坐标变量是独立的

where $u = \cos\theta, f(u, \varphi) = C$  meaning sapmpling uniform

$$
\begin{cases}
u\in [-1, 1]\\
\varphi \in [0, 2\pi]
\end{cases}
$$

## Importance Sampling

There two kinds of importance sampling

If $f(\Omega) = C$ and you could sampe according to this distribution, totally sampe according it.

$$
\mathbb E_f[g] = \frac{1}{M} \sum_{k=1}^M g(\Omega_k)
$$

If your samping is limited to  $p(\Omega)$, set a power

$$
\mathbb E_f[g] = \mathbb E_p[g\frac{f}{p}]= \frac{1}{M} \sum_{k=1}^M g(\Omega_k) \frac{f(\Omega_k)}{p(\Omega_k)}
$$

In essence, the sampling operation itself simulates the probability distribution. Use continuous representation to understand it.

$$
\mathbb E_f[g] = \int g(x)f(x) dx = \int g(x) \frac{f(x)}{p(x)} p(x) dx
$$