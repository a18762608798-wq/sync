# Chapter 1 静电场和恒流场

*  Foundation：库仑定律

$$
\vec F=\frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r^2}\hat e_r
$$

## $\S 1.1$ 静电场

### $\S 1.1.1$ 电场

* 点电荷

$$
\vec E=\frac{1}{4\pi\varepsilon_0}\frac{q_1}{r^2}\hat e_r
$$

* 可有源，无旋场性质。

$$
\begin{cases}
\Phi_E=\oiint_{s}\vec E\cdot d\vec S=\frac{q}{\varepsilon_0}\\
\oint \vec E\cdot dl=0
\end{cases}
$$

这里高斯定理可从立体角和点电荷电场证得：$d\Phi_s=\vec E\cdot d\vec S=\frac{q}{4\pi\varepsilon_0}\frac{\hat e_r}{r^2}\cdot d\vec S=\frac{q}{4\pi\epsilon_0}d\Omega$，其中$d\Omega$球面曲率为$4\pi$

### $\S 1.1.2$ 电势场

* 直接定义

$$
\begin{cases}
\vec E=-\nabla\varphi\\
U_{ab}=\varphi(a)-\varphi(b)=\int_a^b\vec E\cdot d\vec l
\end{cases}
$$

显然此为标量场，由此电场无旋。<font color=red>注意dl有方向，在平行版电容器里更甚。</font>

* 点电荷

$$
\varphi(r)=\frac{1}{4\pi\varepsilon_0}\frac{q}{r}\quad[\varphi(+\infin)\rightarrow 0]
$$

* Energy

1. 电势能

$$
W_{ab}=q[\varphi(a)-\varphi(b)]=qU_{ab}
$$

意为A到B点电场力所做功。

2. 静电能

互能：对于电荷组

$$
\begin{cases}
W_{i}=\frac{1}{2}\sum_{i=1}^nq_iU_i\\
U_i=\sum_{j=1}^n' \frac{1}{4\pi\varepsilon_0}\frac{q_i}{r_{ij}}
\end{cases} 总
$$

总能量：对于连续带电导体。<!--当然若只有一个带电体，自然是自能。-->
$$
W_e=\frac{1}{2}\int{dqU}
$$


### $\S 1.1.3$ 静电场应用

#### $\S 1.1.3.1$ 电偶极子

* 受力

$$
\begin{cases}
 均匀场：\quad \vec L=\vec P\times\vec E \\
 非均匀场：\quad \vec F=-\nabla(\vec P\cdot \vec E)
\end{cases}\\
$$

其中，偶极子 $\vec P=q\vec l$, 均匀场力矩可由质心系易得。

* 电势

一般取0阶，==注意别忘了非r向的电场。==

#### $\S 1.1.3.2$ 电容

* Definition

$$
C_{AB}=\frac{q_A}{U_A-U_B}
$$

<font color=red>严格的电容处于静电屏蔽之中，B的内表面带电由A确定。</font> 唯一性定理由于 $q_A、q_B$ 确定，**$U_A-U_B$ 是固定**的。

* 能量

$$
W_e=\frac{1}{2}QU=\frac{1}{2}CU^2
$$

由静电能易证。

* 重要应用：平行板

不严格的电容。

1. ==注意和均匀无限大平板不同，这个是导体。利用导体bound condition==

2. <font color=red>但是可以把单个表面任然当作无穷大，6。</font>
3. <font color=red>无论平行板中间放不放介质，C都是很好求的，可以先求这个</font>

#### $\S 1.1.3.2$ 静电场导体

* **静电平衡**

<span style="color:lime"> $\sigma$ 相同导体为等势体；内部场强为0；电场线垂直表面；静电荷只在表面（空腔只在外表面）。</span>

* Boundary

$$
\vec E=\frac{\sigma_e}{\varepsilon_0}
$$

只有上面一个面有场强，有散场高斯即可。

>  <span style="color:magenta">此结论所得电场是近导体表面的绝对电场, 不参与其他电场叠加。它的条件是恒满足的。</span>
>
> 而无穷大平面的条件可以叠加原因是对称性条件破坏但是平面电荷分布无影响。

* 静电屏蔽

1. 导体腔内部无带电体。

显然高斯内部无电荷。

2. 有带电体。<!--导体唯一性定理-->

若壳不接地，腔内带电体对外无影响；（内空间电荷固定）

若壳接地，腔内外互不影响；（壳电势固定，带电体电量固定）

## $\S 1.2$ 恒流场

* Foundation

1. 电荷守恒和恒流要求

$$
\begin{cases}
\oint \vec j\cdot d\vec S=-\frac{dq}{dt}=0
\end{cases}
$$

恒流电荷分布不能变化，否则电场变化影响电流恒定。

2. 电流密度矢量

$$
dI=\vec j\cdot d\vec S
$$

* 微分欧姆定律

$$
\vec j=\sigma \vec E
$$

<!--这里有j和E同向。这没有理论证明，大概是若不平衡会导致静电荷累积强制平衡。-->

* 补充

1. 电源内部非电场力做功

$$
\vec j=\sigma(\vec K+\vec E)
$$

