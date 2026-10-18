# Contour Integral [AI]

**CONCEPT:**

复平面是二维的，从起点 $z_1$ 到终点 $z_2$ 的复积分依赖于连接两点的有向曲线 $C$（称为路径或围道 contour）.

**DEFINITION:**

设复平面上的有向光滑曲线 $C$ 参数化为 $z(t) = x(t) + i y(t)$（$t \in [t_1, t_2]$），则复函数 $f(z)$ 沿围道 $C$ 的线积分为

$$
\int_C f(z) \, dz = \int_{t_1}^{t_2} f(z(t)) \, z'(t) \, dt
$$

**PROPERTY:**

模估计不等式（ML 不等式）：设围道 $C$ 的弧长为 $L$，且在 $C$ 上满足 $|f(z)| \le M$，则

$$
\left| \int_C f(z) \, dz \right| \le M L
$$
