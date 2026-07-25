# The Velocity of wave

## Phase velocity

Phase velocity could only employed to **single wave function!!**

对于已经发出的波，其形状不会变。所以我们记其等相面的速度记作phase velocity.

那么等相面要求：

$$
d\varphi=0
$$

又对于单色波，对于等相面的$\varphi$ (多色波我也只看一个)，由于单色光波矢和频率是常数。
$\varphi=kr-wt\rightarrow\\d\varphi=kdr-wdt=0\rightarrow\\v_p=\frac{dr}{dt}=\frac{w}{k}$

由此phase velocity

$$
v_p=\frac{w}{k}
$$

## Group velocity

* 对于连续波矢叠加波

$$
\psi(x,t)=\frac{1}{2\pi}\int_{-\infin}^{+\infin}\varphi(k)e^{ikr-wt}dk
$$

我们计算Group velocity，是所谓波包中心的速度。波包中心的直接定义就是叠加效果最强的位置。或者说在$x_c$附近，$k(w效果类似，只是一般认为w是k的函数)$对$\varphi$影响小。Viz.

$$
\frac{\partial \varphi(k,x)}{\partial k}=0
$$

也即

$$
x_c=\frac{dw}{dk}t=v_g*t
$$

* 对于离散叠加波

  显然由于$v_g=\frac{dw(k)}{dk}$ w,k要有一个固定的函数关系才可以计算群速度。和实际的最大振幅位置不是一个位置，甚可能不是一种波（w-k关系)而没有所谓群速度。

  总之这个群速度大致是波包中心的速度，但有w-k呈函数的要求，需要是一类波。

## Instance

* photon

由波动方程有真空相速度

$$
v_p=\frac{w}{k}=\frac{1}{\sqrt{\epsilon_0\mu_0}}=c
$$

所以群速度是

$$
v_g=\frac{dw(k)}{dk}=c
$$

所以真空向速度等于群速度

但如果有介质

$$
\begin{cases}
v_p=\frac{w}{k}=\frac{c}{n(k)}\\
v_g\ne v_p
\end{cases}
$$