2. 恒流导线净电荷问题<!---要求sigma处处相等，即均匀导体-->

$$
\oint \vec j\cdot d\vec S=\oint\sigma\vec E\cdot d\vec S=0
$$

若 $\sigma$ 为常数，又因为$\oint\vec E\cdot d\vec S=\frac{q}{\varepsilon_0}$ ,说明恒流均匀导体内部无电荷，都在表面上。<font color=red>注意不是电流，电流均匀分布，是净电荷</font>

## $\S 1.3$ 电动力学衔接

### $\S1.3.1$ ==导体真空唯一性定理==

#### $\S 1.3.1.1$ 物理上

除导体的空间信息外，只需要<font color=lime>指定导体组的一组电势或带电量混合条件，空间电场分布唯一</font>。

<span style="color:magenta">更广泛而且准确的说，对于**某个**相同的**闭合区域**边界条件，标量场分布唯一</span>

* 引理:

1. 无源空间无极值。（极值一定为源或汇）
2. 等势边界导体包围空间也等势。（由1可得，无极值。）
3. 所有导体边界不带电，空间和边界等势。（若有不等势，最高电势导体必然为源，与条件相左）
4. 对于全0边界条件，导体混合边界条件和等势没有区别。

<!--对于混合边界条件，假设电势不相等，一定有最高电势者为源。由于部分导体无带电量，必然不为源，只能是有电势边界者为源。由因为源导体等势，互相之间没有电场线，只能是带电量为0者为汇。到现在就明显了，整体看带电量者只能为汇而非源，说明其必然带负电荷。与该些导体不带电向左。-

* 构造假设。

1. 假设对于同一组边界，我们知道若干个电量$Q_{n_i}$和若干个电势$U_{n_j}$作为边界条件。

2. 假设对于此边界条件，有两个不同的空间电势分布解 $\phi_1$， $\phi_2$，**由电场电势的叠加性，必然有解 $\phi=\phi_1-\phi_2$ 也符合此边界条件的叠加：也即：$Q_{n_i}=0,U_{n_j}=0$**

由此有分布$\phi$，边界条件对于部分导体电势为0，部分导体带电量为0；显然target: $\phi=constant$

* 证明：

显然若全部边界电势为0, 引理2空间$\phi=0$ ；若全部带电量为0，引理3等势也可证明（但不一定是0了）；对于全0边界条件，导体混合边界条件和边界电势为0没有任何区别，引理4可证。

* 结论

**对于同一组导体边界条件，其势能分布只能相同或者差一个常数。**

#### $\S 1.3.1.2$ 数学上

对于通解。

* 构造假设。

1. 假设对于同一组边界，我们知道若干个电势$\phi_{n_i}$和若干个电势梯度$\partial_{nj} H_{n_j}$作为边界条件。

2. 假设对于此边界条件，有两个不同的空间电势分布解 $\phi_1$， $\phi_2$，**由电场电势的叠加性，必然有解 $\phi=\phi_1-\phi_2$ 也符合此边界条件的叠加：也即：$\phi_{n_i}=0,\partial_{n_j} H_{n_j}=0$**

由此有分布$\nabla^2\phi=0$，边界条件对于部分导体电势为0，部分导体边界磁场梯度为0；显然target: $\phi=constant$

$$
0=\int\nabla^2 \phi dV=\oint_n\partial_n\phi dS
$$

<font color=red>待证</font>

这里只给拉普拉斯即无源区域，泊松可拆分为特解和通解，关注通解即可。

对于有界区域对于标量场的拉普拉斯方程，给定边界的函数值$\phi_n$或者法向梯度$\nabla_r\phi$，区域解唯一。

证明：假设有两个解，可构造$u=\phi_1-\phi_2$，由于线性关系，满足$\nabla^2 u=0$；又因为边界条件完全相同，也即$u_n$和$\nabla_ru$ 为0，其中又有$0=\int\nabla^2 udV=\int_n\partial_nudS_1$,意味着边界上u为常数，这里直接全是0；又根据**迪里克雷条件**<!--这是个假设，要边界平滑，区域内无源-->，<font color=red>通解</font>在内部不能取极大极小，也即u恒为0。

2. usage

如电像法。

#### $\star$ 1.3.1.3 Cases

<span style="color:orange">对于真空中导体球，半径为R，带电为 $q_0$ ；距离r处(r>R)，有点电荷 $q$ 求空间电荷分布</span>

构建相同边界条件。$q'$于球内使r=R处$\varphi=0$ 

综上对于r>R有等效分布：$q',q_0-q',q$

### $1.3.2$* 导体边界问题

1. content

$$
\begin{cases}
(\vec j_1-\vec j_2)\cdot \vec n=0\\
(\vec E_1-\vec E_2)\times\vec n=0
\end{cases}
$$

表导体**恒流**电流法向不变，电场切向不变。以电流恒流无旋和电场无旋证之。

2. 恒流电流界面折射

$$
\frac{\sigma_1}{\sigma_2}=\frac{\tan\theta_1}{\tan\theta_2}
$$

除边界条件，还需$\vec j_i=\sigma_i\vec E_i$

