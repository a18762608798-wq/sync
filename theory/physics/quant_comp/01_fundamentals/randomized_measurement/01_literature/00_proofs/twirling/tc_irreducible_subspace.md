# tc irreducible subspace

## 不可约不变子空间

- 不变子空间一定是**相对于某组操作**而言的.
- 指改操作对在某个子空间内部的态作用无法超出该子空间.
- 不可约指的是最精细的一组划分.

## $U\otimes U$ 不可约子空间

对于 $U\otimes U$, 为两份复制空间完全对等的幺正操作, 显然有最直接对易算子:

$$
[SWAP, U \otimes U] = 0
$$

其中 SWAP 顺序是两份空间的平行置换. 两份不可约子空间可以被两个SWAP量子数区分:

$$
\begin{split}
&\mathcal{H_+} = \{|00\rangle, |11\rangle, |00\rangle + |11\rangle\}\\
&\mathcal{H_-} = \{|00\rangle - |11\rangle\}
\end{split}
$$

也即:

$$
\mathbb C^2 \otimes \mathbb C^2 = \mathcal{H_+} \oplus \mathcal{H_-}
$$
