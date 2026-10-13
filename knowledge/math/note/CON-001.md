# Fourier Series

**REQUIRE:**

$$
f(x) = f(x + 2L)
$$

**PROPOSITION:**

$$
\begin{split}
f(x) &= \frac{a_0}{2} + \sum_{n=1}^{\infty} [a_n \cos(nk_0 x) + b_n \sin(nk_0 x)]\\
&= \sum_{n=-\infty}^{\infty} c_n e^{i nk_0x}
\end{split}
$$

**WHERE:**

$$
\begin{split}
&k_0 = \frac{\pi}{L}\\
&a_n = \frac{1}{L}\int_{-T/2}^{T/2} f(x)\cos(k_0x) dx\\
&b_n = \frac{1}{L}\int_{-T/2}^{T/2} f(x)\sin(k_0x) dx
\end{split}
$$
