# Solving Poisson equation

## Solving Poisson equation by mirror image method

### Evidence

#### Theorem

Uniqueness Theorem: If the distribution of potential is $\Delta\psi=-\frac{\rho_f}{\epsilon}$, and have the same boundary condition. the $\psi(r,\theta,\phi)$ is unique, ==which means we can revise the charge out of the $\psi$ room without revising conditions as up, then get the unique solution.==

#### NOTICE: 

**you can't revise value as follow in objective target potential area.**

* $\Delta\psi=-\frac{\rho_f}{\epsilon}$

  or **the foundational 麦克斯韦's equations is OK**

* boundary conditions

### Example

#### Infinite charged plate:

* Hypothesis charge of field source is $Q$
* The inductive charge is equivalent to $-Q$
* Result: the mirror point charge is $-Q$

#### Earth conductor ball:

![mirror earth conductor ball](D:\App_work\office_file\BaiduSyncdisk\文件快传\Physics\电动力学\正文\mirror earth conductor ball.jpg)

* Hypothesis exist the mirror point charge Q', it must has limiting as follow: 

  1. Because of the symmetry, $Q'$ is must on $OQ$
  2. On the surface of this conductor ball, The potential is equivalent to $0$, so $\varphi_p=\varphi'(r_p')+\varphi(r_p)=\frac{1}{4\pi\epsilon_0}*(\frac{Q'}{r'}+\frac{Q}{r})=0$, mean: $\frac{Q'}{Q}=-\frac{r'}{r}=const$
  
* Result:

  1. As long as$\Delta OPQ \cong \Delta OQ'P$, mean: ==$Q'=-\frac{R}{a}*Q$, $OQ'=\frac{R^2}{a}$==
  2. More: $\oint E \cdot dS=\oint -\nabla\varphi_n\cdot dS=Q=\oint \sigma_f \cdot dS$, mean: ==$E_2-0=\sigma_f$==
  

## Solving Poisson equation by Separating (Laplace's is also useful)

* Distribution equation:

$$
\Delta \psi=-\frac{\rho}{\epsilon}
$$

* separate: Separate the $\rho_f$ out of Poisson equations. Notice that because of **uniqueness theorem**, if $\varphi'$ satisfy the Poisson equation and $\psi$ satisfy the boundary conditions, ==we can set $\varphi'$ arbitrarily without noticing its form==

$$
\psi=\psi_0+\psi'\\
\Delta\psi_0=0\\
\Delta\psi'=-\frac{\rho}{\epsilon}
$$

* Plug the conditions in $\psi=\psi_0+\psi'$

## Solving General Poisson equation

* Precondition:
  1. Thinking: Like mirror image method, we will ==establish relationship between **unit point charge and inductive charge**==
  2. $\Delta\varphi=-\frac{\rho}{\epsilon_0}$
  3. $\Delta\psi=-\frac{\delta(x-x')}{\epsilon_0}$
  
* general solution:

  1. Plug $\psi$ and $\varphi$ formula into **Green's function**:

  $$
  \int_V(\psi\Delta\varphi-\varphi\Delta\psi)dV=\oint(\psi\nabla\varphi-\varphi\nabla\psi)\cdot dS
  $$
  
  2. According to: 
     * $\Delta\psi=-\frac{\delta(x-x')}{\epsilon_0}$, $\int_V\varphi\Delta \psi dV=-\frac{1}{\epsilon_0}\varphi$
     * $\Delta\varphi=-\frac{\rho}{\epsilon_0}$, $\int_V\psi\Delta\varphi dV=-\frac{\rho}{\epsilon_0}\int_V \psi dV$
     
     Plug the formulas into $3.1$, get ==the general solution of Poisson==.
     $$
     \varphi=\int_V\psi\rho dV+\epsilon_0\oint_S(\psi\nabla\varphi-\varphi\nabla\psi)\cdot dS
     $$
  
* ==Result with boundary==: 

  1. $\psi\vert_S=0$, under the circumstance, $\oint_S\psi\nabla\varphi\cdot dS=0$, so the solvating of Poisson equation with the first kind boundary condition is that: 
     $$
     \varphi=\int_V\psi\rho dV-\epsilon_0\oint_S\varphi\nabla\psi \cdot dS
     $$

  2. $\nabla\psi\vert_{S}=-\frac{1}{\epsilon_0S}$, under the circumstance, $\oint_S\varphi\nabla\psi\cdot dS=\langle\varphi\rangle_s\oint_S\nabla\psi\cdot dS=-\langle\varphi\rangle\frac{1}{\epsilon_0}$, so the solvating of Poisson equation with the second kind boundary condition is that:
     $$
     \varphi=[\int_V\psi\rho dV+\epsilon_0\oint_S(\psi\nabla\varphi)\cdot dS-\langle\varphi\rangle_S
     $$
