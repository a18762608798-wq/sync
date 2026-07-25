# the Foundational Rrles of Particle

## Chapter $\S 1$: the Phoronomics of Particle

### $\S1.1$ Polar coordinates

* the establishment of basic vector 

$$
\hat e_r \times \hat e_\theta\rightarrow out\quad to\quad the\quad paper\\
\hat e_r \cdot\vec r>0
$$

* Velocity 

$$
\vec v=\frac{dr}{dt}\hat e_r+wr \hat e_\theta
$$

* Acceleration

$$
\vec a=(\frac{d^2r}{dt^2}-w^2r)\hat e_r+(2\frac{dv}{dt}w+r\frac{d^2\theta}{dt^2})\hat e_\theta
$$

### $\S1.2$ Intrinsic coordinates

* the establishment of basic vector

$$
\hat e_t \times \hat e_n\rightarrow out\quad to\quad the\quad paper\\
\hat e_n\cdot\vec r<0
$$

* Velocity

$$
\vec v=v\hat e_t\\
$$

* Acceleration

$$
\vec a=\frac{dv}{dt}\hat e_t+\frac{v^2}{R}\hat e_n\\
R=\frac{ds}{d\theta}
$$

<!--R is the radius of curvature-->

### $\S1.3$ The transform of coordinates

$$
\vec a=\vec a_{相对}+\vec a_{牵连}+\vec a_{其他}
$$

这里 $\vec a$ 一般是惯性系下加速度，$\vec a_{相对}$ 是非惯性系下的加速度，$\vec a_{牵连}$ 是非惯性系和惯性系之间的相对加速度，$\vec a_{其他}$ 是交叉项。<!--这主要服务于后面的惯性力证明，是一个经典的伽利变换。-->

以经典的匀速转动的坐标系为例,我们干脆放非惯性系里面说。



## Chapter $\S 2$: 观察者惯性系

需要注意的是，牛顿三定律规定<font color=red>观察者惯性系</font>

#### $\S2.1$ The defination of mass

以惯性（牛二）或者引力定标两种方式，后面可以用扭称实验验证二者正比，但是其物理机制永不相同。

#### $\S2.2$ 牛三问题

<font color=red>牛三是动量和角动量守恒的反应。在牛顿定律中确实有其独立的一部分。具体体现在牛二是时间和空间的平移对称性（即规则不依赖于具体时间点和位置），而牛三是空间平移和旋转对称性上。二者不是包含关系。</font>；此外牛三是机械运动结果，牵扯到机械动量不等于正则动量的时候会失效

* 相互作用一定是==相同性质==的力。<!--后两点才有问题，第一点比较新颖-->
* 作用力和反作用力的物体不同。<!--此点为什么有问题应该指交换的玻色子是同一施力物体-->
* 相互作用同时。

#### $\S2.3$ 张力

* 对于轻质绳子，加速度为0，张力在=无摩擦时处处相等。
* 对于非轻质绳子，==张力对于同一子微元作用方向相反==。

## Chapter $\S 3$: 观察者非惯性系

常见非惯性系的惯性力，是一种**等效原理**的思想引入，在形式上也较为简便。

### $\S 3.1$ 非惯性系

* General rules

$$
\begin{cases}
\vec F=m\vec a\\
\vec F+\vec F_{惯性}=m\vec a_{相对}\\
\vec F_{惯性}=\vec{F}_{牵连}+\vec F_{其他}
\end{cases}
$$

* 加速平动非惯性系

$$
\vec F_{惯性}=-m\vec a_{牵连}\\
$$

注意换到标量方程中的方向问题。未知力要在任一套假设方向组合下列方程。

* 匀角速转动非惯性系 

$$
\begin{cases}
\vec F_{惯}=\vec F_{离心}+\vec F_{科氏}\\
\vec F_{离心}=-\vec w\times(\vec w\times \vec r)=mw^2r\hat e_r\\
\vec F_{科氏}=2m\vec v_{相对}\times\vec w
\end{cases}
$$

> 这里的 $\vec w\times \vec r$ 就是牵连速度。

### *3.2 引力质量和惯性质量

* 从物理属性来看，引力质量和惯性质量毫不相干。但是从实验来看，==引力质量和惯性质量成正比==。

* 目前的质量体系（以及SI）本质上是由惯性质量定义的。以**G调节使得 $m_{引}=m_{惯}$** 。

* 由此我们无法分辨引力惯性力之区别，有==等效原理==。

