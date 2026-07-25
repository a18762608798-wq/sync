# Associated with Legendre's equation

## Legendre's equation

### In math

* Equation(2,1,0)

$$
\frac{d}{dx}[(1-x^2)\frac{dy}{dx}]+\lambda y=0\quad(|x|\leq1)
$$

* Solution

$$
u=C_1y_1(x)+C_2y_2(x)
$$

* Divergent behavior

$$
u_1(1),u_2(1)\rightarrow\infty\quad(必然发散，需要截断)\\
$$

### In physics: Legendre's polynomial

* Introductory

In anticipation for being limiting when $x= 1$ , we must truncation the $y_1$ or $y_2$, then make $C_2=0$ or $C_1=0$.

* Truncation condition

$$
\lambda=l(l+1)(l\in N)
$$

When $n\in 2N$, $y_1$ is truncated to a polynomial; When $n\in2N+1$, $y_2$ is truncated to a polynomial.

* Simplified form

We always make the **top coeffient is $C_l=\frac{(2l)!}{2^l(l!)^2}$**

Then Legendre polynomial cound be turned to a simplified form:

$$
P_l(x)=\frac{1}{2^ll!}\frac{d^l}{dx^l}(x^2-1)^l
$$

* Property

$$
\begin{cases}
P_l(-x)=(-1)^lP_l(x)\\
\int_{-1}^1P_l(x)P_{l'}(x)dx=\frac{2}{2l+1}\delta_{ll'}
\end{cases}
$$

## Associated with Legendre's equation

### In math

* Equation

$$
\frac{d}{dx}[(1-x^2)\frac{dy}{dx}]+(\lambda-\frac{m^2}{1-x^2}) y=0\quad(m\leq l,|x|\leq1)
$$

### In physics

* Introdution

All truncations are similar as Legendre's polynomial

* Simplified form

$$
P^m_l(x)=(1-x^2)^{m/2}\frac{d^m}{dx^m}P_l(x)
$$

* Property

$$
\begin{cases}
P_l^{-m}(x)=(-1)^m\frac{(l-m)!}{(l+m)!}P_l^m(x)\\
\int_{-1}^{+1}P_l^mP_k^mdx=\frac{(l+m)!}{(l-m)!}\frac{2}{2l+1}\delta_{kl}
\end{cases}
$$

