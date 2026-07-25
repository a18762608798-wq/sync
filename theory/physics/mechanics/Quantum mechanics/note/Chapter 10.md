# $\S10$ The Algebraic Solution of the Eigenvalue of Mechanical quantities

## $\S10.0$ Harmonic oscillator

### $\S10.0.0$ premise

As a matter of fact, we have know the properties of *Hermite polynomial*
$$
H_{n+1}(x)-2xH_n(x)+2nH_{n-1}(x)=0
$$

### $\S10.0.1$ <font color=red>Definition</font>

<font color=red> Natural system of units </font>
$$
\begin{cases}
\hat a^+=\frac{1}{\sqrt 2}(x+i\hat p)\\
\hat a=\frac{1}{\sqrt 2}(\hat x+i\hat p)\\
\hat N=a^+a
\end{cases}
$$
Therefrom, $\hat H=\hat N+\frac{1}{2}$

### $\S10.0.2$ properties

* commute: <font color=orange>$[a,a^+]=1$</font> $\rightarrow[\hat N,\hat a^+]$;

* $\hat N$
1. $\langle \hat N\rangle\ge 0$, 即<font color=orange>正定</font>
2. $\hat N$ is a Hermite operator
3. <font color=orange>$Na|{n}\rangle=(n-1)a|{n}\rangle; Na^+|{n}\rangle=(n+1)a^+|{n}\rangle$</font>

### $\S10.0.3$ Output the function of harmonic oscillator

* Primal state is <font color=red>$|{0}\rangle$</font>, <font color=orange>$a|{0}\rangle=0$</font>
* <font color=red>$|{n}\rangle=\frac{1}{\sqrt n}(a^+)^n|{0}\rangle\quad n\in \N$</font>, turn the operator $\hat a^+$ to x representation. 

### $\S10.0.4$ 延拓

对于幺正变换的$\hat H$，一般对$\hat a、\hat a^\dagger$ 进行线性构造，达到：
$$
\begin{cases}
\hat b=C_1 \hat a+C_2\hat a^\dagger+C_3\\
\hat H=K \hat b^\dagger \hat b+C_4\\
[\hat b,\hat b^\dagger]=1
\end{cases}
$$
针对$\hat H$具体形式决定具体参数取值。<span style="color:magenta">理论上是可以构造非整数占据数表象，但是一般没人用。</span>

## $\S10.1$ the General Properties of Angular Momentum

### $\S10.1.0$ premise

the general properties of angular momentum(<font color=blue> Natural system of units </font>)

$$
\begin{cases}
[j_\alpha,j_{\beta}]=i\epsilon_{\alpha\beta\gamma}j_\gamma\\
[j^2,j_\alpha]=0
\end{cases}
$$

which meaning the <font color=red>representation we will deploy is $[j^2,j_\alpha],viz.,|{j m}\rangle$</font>

### $\S10.1.1$ <font color=red>definition</font>

$$
\begin{cases}
j_+= j_x+ij_y\\
j_-=j_x-ij_y=(j_+)^+
\end{cases}
$$

### $\S10.1.2$ <font color=orange>commute for selection rule</font>

* Single bite

$$
\begin{cases}
[j^2,j_\alpha]=0\\
[j_z,j_{\pm}]=\pm j_{\pm}
\end{cases}
$$

therefrom we can put up <font color=orange>selection rules</font>:
$$
\begin{cases}
\bra{j'm'}j_\alpha\ket{\lambda m}=\delta_{j'j}\bra{j m'}j_\alpha\ket{j m}\\
\bra{j'm'}j_\pm\ket{j m}=\delta_{j'j}\bra{j m'}j_\pm\ket{j m}=\delta_{jj'}\delta_{m'm+1}\bra{j m+1}j_\pm\ket{j m}\\
\end{cases}
$$
Add the rules of $[j^2,j_\alpha]$
$$
\bra{j'm'}j^2\ket{jm}=\lambda\delta_{jj'}\delta_{m,m'}\\
\bra{j'm'}j_z\ket{jm}=m\delta_{jj'}\delta_{m,m'}
$$

