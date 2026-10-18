# Contour Deformation Proof [AI]

**INTERPRET:**

从柯西积分定理推出有限区域内的围道变形公式，即同端点路径在无奇点区域内积分相等.

**GIVEN:**

$f(z)$ 在单连通区域 $D$ 内处处解析：

$$
\oint_\Gamma f(z) \, dz = 0 \tag{1}
$$

对 $D$ 内任意简单闭合围道 $\Gamma$ 成立. 设 $C_1$ 与 $C_2$ 为 $D$ 内连接同一起点 $a$ 到同一终点 $b$ 的两条有向光滑路径，且二者围成的有限区域完全含于 $D$：

$$
\partial \Omega = C_1 \cup (-C_2) \tag{2}
$$

**GOAL:**

$$
\int_{C_1} f(z) \, dz = \int_{C_2} f(z) \, dz \tag{3}
$$

**HAVE:**

将 $C_1$ 与 $C_2$ 的反向 $-C_2$ 首尾相接构成简单闭合围道 $\Gamma = C_1 \cup (-C_2)$：

$$
\oint_\Gamma f(z) \, dz = \int_{C_1} f(z) \, dz + \int_{-C_2} f(z) \, dz \tag{4}
$$

**BY:**

(1), (4)

**THEREFORE:**

由式 (1) 得 $\oint_\Gamma f(z) \, dz = 0$，结合反向路径性质 $\int_{-C_2} = -\int_{C_2}$，即得式 (3) 成立.

**BY:**

[Cauchy Integral Theorem](CON-Cauchy_Theorem.md)

**QED**
