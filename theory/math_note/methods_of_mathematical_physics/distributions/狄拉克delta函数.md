# 狄拉克 delta 函数

## 1. 定义：用"筛选性质"定义，不画图像

$\delta$ 不是普通函数，而是**分布（distribution）/ 广义函数**：它由自己对测试函数 $f$ 的作用来定义，即筛选性质

$$
\int_{-\infty}^{+\infty} f(x)\,\delta(x - a)\,dx = f(a) .
$$

任何" $\delta(0) = \infty$ 、别处为 0 "的图像式说法都只是启发，不作定义用。

## 2. 基本性质（都在积分号下理解）

- 偶函数： $\delta(-x) = \delta(x)$
- 缩放： $\delta(ax) = \dfrac{\delta(x)}{|a|}$ ， $a \neq 0$
- 乘 $x$ 归零： $x\,\delta(x) = 0$ ，更一般 $x\,\delta'(x) = -\delta(x)$
- 复合函数：若 $g(x_i) = 0$ 且 $g'(x_i) \neq 0$ ，则

$$
\delta(g(x)) = \sum_i \frac{\delta(x - x_i)}{|g'(x_i)|} .
$$

- **导数**（分部积分，边界项为零）：

$$
\int f(x)\,\delta'(x - a)\,dx = -f'(a) .
$$

其中

$$
\partial_{x} \delta(x - x') = - \partial_{x'} \delta(x - x')
$$

## 3. 与阶跃函数的关系

Heaviside 阶跃函数 $\theta(x)$ 的广义导数就是 $\delta$ ：

$$
\theta'(x) = \delta(x), \qquad \int_{-\infty}^{x} \delta(t)\,dt = \theta(x) .
$$

## 4. Fourier 表示与连续谱正交归一

$$
\delta(x) = \frac{1}{2\pi}\int_{-\infty}^{+\infty} e^{ikx}\,dk,
\qquad
\delta(x - x') = \frac{1}{2\pi}\int_{-\infty}^{+\infty} e^{ik(x-x')}\,dk .
$$

这是连续谱版本的正交归一，对比分立谱： $\langle n \vert m \rangle = \delta_{nm}$ ，连续谱 $\langle x \vert x' \rangle = \delta(x - x')$ 。注意量纲： $\delta(x)$ 带有 $1/[x]$ 的量纲。

## 5. 常用极限表示（窄峰极限）

$$
\delta(x) = \lim_{\epsilon \to 0^+} \frac{1}{\sqrt{2\pi\epsilon}}e^{-x^2/2\epsilon}
= \lim_{\epsilon \to 0^+} \frac{1}{\pi}\frac{\epsilon}{x^2 + \epsilon^2}
= \lim_{K \to \infty} \frac{\sin Kx}{\pi x} .
$$

依次为高斯型、Lorentz 型、sinc（Dirichlet 核）型。

## 6. Kronecker $\delta$ vs Dirac $\delta$

| | Kronecker $\delta_{mn}$ | Dirac $\delta(x)$ |
|---|---|---|
| 变量 | 分立指标 | 连续变量 |
| 配对运算 | 求和 $\sum_n$ | 积分 $\int dx$ |
| 量纲 | 无量纲 | $1/[x]$ |
| 出现处 | 分立基正交归一 | 连续基正交归一 |

## 相关

- 特殊函数正交归一关系里的 $\delta_{mn}$ 见 [Hermite equation](../special_functions/Hermite%20equation.md)（Kronecker 情形的实例）。
- 后续格林函数笔记（有内容时再建目录）会以本页为前置。
