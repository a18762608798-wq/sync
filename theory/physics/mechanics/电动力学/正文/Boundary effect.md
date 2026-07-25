# 静场边界效应

## 法向方向（交界面垂直于场的方向）

### 电场

* 由$\nabla \cdot D=\rho_0$，做圆柱高斯面，使其高h极小，有：

  ==$\vec{e}_n \cdot (\vec{D}_2-\vec{D}_1) =\sigma_f $==

* 又$D_i=\epsilon_0*E_i+P$，界面上$P$相同，有：<font color=#ff0000>I don't find its use in static potential</font>

  ==$\vec{e}_n \cdot (\vec{E}_2-\vec{E}_1) =\frac{\sigma_f}{\epsilon_0} $==

### 磁场

* $\nabla \cdot H=0$自然有：

  ==$dB=0$==

### Static potential field

* On the basis of $\vec{E}=-\nabla \psi$, and $\psi$ is integral from $\vec{E}$: 
  1. $\epsilon_2 \nabla \psi_2-\epsilon_1\nabla\psi_1=-\sigma_f$
  2. $\psi_1=\psi_2$

## 切线方向（交界面平行于场的方向）
### electric field

* By $\nabla \times E=\frac{\part B}{\part t}$，there are no magnetic field here，so：

  ==$dE=0$==

### magnetic field
* By $\nabla \times H=J_0+\frac{\part D}{\part t}$，there are no electric field here，$D=0$，so：

  ==$dH=J_0$==

## Summarize

| direction       | normal                                                       | tangential |
| --------------- | ------------------------------------------------------------ | ---------- |
| electric field  | $\vec{e}_n \cdot (\vec{D}_2-\vec{D}_1) =\sigma_f $           | $dE=0$     |
| magnetic field  | $dB=0$                                                       | $dH=J_0$   |
| potential field | $\epsilon_2 \nabla \psi_2-\epsilon_1\nabla\psi_1=-\sigma_f \quad \psi_1=\psi_2$ | $dH=J_0$   |

<!--Set direction, then the vector quantity is up to you.--> 
