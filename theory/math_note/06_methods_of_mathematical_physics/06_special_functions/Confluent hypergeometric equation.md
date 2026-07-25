# Confluent hypergeometric equation

## In math

* Equation(110)

$$
z\frac{d^2y}{dz^2}+(\gamma-z)\frac{dy}{dz}-\alpha y=0
$$

* Solution

Basic solutions

$$
\begin{cases}
y_1=F(\alpha,\gamma,z)\\
y_2=z^{1-\gamma}F(\alpha-\gamma+1,2-\gamma,z)
\end{cases}
$$

Then The solutions

$$
\begin{cases}
C_1y_1+C_2y_2\quad\gamma\neq \mathbb{Z}\quad 谐振子径向，y_2用不上\\ 
Cy_2 \quad\gamma=-N, \neg((\alpha\geq\gamma)\vee(\alpha\in -\mathbb{N}))\\
Cy_1=Cy_2\quad \gamma=1\\
Cy_1\quad\gamma\geq2,\gamma\in \mathbb{Z} \quad氢原子径向
\end{cases}
$$

* Divergent behavior

$$
\begin{cases}
y_1(z\rightarrow \infty)\propto e^z\quad(必然发散，需要截断)\\
y_2(z\rightarrow 0)\propto r^{-2l-1} 这个一般不被Schrodinger接受
\end{cases}
$$

## In physics

* Truncation condition

$$
\alpha\in-\mathbb{N}
$$
