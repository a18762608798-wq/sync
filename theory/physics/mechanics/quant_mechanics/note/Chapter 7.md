# Chapter 7The movement of particles in electromagnetic field

[toc]

主要还是磁场。

## 7.0 primise

### 7.0.1 Constrction of equation

#### premise and condition

* Canonical equation

$$
\begin{cases}
\frac{d\vec r}{d t}=\frac{\partial H}{\partial \vec P}\\
\frac{d\vec p}{dt}=\frac{\partial H}{\partial \vec r}
\end{cases}
$$

* Lorentz equation

$$
\mu\frac{d^2 \vec r}{dt^2}=q(\vec E+\vec v\times \vec B)
$$

* The standard of electronmagnetic field(**They could do some norm transform**)

$$
\begin{cases}
\vec E=-\frac{1}{c}\frac{\partial A}{\partial t}-\nabla \phi\\
\vec B=\nabla\times \vec{A}
\end{cases}
$$

* Then we always use **Shear wave condition**

$$
\nabla\cdot\vec A=0\rightarrow[\hat P,\hat A]=0
$$

#### Equation

a meeted form:

$$
H=\frac{1}{2\mu}(\hat P-\frac{q}{c}\vec A)^2+q\phi
$$

#### Canonical quantum

$$
\hat P=-i\hbar\nabla
$$

The reason refuse $\mu v=-i\hbar \nabla$

1. Canonical equation
2. **$\nabla\psi$ , $\hat P$ could not be abrupt change with the abrupt change of $\vec A$ ; yet $\mu v$ will be**.

#### Expland

$$
\begin{cases}
\vec{j}=Re(\psi^*\hat v\psi)\\
\mu\hat v=\hat P-\frac{q}{c}\hat A
\end{cases}
$$

### 7.0.2 The conservation of $[H,l^2,l_z]$ with intense magetic field

* Landau energy levels

$$
\begin{cases}
[H,l_z]=w_L[l_z,lz]=0 \\
[H,l]=w_L[l_z,l]=w_L(\hat e_y[l_z,l_x]+\hat e_x[l_z,l_y])=w_L(\hat e_yl_y+-\hat e_xl_x)\ne 0\\
[H,l^2]=l[H,l]+[H,l]l=0
\end{cases}
$$

* Hydrogen

一模一样的多一项 $w_L\hat l_z$

### 7.1 Landau energy levels(without potential field)

#### The construct of magnetic field

When magnetic field is even, $\vec A=\frac{1}{2}\vec B\times \vec r$  could meet $\nabla\times \vec A=\vec B$  and $\nabla\cdot \vec A=0$

$$
A=\begin{Bmatrix}
-\frac{1}{2}B_zy\\
\frac{1}{2}B_zx\\
0
\end{Bmatrix} \quad;B=\begin{Bmatrix}
0\\
0\\
B_z
\end{Bmatrix}
$$

seems to $A=\frac{1}{2}B\times r$ meet $\nabla\times B=A$, $\nabla\cdot A=0$ ,we could assign values for $A$

#### Equation

$$
\frac{1}{2\mu}(\hat P-\frac{q}{c}\vec A)^2\\
=H+\hat T_{canZ}
$$

We just care about the info on x-o-y

$$
\begin{cases}
H=H_0+w_L\hat L_z\\
H_0=\hat T_{can}+\frac{1}{2}Mw_L^2\rho^2\\
w_L=\frac{eB}{2\mu }
\end{cases}
$$

#### Solution

Evidently , The form of $H_0$ is similar as Harmonic oscillator(dim2), The effect of $\hat L_z$ is just a constant.

$$
\begin{cases}
E_N=(N+1)\hbar w_L\quad N\in2\N\\
N=2n_\rho+|m|+m\\
\end{cases}
$$

#### Properties

##### Magnetic moment（存疑)

1. Classic

If the magnetic moment is parallel with magnetic field $B_z$

$$
U=-\vec B\cdot \vec \mu\rightarrow \mu_z=-\frac{U}{B_z}
$$

