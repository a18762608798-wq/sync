# Bessel Equation(只有它没有截断条件)

## Bessel Equation

* Equation(0,-1,-2)

$$
\frac{d^2y}{dz^2}+\frac{1}{z}\frac{dy}{dz}+(1-\frac{\upsilon^2}{z^2})y=0\quad(|argz|<\pi)
$$

* Solution

The solution have 3 varieties to adapt many limiting behaviors

1. If $\upsilon\neq Z$ :

$$
y=C_1J_\upsilon(z)+C_2J_{-\upsilon}(z)
$$

**$J_v$ is be called as 'Bessel Function'.**

2. If $\upsilon= Z$ , $J_\upsilon$ and $J_{-\upsilon} $ are linear correlation.（**Then $J_{|m|}(z)$ could be employed if there is only a bound condition**)

$$
y=C_1J_\upsilon(z)+C_2N_\upsilon(z)
$$

**$N_\upsilon$ is be called as 'Neumann Function'. （诺伊曼）**

3. beyond these, we cound employ the linear combine of $J_\upsilon$ and $N_\upsilon$

$$
y=C_1 H_\upsilon^{(1)}+C_2H_\upsilon^{(2)}
$$

$H_\upsilon^{(1)}$ and $H_\upsilon^{(2)}$ and dependent, **which are called as 'Hankel function' (汉克尔)**

* Divergent behavior

Unusually, when $\upsilon\in\mathbb{Z}$

$$
\begin{cases}
J_0(0)=1\\
J_n(0)=0\quad(n\ge1)\\
J_n(\infty)=0
\end{cases}
$$

## Variant Bessel Equation

* Equation

$$
\frac{d^2y}{dx^2}+\frac{1}{x}\frac{dy}{dx}+(1-\frac{\upsilon^2}{x^2})y=0\quad(x\quad is \quad real)
$$

* Solution

1. When we make z=ix, and $\upsilon\neq Z$, this equation cound be regressed to Bessel equation

$$
y=C_1J_\upsilon(ix)+C_2J_{-\upsilon}(ix)
$$

2. However, we desperate to get a real solution when $\upsilon=Z$，so we make **variant Bessel function $I_\upsilon$** , when $\upsilon\neq Z$

$$
y=C_1I_\upsilon(x)+C_2I_{-\upsilon}(x)
$$

3. So when $\upsilon=Z$,

$$
y=C_1I_\upsilon(x)+C_2K_\upsilon(x)
$$

* Divergent behavior

1. $x\rightarrow \infty$

$$
\begin{cases}
I_\upsilon(x)\propto\frac{e^x}{\sqrt x}\\
K_\upsilon(x)\propto\frac{e^{-x}}{\sqrt x}
\end{cases}
$$

2. $x\rightarrow 0$

用了再写

## Spherical Bessel equation (Always text it)

### In math

* Equation

$$
\frac{d^2y}{dx^2}+\frac{2}{x}\frac{dy}{dx}+[1-\frac{l(l+1)}{x^2}]y=0\quad(l\in N)
$$

Let $y(x)=\frac{1}{\sqrt x}\upsilon(x)$, we can get:

$$
\frac{d^2y}{dx^2}+\frac{1}{x}\frac{dy}{dx}+[1-\frac{(l+1/2)^2}{x^2}]y=0\quad(l\in N)
$$

* Solution

Evidently,the solution of $\upsilon(x)$ is the solution of $l+1/2$ order Bessel equation, for instance(we have meet the condition $l+1/2\neq Z$)

$$
y(x)=\frac{1}{\sqrt x}\upsilon(x)=C_1\frac{1}{\sqrt x}J_{l+1/2}(x)+C_2\frac{1}{\sqrt x}J_{-l-1/2}(x)
$$

Tend to this solution, we also put forward a number of new basic function, **we can use any 2 vectors to add.**

$$
y(x)=j_l(x),n_l(x),h_l(x),h_l^*(x)
$$

### In physics

* Simplified form

$$
\begin{cases}
j_l(x)=(-1)^lx^l(\frac{1}{x}\frac{d}{dx})^l\frac{\sin x}{x}\\
n_l(x)=(-1)^{l+1}x^l(\frac{1}{x}\frac{d}{dx})^l\frac{\cos x}{x}\\
h_l(x)=-i(-1)^l(\frac{1}{x}\frac{d}{dx})^l\frac{1}{x}\exp(ix)

\end{cases}
$$

* Divergent behavior($l$ have be $\mathbb Z$)

$$
j_l(0)\rightarrow0\\
$$

1. $x\rightarrow i\infty$

$$
\begin{cases}
h_l(x)\rightarrow\frac{C}{x^{l+1}}
\end{cases}
$$

**so we always use $j_l,h_l$ in physics**

* Different

$$
\frac{d}{dr}[r^{l+1}j_l(r)]=r^{l+1}j_{l-1}(r)
$$