* Double bites

$$
[J_z,j_{1\alpha}]
$$

### $\S10.1.3$ <font color=orange>general rules of angular momentum</font>

#### 10.1.3.1 The limit of angular quantum number

$$
|m|\begin{cases}
\le j\\
\in \N
\end{cases}\\
j=\begin{cases}
\N
\quad Bose\\
\N+\frac{1}{2}\quad Femi
\end{cases}
$$

#### 10.1.3.2 matrix elements

<font color=red>$|\epsilon_m|^2=|\langle {jm+1}| j_{+}|{jm}\rangle|^2=\lambda-m(m+1)$</font>, also $(j_{+})^+=j_{-}\Rightarrow (j_+)^\dagger_{m-1m}=(j_+)^*_{mm-1}=(j_-)_{m-1m}$

Viz.,<font color=magenta>assign phase 0</font>

$$
\begin{cases}
\bra{jm+1}j_+\ket{jm}=\sqrt{\lambda-m(m+1)}\\
\bra{jm-1}j_-\ket{jm}=\bra{jm}j_+\ket{jm-1}\\
\end{cases}
$$

Explasion, we could gain $j_{\pm},j_x,j_y$ matrix elements

说明: 这章的矩阵元喜欢降序, 一者是和 $\sigma_z$ 对应, 二者是和 "上升, 下降" 之意对应.

#### 10.1.3.3 Other properties

* <font color=lime>To **primal state $|\lambda m_z\rangle$**, measure $\hat j_x,\hat j_y$ , the probability of getting $m_x$ and $-m_x$ are equal.</font>

> Basic on $\langle jm_z|j_x^{2k+1}|jm_z\rangle=0$
>
> * If $ m_x, m_z\in \Z$, 
>
> construct :
>
> $$
> f(\hat j_x)=\hat j_x(\hat j_x^2-1^2)(\hat j_x^2-2^2)...[\hat j_x^2-({m_x'}-1)^2][\hat j_x^2-({m_x'}+1)^2]...(\hat j_x^2-j^2)
> $$
>
> <font color=magenta>$Viz.,$ where is no term of $\pm m_x'$</font>, evidently,
> $$
> \begin{cases}
> f(m_x')+f(-m_x')=0\\
> f(m_x)=f(m_x)\delta_{m_x,\pm m_x'}
> \end{cases}
> $$
>
> therefore :
> $$
> \langle j m_z|f(\hat j_x)|jm_z\rangle=\sum_{m_x}\langle jm_z|f(\hat j_x)|jm_x\rangle\langle jm_x|jm_z\rangle =\sum_{m_x} f(m_x)P(m_x)\\
> =f(m_x')P(m_x')+f(-m_x')P(-m_x')=f(m_x')[P(m_x')-P(-m_x')]=0\\
> \Rightarrow P(m_x')=P(-m_x')
> $$
>
> * If $\hat m_x\in \Z/2$
>
> construct :
> $$
> \hat j_x(\hat j_x^2-(\frac{1}{2})^2)(\hat j_x^2-(\frac{3}{2})^2)...[\hat j_x^2-({m_x'}-1)^2][\hat j_x^2-({m_x'}+1)^2]...(\hat j_x^2-j^2)
> $$
> Proof similarly for the following.

## $\S 10.2$ The coupling angular momentum

* CG coefficient

The representation transform of $|{j_1m_1j_2m_2}\rangle$ product state and $|{j_1j_2JM}\rangle$ coupling state. 

* <font color=orange>The relationship between quantum numbers of $\hat J=\hat j_1+\hat j_2$</font>

$$
\begin{cases}
J\ge|j_1-j_2|\\
J\le j_1+j_2 
\end{cases}
$$
