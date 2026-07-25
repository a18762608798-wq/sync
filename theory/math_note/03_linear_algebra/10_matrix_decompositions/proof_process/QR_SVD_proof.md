# QR SVD proof

### 数值线性代数中的分解方法与稳定性分析

针对您提出的关于 QR 分解、奇异值分解（SVD）以及条件数导致数值不稳定性的问题，以下基于数值线性代数标准理论（参考：Golub & Van Loan, *Matrix Computations*; Trefethen & Bau, *Numerical Linear Algebra*）进行严谨阐述。

---

#### 1. 条件数与数值不稳定性（Why Condition Number Matters）

**1.1 条件数的定义**
矩阵 $A \in \mathbb{R}^{m \times n}$ 的 2-范数条件数（Condition Number）定义为最大奇异值与最小奇异值之比：
$$
\kappa_2(A) = \frac{\sigma_{\max}(A)}{\sigma_{\min}(A)} = \|A\|_2 \|A^+\|_2
$$
条件数衡量了线性系统 $Ax=b$ 对输入误差（如 $b$ 的扰动或计算过程中的舍入误差）的敏感程度。相对误差放大倍数满足：
$$
\frac{\|\delta x\|}{\|x\|} \le \kappa(A) \frac{\|\delta b\|}{\|b\|}
$$

**1.2 正规方程的“平方效应”**
在正规方程 $A^T A x = A^T b$ 中，系数矩阵变为 $M = A^T A$。$M$ 的奇异值为 $A$ 的奇异值的平方（$\sigma_i(A^T A) = \sigma_i(A)^2$）。因此，$M$ 的条件数为：
$$
\kappa_2(A^T A) = \frac{\sigma_{\max}(A)^2}{\sigma_{\min}(A)^2} = \left( \kappa_2(A) \right)^2
$$

**1.3 为何导致数值不稳定？**
计算机使用浮点数算术（Floating-Point Arithmetic），具有有限的精度，通常用机器 epsilon（$\epsilon_{\text{mach}}$）表示（双精度约为 $10^{-16}$）。
*   **信息丢失**：若 $\kappa(A) \approx 10^8$，则 $\kappa(A^T A) \approx 10^{16}$。在双精度计算中，这意味着 $A^T A$ 的最小特征值可能在计算过程中被舍入误差淹没，导致矩阵在数值上奇异（Numerically Singular），即使理论上它是可逆的。
*   **精度损失**：求解过程中的相对误差上限变为 $\kappa(A)^2 \cdot \epsilon_{\text{mach}}$。若该值接近或超过 1，则计算结果将没有任何有效数字。
*   **形成 $A^T A$ 的过程**：显式计算 $A^T A$ 会引入额外的舍入误差，进一步恶化精度。

因此，严谨的数值计算应避免显式形成 $A^T A$。

---

#### 2. QR 分解（QR Decomposition）

**2.1 定义**
对于矩阵 $A \in \mathbb{R}^{m \times n}$ ($m \ge n$)，QR 分解（通常是Householder Reflections）将其分解为：
$$
A = Q R
$$
*   **$Q \in \mathbb{R}^{m \times m}$**：正交矩阵（Orthogonal Matrix），满足 $Q^T Q = Q Q^T = I$。其列向量构成 $\mathbb{R}^m$ 的标准正交基。
    *   *注：在“经济型”QR 分解中，$Q \in \mathbb{R}^{m \times n}$ 具有正交列（$Q^T Q = I_n$），$R \in \mathbb{R}^{n \times n}$。*
*   **$R \in \mathbb{R}^{m \times n}$**：上三角矩阵（Upper Triangular Matrix）。

