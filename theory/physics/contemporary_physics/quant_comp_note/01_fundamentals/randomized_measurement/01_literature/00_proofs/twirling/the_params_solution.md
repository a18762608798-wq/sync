# the params solution

## purity

> 这个证明不涉及 $\omega_j$ 的具体形式

Known

$$
\tau^{(2)}_j(\omega_j) = aI + bS_j
$$

对于其系数的求取, 需要利用此函数的 trace-preserving 属性
以及和 $S_j$ 的交换性, Viz.,

$$
\begin{split}
&u = tr(\tau_j^{(2)}(\omega_j)) = tr(\omega_j) \\
&t = tr(S_j\tau_j^{(2)}(\omega_j)) = tr(S_j\omega_j) \\ \tag{1}
\end{split}
$$

> **注意I和S并不是正交矩阵基, 所以系数不是直接trace.**

**由此我们可以通过构建 $\omega_j$ 形式,
得到不同的 $tr(\omega_i)$, $tr(S_j\omega_j)$ 以指定a, b.**

此关系证明如下:

$$
\begin{split}
& tr[\tau_j^{(2)}(\omega_j)]
= tr[\mathbb E_{U}[(U^\dagger)^{\otimes 2} \omega_j U^{\otimes 2}]]
= \mathbb E_U [tr(\omega_j)] = tr(\omega_j)\\
& tr[S_j\tau_j^{(2)}(\omega_j)] = tr[\mathbb E_U[(U^\dagger)^{\otimes 2} S_j\omega_j U^{\otimes 2}]] =tr(S_j \omega_j)
\end{split}
$$

又因为:

$$
\begin{cases}
tr(\tau_j^{(2)}(\omega_j)) = 4a + 2b = u\\
tr(S_j\tau_j^{(2)}(\omega_j)) = 2a + 4b = t
\end{cases}
$$

我们经常有 $a = 0, b = 1$, 也即:

$$
\begin{cases}
u = 2\\
t = 4
\end{cases}
$$
