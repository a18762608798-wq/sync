# Cauchy Integral Formula [AI]

**REQUIRE:**

函数 $f(z)$ 在单连通区域 $D$ 内处处解析，$\Gamma$ 为 $D$ 内不自交的简单闭合围道，点 $a$ 位于 $\Gamma$ 内部.

**THEOREM:**

$$
f(a) = \frac{1}{2 \pi i} \oint_\Gamma \frac{f(z)}{z - a} \, dz \tag{1}
$$

**BY:**

[Cauchy Integral Theorem](CON-Cauchy_Theorem.md), [Contour Deformation Proof](PRF-Contour_Deformation.md)

**PROPERTY:**

$n$ 阶导数公式：

$$
f^{(n)}(a) = \frac{n!}{2 \pi i} \oint_\Gamma \frac{f(z)}{(z - a)^{n+1}} \, dz
$$

**CHECK:**

若 $f(z) = 1$ 为常数函数，则式 (1) 化为 $\oint_\Gamma \frac{dz}{z - a} = 2 \pi i$，与直接参数化 $z = a + r e^{i\theta}$ 计算一致.

**CAVEAT:**

点 $a$ 必须严格位于 $\Gamma$ 内部；若 $a$ 在 $\Gamma$ 外部，则被积函数在 $\Gamma$ 内处处解析，积分值为 $0$. 要求 $f(z)$ 在 $\Gamma$ 上及内部均解析，不可含有分支切割穿过 $\Gamma$.
