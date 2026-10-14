# PRF S form

## 张量形式

**IF:**

$$
\phi = S \psi
$$

**THEN:**

$$
\phi^{s_1', s_2'} = S^{s_1', s_2'}_{s_1, s_2} \psi^{s_1, s_2}
$$

**REQUIRE:**

$$
\phi^{s_1', s_2'} = \psi^{s_2', s_1'}
$$

**NOTE:**

这里的 $s_i$ 是求和哑指标, 是用来求和的, 不是直接交换的作用.

交换的作用本质上体现在对**输出槽位**(相对于S)的颠倒.

**HAVE:**

$$
S^{s_1', s_2'}_{s_1, s_2} = \delta^{s_1'}_{s_2}\delta^{s_2'}_{s_1}
$$

## 狄拉克形式

**HAVE:**

$$
\begin{split}
S &= ISI = \sum_{ab} |ab\rangle\langle ab| S \sum_{cd} |cd\rangle\langle cd|\\
&= \sum_{abcd} |ab\rangle \langle ab|cd \rangle \langle cd|\\
&= \sum_{ab} |ab\rangle \langle ba|
\end{split}
$$
