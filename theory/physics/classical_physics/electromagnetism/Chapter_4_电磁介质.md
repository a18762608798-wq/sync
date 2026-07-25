# $\S4$ 电磁介质

## $\star$ 4.1 电介质

### $\S 4.1.1$ 极化

* **极化强度**

有感应电场<!--多数反向，但不一定-->产生，也即
$$
\vec E=\vec E_0+\vec E_p
$$

1. 定义式子

$$
\vec P=\frac{\sum p_{分子}}{\Delta V}=nq_+\vec l=\rho_e\vec l
$$

> <span style="color:orange">这东西还挺有用。</span>

2. 常见的线性介质

$$
\vec P=\chi_e\varepsilon_0\vec E
$$

<span style="color:magenta">注意是和最终电场呈线性关系，而不是外加电场$E_0$</span>

3. 极化电荷

面电荷有高斯关系，显然
$$
\nabla \cdot\vec P=-\rho_p
$$
界面上的面电荷是其特例。
$$
\vec P\cdot \vec n=\sigma_p'
$$
<span style="color:magenta">显然这里的 $\sigma_p'$ 不是传统的介质内极化电荷导致的，而是伸出界面的极化电荷。</span>

> 取界面附近，单种物质的小圆柱，满足关系：
> $$
> \oint \nabla \cdot \vec P dV=\int \vec P\cdot d\vec S=\int-\rho_p dV=-\int \sigma_p \cdot dS\\
> \Rightarrow Let\quad  \sigma_p'+\sigma_p=0
> $$
> 

### $4.1.2$  电位移

* 定义

$$
\vec D=\varepsilon_0\vec E+\vec P=(1+\varepsilon_r)\varepsilon_0\vec E
$$

这个加法没啥逻辑，是极化强度高斯和电场高斯的结果。

* maxswell equation

$$
\begin{cases}
\nabla\cdot\vec D=\rho\\
\nabla\times\vec E=0
\end{cases}
$$

散度由电位移定义方式可得。此处书上明确说$\nabla\times \vec D\neq 0$，甚至铁电体里面方向都不同，<font color=orange>说明 $E_p$不一定和$E_0$ 称常线性关系</font>

* 边界关系

$$
\begin{cases}
(\vec D_2-\vec D_1)\cdot\vec n=\sigma_e\rightarrow 0\\
(\vec E_2-\vec E_1)\cdot \vec n=0
\end{cases}
$$

这显然是两个maxswell关系在边界应用得到的。==第一式取0因为单电介质理论上没有自由电荷。==

### $\S 4.1.3$  介质电场能量  

* 电场能量密度定义

$$
w_e=\frac{1}{2}\vec D\cdot \vec E
$$

> <font color=magenta>这里的能量密度必须对全空间而言才有意义。</font>

书上以平行板能量得到，其能量分布均匀。

<font color=red>注意平行板介质体系能量变化</font> ：

该体系元素有：电源、极板、介质。设电源能量做功$\Delta E$，静点势能为 $W_e$，对介质做功为 $A$
$$
\begin{cases}
\Delta E=\Delta Q *U\\
\Delta E=\Delta W_e+A\\
\hat F=-\nabla W_e
\end{cases}
$$

* properties:

1. <font color=orange>这个能量密度的积分和自能加互能或者说$W_e=\int_v \frac{1}{2}\rho \phi dV$得到的结果相同</font>

2. 事实上严格证明就是

$$
W_e=\int \frac{1}{2}(\nabla\cdot \vec D)\phi dV=\frac{1}{2}\int [∇⋅(ϕD)−D⋅∇ϕ]dV=\frac{1}{2}\int \phi\vec D \cdot d\vec  S+\frac{1}{2}\int\vec D\cdot\vec E dV
$$

这里$r\rightarrow\infin$的话第二项可以忽略，但是其他情况应该是有点问题的呀。<font color=red>这里的能量密度必须对全空间而言才有意义，局部区域的能量还是要有两项。</font>

## * 4.2 磁介质

这里只说分子电流观点。

### $\S 4.2.1$ 磁化

* 磁化强度

有分子电流产生磁矩，但**具体朝哪取决于材料**。对应顺反磁性。==但对于导体$\mu_r$为1较多。==

1. 定义式

$$
\vec M=\frac{\sum \vec m_{分子}}{\Delta V}=nI\vec a
$$

2. properties
a. <font color=red>磁化电流面密度，注意M和 $\sigma$ 垂直</font>
$$
\vec M\times\vec n=\vec \sigma_m
$$
b. 线性介质，磁化电流等。