**However, we use $E_n$ (确实也是z方向的) to replace $U$ (why?????????)**

$$
\mu_z=-\frac{E_z}{B_z}<0\quad(assumeB_z>0)
$$

这是经典的类比，但显然有点问题。关于本征值等效于磁场势能过于粗糙，而且势能零点也不大好解释。

2. Quantum
* 电流

$$
\vec j=-e(\psi^*\hat P\psi+c.c)=\frac{ei\hbar}{2\mu}(\psi^*\nabla\psi-c.c)\\
$$

极坐标下的梯度算符

$$
\nabla=\hat e_\rho\partial_\rho+\hat e_\varphi\frac{1}{\rho}\partial_\varphi
$$

显然只有$j_\varphi$有数值。

$$
\hat j_\varphi=\frac{ei\hbar}{2\mu}\frac{1}{\rho}(\psi^*\partial_\varphi\psi-c.c)=\frac{ei\hbar}{2\mu}\frac{1}{\rho}(im+im)|\psi|^2=-\frac{m\hbar e}{\mu \rho}|\psi|^2
$$

显然磁矩在表像 $[H,l_z]$ 下只在z方向有磁矩。环z电流中心对称$(\varphi)$ ,取带宽$\sigma$ 的圆环,面积为$d\tau$

$$
M=\int S dI=\int\pi\rho^2\cdot j_\varphi d\sigma=-\frac{m\hbar e}{\mu }\int\pi\rho|\psi|^2d\sigma=-\frac{m\hbar e}{2\mu}\int\pi|\psi|^2d\tau=-\frac{\hbar e}{2\mu}m
$$

这个和此问题的$\mu_Z$更无关系。。。我觉得确实应该只有$w_L\hat l_z$这一部分作为势能计算磁矩。

* 简并度

很容易发现，对于有$m\le 0$ ,N是相同的。而在极坐标下，m了无限制，所以对于所有能级简并度为无穷。

显然也可以从构造不对易守恒量说明。

## 7.2 Normal Zeeman effect (with Hydrogen potential field)

要求是**强磁场**，虽然我还不知道为什么。

### The construct of magnetic field

**When magnetic field is even, $\vec A=\frac{1}{2}\vec B\times \vec r$  could meet $\nabla\times \vec A=\vec B$  and $\nabla\cdot \vec A=0$**

$$
A=\begin{Bmatrix}
-\frac{1}{2}B_zy\\
\frac{1}{2}B_zx\\
0
\end{Bmatrix} \quad;B=\begin{Bmatrix}
0\\
0\\
B_z
\end{Bmatrix}
$$

### Equation

弃除相对小量（$B^2$项一般能量很小,而且是纠缠项，不要了）

$$
\begin{cases}
\frac{1}{2\mu}(\hat P-\frac{q}{c}\vec A)^2+V(r)\approx H_{Hyd}+w_L\hat l_z\\
w_L=\frac{eB_z}{2\mu}
\end{cases}
$$

### Solution

Evidently , The form of $H_0$ is similar as Hydrogen(dim3), The effect of $\hat L_z$ is just a constant(m).

$$
E_{n_rlm}=E_{n_rl}+m\hbar w_L\\
$$

### Properties

* 强磁场下能谱分裂。

Evidently, if we add a intense magnetic field, The levels for $E_{n_rlm}$ will be devided into $(2l+1)$ parts

For any 能谱 into any two eneray levels $(E_{n_rl})$ has similar effect，而且分裂相差频率恰好为$mw_L$

* 磁矩

实际上算过了$[H,\hat l^2,\hat l_z] $ 下

$$
M_z=-\mu_Bm=-\frac{\hbar e}{2\mu}m
$$

而且参考共线时磁矩势能$U=-\vec \mu_z\cdot \vec B_z=-\mu_zB_z\rightarrow\mu_z=-\frac{U}{B_z}$

显然作用能量为$w_L\hat l_z$

$$
\mu_z=-\frac{U}{B_z}=-\frac{e}{2\mu}\hat l_z
$$

对应$\hat l_z=m\hbar$
