# Chapter 12

## 量子跃迁

假设：
* 系统能量为 $H(t) = H_0 + H'(t)$ 。 
* 跃迁初态为 $H_0$ 的本证态，也即 $\psi_k(t) = \phi_k$ ，$k$ 只起到标记初态的作用。
* 定义 $\phi_k(t) = e^{-iH_0t}\phi_k$
* 标记跃迁概率为 $P_{nk}(t) = |\langle \phi_n(t) |\psi_k(t)\rangle|^2 =|\langle \phi_n|\psi_k(t)\rangle|^2$ 也就是从初态 $\phi_k$ 经历 $t$ 时间最后到达 $\phi_n$ 的概率。

将

$$
\psi_k(t) = \sum_n C_{nk}(t) \phi_n(t)
$$

代人 shrodinger equation，有

$$
i\partial_t C_{k'k}(t) = \sum_n e^{i\omega_{k'n}t} H'_{k'n} C_{nk}(t)\tag{1}
$$

where

$$
\begin{cases}
C_{nk}(0) = \delta_{nk}\\
\omega_{k'n} = (E_{k'} - E_n) / \hbar
\end{cases}
$$

## 含时微扰论

Let

$$
C_{nk} = C_{nk}^{(0)} + C_{nk}^{(1)} + ...
$$

0 级微扰：

$$
H' = 0
$$

where

$$
C_{nk}^{(0)}(t) = C_{nk}^{(0)} (0) = \delta_{nk}
$$

1 级微扰:

对于 (1) 式右边，let
$$
C_{nk}(t) = C_{nk}^{(0)}(t) = \delta_{nk}
$$

则有

$$
i\partial_t C^{(1)}_{k'k}(t) = e^{i\omega_{k'k}t} H'_{k'k}
$$

解得

$$
C^{(1)}_{k'k}(t) = -i \int_0^t e^{i\omega_{k'k}t} H'_{k'k} dt
$$

一般我们还是关注这个一阶微扰，因为肯定是关系跃迁出来的这部分。

## 例子

### 周期微扰

$$
H'(t) = H'e^{-iwt}
$$

$$
P_{k'k}(t) = 4|H_{k'k}|^2 [\frac{\sin[(w_{k'k} - w)/2]}{w_{k'k} - w}]^2
$$

当 $(w_{kk}' - w) t >> 1$

$$
P_{k'k}(t) = 2\pi t|H_{k'k}|^2 \delta(w_{k'k} - w)
$$

### 常微扰

$$
H'(t) = H'[\theta(t) - \theta(t - T)]
$$

当 $t \ge T$

$$
P_{k'k}(t) = |H'_{k'k}|^2 \frac{\sin^2(w_{k'k} T/2)}{(w_{k'k}/2)^2}
$$

当 $t \ge T$ , $w_{k'k}T >> 1$ ，类似绝热演化条件，

$$
P_{k'k}(t) = 2\pi |H_{k'k}|^2\delta(w_{k'k})T
$$

当 $w_{k'k} \rightarrow 0$

$$
P_{k'k}(t) = |H'_{k'k}|^2 T^2
$$

这个表达式比较荒谬，说明此时一阶微扰不成立