分子电流其实用的少。没啥用，我反推的。
$$
\vec M=\frac{\mu_r-1}{\mu_0\mu_r}
$$

### $\S 4.2.2$ 磁场强度

* 定义

==注意H和B可以反向，经典抗磁性==
$$
\vec H=\frac{B}{\mu_0}-\vec M=\frac{B}{\mu_r\mu_0}
$$

* Maxswell

$$
\begin{cases}
\nabla\cdot \vec B=0\\
\nabla\times\vec H=\vec J(+\partial_t \vec D)
\end{cases}
$$

<font color=red>这里不知道$\vec M$的散度为何不为0,或者说反例是什么？等做题吧。</font>

* Boundary Condition

$$
\begin{cases}
(\vec B_2-\vec B_1)\cdot \vec n=0\\
(\vec H_2-\vec H_1)\cdot \vec n=\sigma\approx0
\end{cases}
$$

这里取0的原因是==一般情况下介质面无自由电流，自由电荷都没有==。

### $\S 4.2.3$ 介质磁场能量

* 磁场能量密度定义

$$
w_m=\frac{1}{2}\vec B\cdot \vec H
$$

这个定义是由理想环磁场得到的的均匀积分形式对取空间微元得到。

* properties

1. 这个结果对全空间的积分和自感的结果相同。也即 $\frac{1}{2}LI^2$ 但是其实这个也没有什么普适理论。

2. 上述“自感”取的是整体视角，若是有两个或更多回路，自然有

$$
w_m=\frac{1}{2}[(\vec B_1\cdot \vec H_1+\vec B_2\cdot \vec H_2)+\vec B_1\cdot \vec H_2+\vec H_1\cdot \vec B_2 )]
$$

前两项是狭义自感能量密度；后两项是互感能量密度，显然对于正常的线性介质他们相同。

3. <font color=red>矢量证明需要电磁场动量守恒，待证。</font>

##  4.3 应用

### $\S4.3.1$ 电场磁场界面折射

$$
\begin{cases}
\frac{\tan\theta_1}{\tan\theta_2}=\frac{\varepsilon_1}{\varepsilon_2}\\
\frac{\tan\alpha_1}{\tan\alpha_2}=\frac{\mu_{r_1}}{\mu_{r_2}}
\end{cases}
$$

这个结论直接以两组边界条件相除即可。这说明高电导率或磁导率的场线会平行于界面，起到聚场的作用。

### $\S4.3.2$ 磁路定理

$$
\begin{cases}
\mathscr{E} _m=NI_0\\
\mathscr{E}_m=\oint\mathbf{H}\cdot d\mathbf l= \Psi_mR_m\\
R_m=\sum_i \frac{l_i}{\mu_r\mu_0S_i}
\end{cases}
$$

<font color=red>其思想是无漏磁，也即环路$\Psi_i$相等。若是S不变，甚至电场相同。</font> <!--可以高斯无源证之。-->==注意i是指各段路程==

### 4.3.3 介质平行板电容器

* 串并联电容

$$
\begin{cases}
1/C=1/C_1+1/C_2\\
C=C_1+C_2
\end{cases}
$$

>这个串联理应是通用规则，比如：
>$$
>C=\frac{Q}{U}=\frac{Q_1+Q_2}{U}=C_1+C_2\\
>$$
>

## * 4.3 电动力学拓展

### $\S4.3.1$ 顺磁性和抗磁性

此为经典观点，对于**轨道不变**的电子**轨道磁矩**。<!--这里轨道不变的观点在正常塞曼效应上倒是说的通。能级分裂为2l+1是对称的，而且得不到关于能级振幅分布的任何信息。-->

* 顺磁性体现在 $\mathbf L=\mathbf m\times\mathbf B$ 的磁矩**方向的改变顺于磁场**。
* 抗磁性体现在$\Delta\mathbf{|m|}\hat e_m\cdot \mathbf B<0$ 也即磁矩**大小的改变逆于磁场**。

### $\S4.3.2$ 唯一性定理

==依然是导体边界，只是电介质空间==

* 引理

1. 引理一为无源空间电势无极值。（该引理的保持可通过介质边界条件$\mathbf H_1=\mathbf H_2$得到，这里对于线性介质且$\varepsilon>0$ 的情况下保证了 $\partial_n\phi$ 的单调性。<font color=red>没错，其他情况没说.</font>
2. 引理二是导体等势空间也等势。这不用证明了。
3. 引理三是导体不带电就会等势自然空间不带电。（把电场线改为电位移即可。）

其他和真空介质类似。