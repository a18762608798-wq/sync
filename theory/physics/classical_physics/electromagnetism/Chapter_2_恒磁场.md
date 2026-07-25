# Chapter 2 恒磁场

磁偶极子是磁矩特例。

* The founditional discover: 毕奥-萨伐尔定律

$$
d\vec F=Id\vec l\times\vec B
$$

<!--毕奥-萨伐尔定律源于电流元的相互作用，甚至磁感应强度也是这样定义的。这里的动量守恒以正则动量形式存在，机械动量不守恒，因此牛三被破坏。-->

## $\S2.1$ 静磁场

### $\S2.1.1$磁感应强度

$$
\vec B=\frac{\mu}{4\pi}\oint_L\frac{Id\vec l\times\vec e_r}{r^2}
$$

* properties

1. 可有旋，无源

$$
\begin{cases}
\nabla\cdot\vec B=0\Rightarrow \oiint_S\vec B\cdot d\vec S=0\\
\nabla\times\vec B=\mu_0\vec j\Rightarrow \oint_l \vec B\cdot d\vec l=\mu_0I
\end{cases}
$$

==注意 $\mu_0 I$ 对应的是环流磁场，未考虑无旋磁场==

2. **轴矢量**

* <span style="color:blue">Definition: 载流系统镜像变换，镜面上轴矢量反向，垂直镜面的矢量不变。</span>；
* <font color=lime>Property: 对称载流系统B垂直于镜面。</font>

> 结合定义作镜面变换易证。
>
> **旋转对称的话，中心B环流对称。**这和轴矢量无关。中心对称变换守恒性。

### $\S 2.1.2$ 作用力

#### $\S2.1.2.1$ 电流元受力，也即毕奥-萨伐尔定律

$$
d\vec F=Id l(\vec e_l\times\vec B)
$$

> Proof :
>
> According to :
> $$
> \vec F_i=q\vec v\times \vec B\\
> $$
> 小节电流元里面，Let the charge density is $n$ 。则 $dl$ 中的电子所受洛伦兹力之和为：
> $$
> d\vec F=\sum_i \vec F_i=nqsdl\vec v\times \vec B=nqsvdl\vec e_l\times \vec B
> $$
>
> Also : 
>
> $$
> I=nqsv\\
> $$
> therefore :
> $$
> d\vec F=Idl(\vec e_l\times\vec B)
> $$

#### $\S2.1.2.2$ 洛伦兹力

$$
\vec F=q\vec v\times\vec B
$$

* properties

1. 电流元受力的微分形式。
2. 洛伦兹力显然不做功。

## $\S 2.2.1$ 静磁场应用

### $2.2.1$ 载流线圈磁矩和匀强磁场力矩

#### 2.2.1.1 Fundament

$$
\begin{cases}
\vec m=IS\vec n\\
\vec L=\vec m\times\vec B\\
\varphi_m=-(\vec m\cdot\vec B)
\end{cases}
$$

<font color=orange>因此稳定条件是 $\min \varphi_m$ ,也即m,B同向</font>

==磁矩这个概念的提出就是如此，只是计算线圈力矩和势能的，量子力学应该是针对能量对电子的衍生概念。==

> 此证明用任意形状的导线圈。

####  2.2.1.2 任意电流分布

$$
\vec{m} = \frac{1}{2} \int \vec{r} \times \vec{J} \, dV\\
where \quad dI=\vec j\cdot d\vec S
$$

> 由此看来**电流有通量属性**。
>
> 有时候发神经用面电流密度：
> $$
> \vec m=\frac{1}{2}\int \vec r\times \vec K dS\\
> where\quad d\vec I=\vec K\cdot d\vec L
> $$
> **从磁偶极矩到线圈的磁矩推导**
>
> 考虑一个闭合线圈（例如圆形线圈），其电流为 $I$。对于理想的细线圈，电流密度 $\mathbf{J}(\mathbf{r})$ 可以表示为沿着曲线 $C$ 的线电流分布，即：
>
> $$
> \mathbf{J}(\mathbf{r}) = I \int_{C} \delta(\mathbf{r} - \mathbf{r}'(s)) \, \mathbf{t}(s) \, ds
> $$
>
> 其中：
>
> - $\delta$ 是狄拉克δ函数
> - $\mathbf{r}'(s)$ 是参数 $s$ 处的线圈位置矢量。
> - $\mathbf{t}(s) = \frac{d\mathbf{r}'(s)}{ds}$ 是单位切向量。
> - 积分路径 $C$ 表示线圈的形状。
>
> 将上述电流密度表达式代入磁偶极矩的定义式 ：
>
> $$
> \mathbf{m} = \frac{1}{2} I \int_{C} \mathbf{r}'(s) \times \mathbf{t}(s) \, ds = \frac{1}{2} I \oint_{C} \mathbf{r}' \times d\mathbf{r}'
> $$
>
> 应用斯托克斯定理，将环路积分转化为面积积分 ：
>
> $$
> \oint_{C} \mathbf{r}' \times d\mathbf{r}' = 2 \int_{S} \mathbf{n} \, dS = 2 \mathbf{A}
> $$
>
> 其中：
>
> - $S$ 是由曲线 $C$ 所围成的任意曲面。
> - $\mathbf{n}$ 是该曲面的单位法向量。
> - $\mathbf{A}$ 是曲面的面积矢量，定义为 $\mathbf{A} = \int_{S} \mathbf{n} \, dS$。
>
> 因此，对于一个闭合线圈，磁偶极矩的表达式为：
>
> $$
> \mathbf{m} = I \mathbf{A}
> $$
>
> 其中：
>
> - $I$ 是电流强度。
> - $\mathbf{A}$ 是线圈所围面积的矢量，方向由右手定则确定（即电流方向所围面积的法向量方向）。

###  $2.2.2$ 经典粒子

* 直导线
* 环形电流
* 无限长螺线管

$$
\vec B=\mu_0nI
$$

 这个结果可用磁感应环路得到。有意思的是这个结果==无关位置和管子形状。==

###  $2.2.3$ 均匀磁场粒子运动

若初速度不垂直或平行磁场，有螺旋线运动。螺距只和$v_{//}$有关, $M$只和$v_{垂直}^2/B$有关。

可根据此做磁约束。提高$B$迫使$v_{垂直}$ 增加，$V_{//}$ 减小。

### $2.2.4$ 回旋加速器

$T$与$v$无关。但高速可能影响质量。

### $\S2.2.5$ 霍尔效应。

载流子过匀强磁场形成电压。<font color=orange>相同电流向，电压与载流子种类有关。</font>

## $\S 2.3$ 电动力学拓展

### $\S2.3.1$ 磁单极子和磁场

$$
\vec H=\mu_0 \vec B
$$

这个磁场从磁单极子角度对应$\vec E$的形式，从电动力学对应泊松方程形式，但目前没用。

### $\S2.3.2$ 磁矢势

* Definition

$$
\vec B=\nabla\times\vec A
$$

书上所给的一个形式如下，可柱坐标证明其可用，但是实际一积分就发散，也不知道有什么用。

* properties

1. 磁矢势的环量为所围面磁通。

$$
\Phi_B=\oiint\vec B\cdot d\vec S= \oiint (\nabla\times\vec A)\cdot d\vec S=\oint \vec A\cdot d\vec l
$$

2. 可证明磁场无源。

$$
[\nabla\times(\nabla\times\vec A)]_k=\epsilon_{ijk}\partial_i\partial_kA_i=0
$$





