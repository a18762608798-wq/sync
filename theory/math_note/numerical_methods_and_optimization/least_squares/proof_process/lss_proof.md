
# lss_proof

在数学上，给定矩阵 $A \in \mathbb{R}^{m \times n}$ 和向量 $b \in \mathbb{R}^{m}$，若方程组 $Ax = b$ 无精确解（通常发生在 $m > n$ 且 $b$ 不在 $A$ 的列空间中时），则最小二乘解 $x_{LS}$ 定义为满足以下优化问题的向量：

$$
x_{LS} = \arg \min_{x \in \mathbb{R}^n} \| Ax - b \|_2^2
$$

**2. 数学推导与正规方程**

为了求解上述优化问题，通常对目标函数 $f(x) = \| Ax - b \|_2^2$ 关于 $x$ 求梯度并令其为零。

展开目标函数：
$$
\begin{aligned}
f(x) &= (Ax - b)^T (Ax - b) \\
&= x^T A^T A x - x^T A^T b - b^T A x + b^T b \\
&= x^T A^T A x - 2 b^T A x + b^T b
\end{aligned}
$$
*(注：利用标量的转置等于其自身，即 $x^T A^T b = (b^T A x)^T = b^T A x$)*

<span style="color:red">注意该函数为凸函数（二阶导半正定），梯度为0处为全局最小。</span>

$$
\nabla^2f(x) = 2A^\dagger A
$$
[^1] 二阶导半正定（可以取0）

对 $x$ 求梯度：

$$
\nabla f(x) = 2 A^T A x - 2 A^T b
$$

令梯度为零，得到**正规方程（Normal Equations）**：

$$
A^T A x = A^T b
$$

**3. 解的存在性与唯一性**

最小二乘解的存在性与唯一性取决于矩阵 $A$ 的秩（Rank）：

*   **存在性**：对于任意 $A \in \mathbb{R}^{m \times n}$ 和 $b \in \mathbb{R}^{m}$，最小二乘解始终存在。这是因为 $A^T b$ 始终位于 $A^T A$ 的列空间中。
*   **唯一性**：
    *   若 $A$ 具有满列秩（Full Column Rank，即 $\text{rank}(A) = n$），则矩阵 $A^T A$ 可逆，最小二乘解唯一，表达式为：
        $$
        x_{LS} = (A^T A)^{-1} A^T b
        $$
    *   若 $A$ 不满列秩（即 $\text{rank}(A) < n$），则 $A^T A$ 奇异，存在无穷多个最小二乘解。此时，通常引入**最小范数最小二乘解（Minimum Norm Least Squares Solution）**，利用 Moore-Penrose 伪逆（Pseudoinverse）$A^+$ 表示为：
        $$
        x_{LS} = A^+ b
        $$

**5. 数值计算方法**

在实际数值计算中，直接求解正规方程 $(A^T A)^{-1} A^T b$ 可能因 $A^T A$ 的条件数（Condition Number）是 $A$ 条件数的平方而导致数值不稳定。因此，严谨的数值计算通常采用以下分解方法：

1.  **QR 分解**：将 $A$ 分解为 $A = QR$，其中 $Q$ 为正交矩阵，$R$ 为上三角矩阵。求解 $Rx = Q^T b$ 更为稳定。
2.  **奇异值分解 (SVD)**：将 $A$ 分解为 $U \Sigma V^T$。该方法最为稳健，尤其适用于秩亏（Rank-deficient）矩阵，可直接计算伪逆。