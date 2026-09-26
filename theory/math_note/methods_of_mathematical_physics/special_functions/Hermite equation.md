# Hermite equation

## In math

* Equation(0,1,0)

$$
\frac{d^2u}{dx^2}-2x\frac{du}{dx}+(\lambda-1)u=0\\
$$

* Solution

$$
u=C_1u_1(x)+C_2u_2(x)
$$

* Divergent behavior

$$
u_1(\infty),u_2(\infty)\rightarrow e^{x^2}\quad(必然发散，需要截断)\\
$$

## In physics: Hermite polynomial

* Introductory

In anticipation for limitation  [compare with $e^{-\frac{1}{2}x^2}$]  when $x\rightarrow\infty$ , we must truncation the $u_1$ or $u_2$, then make $C_2=0$ or $C_1=0$.

* Truncation condition

$$
\lambda-1=2n(n\in N)
$$

When $n\in 2N$, $u_1$ is truncated to a polynomial; When $n\in2N+1$, $u_2$ is truncated to a polynomial.

* Simplified form

We always make the **top coeffient is $C_n=2^n$**

Then Herimite polynomial cound be turned to a simplified form:

$$
H_n(\varepsilon)=(-1)^ne^{x^2}\frac{d^n}{dx^n}e^{-x^2}
$$

* property

$$
\int_{-\infty}^{+\infty}H_mH_ne^{-x^2}dx=N_n^2\delta_{mn}=\sqrt \pi2^n\cdot n!\delta_{mn}
$$
