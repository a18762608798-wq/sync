# A-B效应

## 现象：

​	双缝干涉外区域的磁分布影响双缝干涉图案(平移效果)。猜测$\vec{A}$有意义。

## 证明

### 准备

* 拉格朗日：$\frac{d}{dt}(\frac{\part L}{\part q'})-\frac{\part L}{\part q}=0$, $L=T-V$
* 哈密顿量：$\vec{H}=\vec{P}\cdot\vec{v}-L$

* 运动方程：$\frac{d\vec{P}}{dt}=q(\vec{E}+\vec{v}\times \vec{B})$

### 正文

* 目标是把运动方程和$\vec{A}$，$\psi$有关系。由$B=\nabla\times A$，$\nabla\times E_D=-\frac{\part B}{\part t}=-\nabla\times\frac{\part A}{\part t}$

因此$E=\nabla \psi-\frac{\part A}{\part t}$，即静电场和动生电场之和。

也即$\frac{d}{dt}(\vec{P}+q\vec{A})=-q\nabla(\psi-\vec{v}\cdot\vec{A})$

* 单粒子拉格朗日量$L=T-V=\frac{1}{2}m\vec{v}^2-(q\psi+q\vec{v}\cdot\vec{A})$

也即$\vec{P}=\frac{\part L}{\part \vec{v}}=m\vec{v}+q\vec{A}=\vec{p}+q\vec{A}$

* 哈密顿量$H=\frac{\vec{p}^2}{2m}+V=\frac{{(\vec{P}-q\vec{A})}^2}{2m}+V=\frac{(-ih\nabla-q\vec{A} )^2}{2m}+V$

  满足$H\Phi=ih\frac{\part\Psi}{\part t}$<!--????薛定谔-->

​		相对于$\vec{p}$即未有$A$的薛定谔方程有
$$
\Phi=e^{ig(r)}\phi\\
g(r)=\frac{q}{h}\int_0^rA(\vec{r'})d\vec{r'}
$$
可见$A$的作用是对$\phi$平移一个相位。
