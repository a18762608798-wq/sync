# joint probability distribution

$$
d\mu (U_1,..., U_N) = \prod\limits_{i = 1}^N d\mu(U_i)
$$

随机变量 X,Y 独立，当且仅当对任意集合 A,B 都有

$$
\begin{cases}
P(X∈A, Y∈B)=P(X∈A)P(Y∈B).\\
P(X∈A, Y∈B)=P(X∈A)P(Y∈B).
\end{cases}
$$

如果它们有联合密度，那就等价于

$$
f_{X,Y}(x,y)=f_X(x)f_Y(y).
$$

如果你用测度语言，那就是联合分布测度是边缘分布的乘积测度：

$$
μ_{X,Y}=μ_X⊗μ_Y.
$$
meaning

$$
d\mu(u, v) = J(u, v)du dv
$$

只有

$$
J(u, v) = a(u)b(v)
$$

也就是 $J$ 可分的时候才会有 $d\mu$ 可分

而在一般情况下，$J$ 作为联合概率分布有

$$
J(u, v) = f(u|v)f(v)
$$