**2.2 求解最小二乘**
利用正交变换不改变向量 2-范数的性质（$\|Qx\|_2 = \|x\|_2$）：
$$
\begin{aligned}
\| Ax - b \|_2 &= \| QRx - b \|_2 \\
&= \| Q^T(QRx - b) \|_2 \quad (\text{左乘 } Q^T) \\
&= \| Rx - Q^T b \|_2
\end{aligned}
$$
令 $Q^T b = \begin{bmatrix} c \\ d \end{bmatrix}$（d对应0行），其中 $c \in \mathbb{R}^n$。由于 $R$ 是上三角矩阵，最小化问题转化为求解上三角线性方程组：
$$
R_{1:n, 1:n} x = c
$$
可通过**回代法（Back Substitution）**高效求解。

**2.3 稳定性分析**
*   **条件数不平方**：正交矩阵的条件数 $\kappa(Q) = 1$。QR 分解算法（如 Householder 变换）是向后稳定的（Backward Stable）。
*   **误差传播**：求解过程的误差放大倍数仅与 $\kappa(A)$ 成正比，而非 $\kappa(A)^2$。
*   **适用性**：适用于满秩矩阵，计算复杂度约为 $2mn^2 - \frac{2}{3}n^3$ 次浮点运算，比正规方程略高但更安全。

---

#### 3. 奇异值分解（Singular Value Decomposition, SVD）

**3.1 定义**
对于任意矩阵 $A \in \mathbb{R}^{m \times n}$，SVD 将其分解为：
$$
A = U \Sigma V^T
$$
*   **$U \in \mathbb{R}^{m \times m}$**：左奇异向量矩阵，正交矩阵。
*   **$V \in \mathbb{R}^{n \times n}$**：右奇异向量矩阵，正交矩阵。
*   **$\Sigma \in \mathbb{R}^{m \times n}$**：对角矩阵（广义），对角线元素 $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_{\min(m,n)} \ge 0$ 为奇异值。

**3.2 求解最小二乘**
利用伪逆（Moore-Penrose Pseudoinverse）$A^+ = V \Sigma^+ U^T$，其中 $\Sigma^+$ 将 $\Sigma$ 非零对角元取倒数并转置。最小二乘解为：
$$
x_{LS} = A^+ b = V \Sigma^+ U^T b
$$
具体计算为：
$$
x_{LS} = \sum_{\sigma_i > 0} \frac{u_i^T b}{\sigma_i} v_i
$$

**3.3 稳定性与 robustness**
*   **最稳健方法**：SVD 显式揭示了矩阵的秩和奇异值结构。
*   **秩亏处理**：若 $A$ 秩亏（存在 $\sigma_i \approx 0$），可直接设定阈值截断小奇异值（Truncated SVD），获得最小范数解，而 QR 分解在处理秩亏时需配合列主元（Column Pivoting）。
*   **代价**：计算成本最高，约为 $12mn^2 + 8n^3$ 次浮点运算，通常是 QR 分解成本的数倍。

---

#### 4. 方法对比总结

| 特性        | 正规方程 (Normal Equations)  | QR 分解            | 奇异值分解 (SVD)            |
| :-------- | :----------------------- | :--------------- | :--------------------- |
| **核心公式**  | $x = (A^T A)^{-1} A^T b$ | $Rx = Q^T b$     | $x = V \Sigma^+ U^T b$ |
| **条件数影响** | $\kappa(A)^2$ (严重放大误差)   | $\kappa(A)$ (稳定) | $\kappa(A)$ (最稳定)      |
| **秩亏处理**  | 失败 (矩阵奇异)                | 需列主元 QR          | 天然支持 (截断小奇异值)          |
| **计算成本**  | 低 (最快)                   | 中 (约 2 倍于正规方程)   | 高 (约 5-10 倍于正规方程)      |
| **推荐场景**  | 条件数极好的良态问题               | 通用标准方法           | 病态矩阵、秩亏矩阵、高精度需求        |

**结论：**
条件数平方效应会导致浮点运算中的有效数字丢失，从而使正规方程在病态矩阵下失效。**QR 分解**通过正交变换避免了条件数平方，是通用场景下的标准选择；**SVD** 则提供了最彻底的数值稳定性及秩诊断能力，适用于高难度或病态问题。