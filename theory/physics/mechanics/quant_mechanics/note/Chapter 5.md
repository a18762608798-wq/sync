# Evolution and symmetry of mechanical quantities over time

[TOC]

## 5.1 The evolution of mechanical quantities over times

### 5.1.1 Conserved quantity

* Input: <font color=lime>The relationship of Ehrenfest</font> 

$$
i\hbar\frac{d \overline A}{d t}=\overline {[A,H]}+\overline{ \frac{\partial A}{\partial t}}
$$

* Definition:

$$
\begin{cases}
[A, H]=0\\
\partial_t A=0
\end{cases}
$$

* properties <!--We have proof via \hat U(t,0)-->
  **For any state:**

$$ \left\{ \begin{array}{l} \displaystyle \frac{d\overline{A}}{dt} = 0 \\ \displaystyle \frac{d|\langle n\alpha|\psi(t) \rangle|^2}{dt} = 0 \end{array} \right. $$
where $|n\alpha\rangle$ is a common state of $[A, H] = 0$, therefore:
$$\langle n\alpha|\hat U|\psi\rangle = e^{-iE_nt/\hbar}\langle n\alpha|\psi\rangle$$

  ### 5.1.2 The relationship of degeneracy of energy level and conserved quantity

* Premise:
  If there are two non-commutative conserved quantity in a system, meaning:

$$
\begin{cases}
[F,H]=0\\
[G,H]=0\\
[F,G]\neq 0
\end{cases}
$$

* Conclusion:
  The energy levels of this system is **usually** degeneracy <font color=magenta>or we could say that the eigen function set could not be totally non-degeneracy</font>
  The counter-example: For **specific states**: $[F,G]\psi_n=0$
* prefer:
  1. For a **non-degeneracy** energy level with a eigenfunction: $\psi_n$, it is also the eigenfunction of the conserved quantity of this system.<!--?-->
  2. <font color=gree>If the conserved quantity $[F,G]=C$, C is a constant, meaning the degrees of degeneracy of all energy levels are infinite.</font>

### 5.1.3 Virial theory

* Input:

$$
i\hbar \frac{d}{dt} \overline{\vec r\cdot\vec{p}}
$$

* Conclusion

$$
2\overline T=\overline{\vec r\cdot \nabla V(\vec r)}
$$

* Instance: for a n order homogeneous potential function:

$$
V(\lambda\vec r)=\lambda^\nu V(\vec r)
$$

$\quad\quad$Then we can get

$$
\begin{cases}
\frac{\partial  V(\lambda\vec r)}{\partial \lambda}=\frac{\partial (\lambda^\nu V(\vec r))}{\partial\lambda};\quad\lambda=1\\
\rightarrow \langle\mathbf r\cdot2 V(\mathbf r)\rangle=2
\langle T\rangle=\nu \langle V\rangle
\end{cases}
$$

> HF定理给virial theory也提供了一种证明方法，参数选择$\mu$，分别选取动量空间和坐标空间对比结果即可。

## *5.2 The propagation of wave package and Ehrenfest theory

* Input

$$
i\hbar \frac{d}{dt}\overline{r}=\overline{[r,H]}\\
i\hbar\frac{d}{dt}\overline{p}=\overline{[p,H]}
$$

* Theory

$$
\frac{d^2}{dt^2}\overline{r}=-\overline{\nabla V(r)}
$$

* Compare with classic theory: $\frac{d^2}{dt^2}{r}=-{\nabla V(r)}$
  Demand:

$$
\begin{cases}
r \approx \overline{r}\\
F(r)\approx\overline{F(r)} \tag{2}\\
Propagation\quad of \quad wave\quad package\quad is \quad slow: \frac{d^2w}{dt^2}\approx 0
\end{cases}
$$

$\quad\quad$Thereof, condition 2 could be expanded near $\overline{r}$

$$
F(x)=F(\overline{x})+F'(\overline{x})(x-\overline{x})+...\\
\overline{F(x)}=F(\overline{x})+\frac{1}{2}F''(\overline{x})\overline{(x-\overline{x})}
$$

$\quad\quad$Meaning

$$
|\frac{1}{2}F''(\overline{x})\overline{(x-\overline{x})}|<<|F'(\overline{x})(x-\overline{x})|
$$

## 5.3 Picture

### 5.3.0 Premise

#### The time-evolution operator

* Input

$$
\psi_s(t)=\hat U(t,0)\psi_s(0)
$$

* Definition

> <font color=magenta>注意：这个演化算符形式只是适用于$\hat H$不含时。**含时的形式不实用，不如直接解schrodinger方程。**</font>

$$
\hat U(t,0)=e^{-i\hat Ht/\hbar}
$$

* property:<font color=gree>unitary operator</font>

$$
\hat U(t,0)^\dagger \hat U(t,0)=1
$$

#### Mechanical quantities of different picture

The result of measure of mechanical quantities in different picture are common, The example is a conserved quantity in Heisenberg picture.

$$
[F_I(t),H_I]=[F_I(t),H]=U^\dagger[F,H]U=0
$$

### 5.3.1 Schrödinger Picture

* Wave function

$$
\psi_s(t)=\hat U(t,0)\psi_s(0)
$$

* The evolution of wave function: Schrödinger equation

$$
i\hbar \frac{\partial}{\partial t}\psi_s(t)=i\hbar \frac{\partial}{\partial t}(\hat U(t,0)\psi_s(0))=H\psi_s(t)
$$

* Mechanical quantities

$$
F_s=F\\
$$
<span style="color:red">这是力学量不含时，而非算符。</span>

* The evolution of mechanical quantities

$\quad\quad$ In fact, $\frac{d F_s}{d t}=0$
$\quad\quad$ However we could care the evolution of $\overline F$ , viz. the relationship of Ehrenfest.

$$
i\hbar\frac{d}{dt}\overline{F}=\overline{[F,H]}
$$
### $\star$ 5.3.2 Heisenberg Picture

* Wave function

$$
\psi_H=\hat U^\dagger(t,0)\psi_s(t)=\psi_s(0)
$$

* The evolution of wave function

$$
\frac{\partial\psi_H}{\partial t}=\frac{\partial\psi_s(0)}{\partial t}=0
$$

* Mechanical quantities
  
  1. Input

$$
\overline {F(t)}=(\psi_H,U^+FU\psi_H)
$$

$\quad\quad$ 2. Definition

$$
\begin{cases}
F_H(t)=U^\dagger \hat FU\\
H_H(t)=U^\dagger \hat HU=\hat H
\end{cases}
$$

<font color=magenta>Therefore $\hat H$ in Heisenberg picture is common to Shrodinger picture.</font>

* The evolution of mechanical quantities

$$
i\hbar\frac{d}{dt}F_H(t)=[F_H(t),H]
$$

* Instance: For $H=\frac{p^2}{2m}+\frac{1}{2}mw^2x^2$

$$
\begin{cases}
i\hbar \frac{d}{dt}x(t)=[U^\dagger xU,H]=U^+[x,H]U=i\hbar p(t)/m\\
i\hbar \frac{d}{dt}p(t)=[U^\dagger pU,H]=U^+[p,H]U=-i\hbar mw^2x(t)
\end{cases}
$$

### 5.3.3 Interaction Picture

* Definition of H, distinguish with H_I

$$
\hat H=H_0+H'(t)
$$

* Wave function

$$
\psi_I=U_0^+\psi_s(t)
$$

* The evolution of wave function($H'_I(t)$)

$$
i\hbar \frac{\partial}{\partial t}\psi_I(t)=H'_I(t)\psi_I(t)
$$

* Mechanical quantities

$$
F_I(t)=U_0^+FU_0
$$

* The evolution of mechanical quantities($H_0$)

$$
i\hbar\frac{d}{dt}F_I(t)=[F_I(t),H_0]
$$

## 5.4 The analysis of the transform(specially conserved quantities) with the invariant of $\hat H$（for any quantities with similar property of H is also OK)

<font color=gree>这里为什么哈密顿量的对称性代表系统的对称性是分析力学的内容。后面分别反映空间，角动量，时间的平移不变性。</font>

### 5.4.0 Definition

* General transform operator: $\hat Q$

$$
\begin{cases}
[Q,H]=0\\
Q^+Q=1\\
\frac{\partial{Q}}{{\partial t}}=0\\
Q^{-1}\quad is \quad exist
\end{cases}
$$

* Infinite same transform operator: $\hat Q=1+i\epsilon\hat F$, always for  continuous transform.

$$
\begin{cases}
F^+=F\quad(Q^+Q=1)\\
[F,H]=0\quad([Q,H]=0)
\end{cases}
$$

### 5.4.1 Essential instance

#### 5.4.1.1 Translation operator (continuous)

* Input: $\delta x\rightarrow0$

$$
\hat D(\delta x)\psi(x)=\psi(x-\delta x)=e^{-i\delta x\hat p_x/\hbar}\psi(x)\approx (1-i\delta x/\hbar*\hat p_x)\psi(x)
$$

<font color=gree>目前看来，这些算符直接作用于函数形状而非表象。对于平移操作，直接结果理应是：</font>
$$
\hat D(a)\psi(x)=\psi'(x)\quad and\quad \psi'(x')=\psi(x)\\
therefore\quad\hat D(a)\psi(x)=\psi(x-a)
$$
<font color=gree>而非是直接改变表象。==最重要的是，平移算符依托于表象x==</font>

* Conclusion

$$
\begin{cases}
operator:D(\delta \vec r)=e^{-i\delta \vec r\cdot \vec p/\hbar}\\
infinite\quad small\quad operator:\vec p
\end{cases}
$$

$\quad\quad$If a system meet these conditions, its $H$ is conserved over translation operator(**free particle**):

$$
\begin{cases}
[\vec p,H]=0\\
p^+=p
\end{cases}
$$

> **Counter instance**: The translation operator of time
> $$
> \hat D(\delta t)\psi(t)=e^{-i \hat H t/\hbar}=\psi(t+\delta)
> $$
> <span style="color:magenta">The core donfliction is the transform of time is not really translation, it is more as similar as evalution</span>

#### 5.4.1.2 Rotation operator (continuous)

* Input: $\delta\varphi\rightarrow0$, meaning the rotation axis is $\hat e_z$

$$
\hat D(\delta \varphi)\psi(\varphi)=\psi(\varphi-\delta\varphi)=e^{-\delta\varphi l_z/\hbar}\psi(\varphi)\approx(1-\delta\varphi/\hbar*l_z)\psi(\varphi)
$$

* Conclusion: for the rotation axis is $\vec e_n$

$$
\begin{cases}
operator:D(\delta \varphi \vec e_n)=e^{-i\delta\varphi \vec e_n\cdot \vec l/\hbar}\\
infinite\quad small\quad operator:\vec l
\end{cases}
$$

$\quad\quad$$\quad\quad$If a system meet these conditions, its $H$ is conserved over rotation operator(**central potential**):

$$
\begin{cases}
[\vec l,H]=0\\
l^+=l
\end{cases}
$$

* <font color=orange>Case：在角动量上有个直接应用：</font>

$$
|j m_n\rangle=\hat D(\varphi_0\hat e_z)\hat D(\theta_0\hat e_y)|j m_z\rangle=e^{-i \varphi_0 \hat l_z}e^{-i \theta_0 \hat l_y}|j m_z\rangle
$$

也即 $[j^2,j_n]$ 表象和 $[j^2,j_z]$ 表象的表象变换，这显然是个**幺正变换**。是由无穷小旋转算符叠加而成，<font color=magenta>这是某一类变换的幺正变换通式。</font>

具体的，以自旋角动量为例子。 $n=(\sin\theta\cos\varphi, \sin\theta\sin\varphi,\cos\theta)$, $\sigma_z$ 表象下，

<font color=magenta>注意算符形式，旋转操作是$s_n$作为生成元</font>
$$
\hat U(\theta_0,\varphi_0)=e^{-i\varphi_0\hat s_z}e^{-i\theta_0\hat s_y}
$$
重点是讨论$e^{-i\theta_0\sigma_y}$的矩阵形式。

>补充证明方法：
>
>利用$\sigma_n^2=\hat I$ :
>$$
>e^{-i\theta_0 \hat s_y}=\sum_n \frac{(-i\theta_0 \sigma_y/2)^n}{n!}=\sum_{k} \frac{(-1)^k(\theta_0/2)^{2k}}{(2k)!}\hat I-i\sum_{k}\frac{(-1)^k(\theta_0/2)^{2k+1}}{(2k+1)!}\hat \sigma_y=\cos(\theta_0/2)\hat I-i\sin(\theta_{0}/2)\hat \sigma_y\\
>e^{-i\varphi_0\hat s_z}=写矩阵\\
>\therefore \hat U(\theta_0,\varphi_0)=[\cos(\theta_0/2)\hat I-i\sin(\theta_0/2)\hat \sigma_z]e^{-i\varphi_0\hat \sigma_z/2}\\
>$$

#### 5.4.1.3 Space reflection operator and parity conservation

* Definition

$$
\hat P\psi(\vec r)=\psi(-\vec r)
$$

$\quad\quad$ 1. eigenvalue

$$
P^2=1\Rightarrow \lambda=\pm1
$$

$\quad\quad$ 2. eigenfunction

$$
\begin{cases}
\psi_+(\vec r)=\psi_+(\vec r)\quad odd\\
\psi_-(\vec r)=-\psi_-(-\vec r)\quad even
\end{cases}
$$

* Properties

$$
P=P^*=\tilde P=P^+=P^{-1}
$$

* Expansion

$\quad\quad$ 1. Parity Conservation

$$
[\hat P,\hat H]=0
$$

$\quad\quad$Implication:

$\quad\quad$ a. if eigenvalue $E_n$ is non-degeneracy,     The eigenfunction $\psi_n(\vec r)$ is odd or even pariy.

$\quad\quad$ b. if eigenvalue $E_n$ is degeneracy , The eigenfunction $\psi_{nk}(\vec r)$ counld be linear superposition to pariy states.

$\quad\quad$ 2. Take apart odd and even parts from any wave function

$$
\psi=\psi_++\psi_-\\
\psi_\pm=\frac{1}{2}(1\pm P)\psi_\pm
$$

## 5.3 The identical particle system and wave function exchange symmetry

<!--permit coupling-->

### 5.5.0 Exchange operator

* Definition

$$
\hat P_{ij}\psi(q_1,...q_i,...,q_j...q_N)=\psi(q_1,...q_j,...,q_i...q_N)
$$

$\quad\quad$ If it is a identical particle system (**This identical system should not change because exchange.**) 

$$
\hat P_{ij}\psi(q_1,...q_i,...,q_j...q_N)=\psi(q_1,...q_j,...,q_i...q_N)=\lambda\psi(q_1,...q_i,...,q_j...q_N)
$$

<span style="color:lime">For Hermite operation, it has similar porperties.</span>

$$
[P_{ij}, H]|\phi_n\rangle = P_{ij}H|\phi_n\rangle - HP_{ij}|\phi_n\rangle = \lambda * 0 = 0
$$

1. Eigenvalue

$\quad\quad$ For a identical system, exchange can't alter the quantum state, implication:

$$
P_{ij}\psi(q_1,q_2)=\lambda\psi(q_1,q_2)
$$

$\quad\quad$ operate twice,

$$
P^2_{ij}=1\Rightarrow \lambda^2=1
$$

$\quad\quad$ 2. Eigen-function

<font color=magenta>Logically speaking</font>, $\lambda$ <span style="color:magenta">is the eigenvalue of P_{ij} in identical system. this identical system is it's eigen-state exactly</span> 

<span style="color:magenta">However, </font> $[p_{ij}, p_{\mu v}] \neq 0$, <span style="color:magenta">This system make no sense have common symmetry with</span> $p_{ij}$ and $p_{\mu v}$ . This system make no sense have common exchange symmetry for all particle pair. 

<span style="color:red">miraculously, The identical particles of nature have definite exchange symmetries. </span>

> **一般本征态照常算，最后重新构造满足对称关系的波函数，参考下方法**

$$
\hat P_{ij}\psi=\psi \quad or\quad \hat P_{ij}\psi=-\psi
$$

* Property

$$
[P_{ij},H]=0
$$

### 5.5.1 Introduction of Bose and Fermi

| spin  | $N\hbar$ | $(N+\frac{1}{2})\hbar$ | Exchange symmetry$\quad\lambda$ | States demand                 | Instance |
| ----- | -------- | ---------------------- | ------------------------------- | ----------------------------- | -------- |
| Fermi |          | 1                      | -1(odd)                         | can't be a on a common states | electron |
| Bose  | 1        |                        | 1(even)                         | free                          | photon   |

### 5.5.2 System of Bose and Fermi

#### 5.5.2.1 Doubt particles(ignore interaction)

* Fermi

$\quad\quad$ 1. On different states, demand odd parity.

$$
\psi_{k_1k_2}^a(q_1,q_2)=\frac{1}{2}(1-P_{12})\psi_{k_1}(q_1)\psi_{k_2}(q_2)=\frac{1}{2}(\psi_{k_1}(q_1)\psi_{k_1}(q_2)-\psi_{k_1}(q_2)\psi_{k_2}(q_1))=\begin{vmatrix}
\psi_{k_1}(q_1)&\psi_{k_1}(q_2)\\
\psi_{k_2}(q_1)&\psi_{k_2}(q_2)
\end{vmatrix}
$$

$\quad\quad$ 2. On common states, The det is 0, which implication the **Pauli exclusion principle**

$\quad\quad$ **Two identical Fermi can't be on common quantum states**

* Bose

$\quad\quad$ 1. On different states, demand even parity.

$$
\psi_{k_1k_2}^s(q_1,q_2)=\frac{1}{2}(1+P_{12})\psi_{k_1}(q_1)\psi_{k_2}(q_2)=\frac{1}{2}(\psi_{k_1}(q_1)\psi_{k_1}(q_2)+\psi_{k_1}(q_2)\psi_{k_2}(q_1))
$$

$\quad\quad$ 2. On common states,

$$
\psi_{kk}^s(q_1,q_2)=\frac{1}{2}(1+P_{12})\psi_{k}(q_1)\psi_{k}(q_2)
$$

#### 5.5.2.2 multiple particles(ignore interaction)

* Fermi

$$
\psi_{k_1k_2,k_3}^a(q_1,q_2,q_3)=\frac{1}{\sqrt{N!}}\begin{vmatrix}
\psi_{k_1}(q_1)&\psi_{k_1}(q_2)&\psi_{k_1}(q_3)\\
\psi_{k_2}(q_1)&\psi_{k_2}(q_2)&\psi_{k_2}(q_3)\\
\psi_{k_3}(q_1)&\psi_{k_3}(q_2)&\psi_{k_3}(q_3)
\end{vmatrix}\\
\hat P_{12} \psi_{k_1k_2,k_3}^a(q_1,q_2,q_3)=\delta_P \psi_{k_1k_2,k_3}^a(q_1,q_2,q_3)=-\psi_{k_1k_2,k_3}^a(q_1,q_2,q_3)
$$

$\quad\quad$ Exchanging the particle implicate exchange the volumns of this det, $\delta_P$ according to the times of bubbing exchange.

* Bose

$\quad\quad$ We should certain the occupation number of every quantum states. Then total permutation summation.

$\quad\quad$ For instance there three states, occupation number: $1,2,0$

$$
\psi_{k_1k_2k_0}^s (q_1,q_2,q_3)=\frac{1}{\sqrt{\frac{3!}{1!2!0!}}}(\psi_1(q_1)\psi_2(q_2)\psi_2(q_3)+\psi_1(q_2)\psi_2(q_1)\psi_2(q_3)+\psi_1(q_3)\psi_2(q_2)\psi_2(q_1))
$$

## Tips

### 1 狗都不用的commute realtionship

* $\langle k|[\hat H,\hat x]^2|k\rangle$

* $\langle k|[x,[\hat H,\hat x]]|k\rangle$

* 有的时候也和HF一起用
