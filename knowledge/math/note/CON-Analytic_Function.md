# Analytic Function [AI]

**DEFINITION:**

若复函数 $f(z)$ 在点 $z_0$ 的极限

$$
f'(z_0) = \lim_{\Delta z \to 0} \frac{f(z_0 + \Delta z) - f(z_0)}{\Delta z}
$$

沿复平面任意方向逼近都存在且相等，则称 $f(z)$ 在 $z_0$ 处复可导. 若 $f(z)$ 在开区域 $D$ 内处处复可导，则称 $f(z)$ 在 $D$ 内解析（analytic / holomorphic）.

**PROPERTY:**

设 $f(z) = u(x, y) + i v(x, y)$，则 $f(z)$ 在区域 $D$ 内解析的必要条件是实部 $u$ 与虚部 $v$ 满足 Cauchy-Riemann 方程

$$
\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \quad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}
$$

**INTUITION:**

解析意味着函数在区域 $D$ 内没有任何坏点. 多项式、指数函数 $e^z$、三角函数及其复合在整个复平面 $\mathbb{C}$ 上处处解析，称为整函数.

**EXAMPLE:**

函数 $f(z) = 1/z$ 在 $z = 0$ 处不解析，函数 $f(z) = \bar{z}$ 在复平面上处处不解析.
