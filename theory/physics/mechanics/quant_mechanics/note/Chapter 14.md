# Chapter 14

## 14.1 变分法

[toc]

### 14.1.1 Permise

#### 14.1.1.1 变分法

$$
\begin{cases}
Objective:\delta (\langle \phi_n|\hat H|\phi_n\rangle)=0\\
limited\quad condition: \langle \phi_n|\phi_n\rangle=1
\end{cases}
$$

拉格朗日乘子法：
$$
\delta(\langle \phi_n|\hat H|\phi_n\rangle)-\lambda \delta(\langle \phi_n|\phi_n\rangle)=0 \tag{1}
$$
其中$\lambda$是拉格朗日乘子。

#### 14.1.1.2 变分原理和定态薛定谔方程有等价性

1. 拉格朗日乘子就是本征值

Accroding to item $(1)$ ，
$$
\langle \delta \phi_n|\hat H|\phi_n\rangle+\langle \phi_n|\hat H|\delta \phi_n\rangle-\lambda \langle \delta \phi_n|\phi_n\rangle-\lambda \langle \phi_n|\delta \phi_n\rangle=\langle \delta\phi_n|\hat H-\lambda|\phi_n\rangle+\langle \phi_n|\hat H-\lambda|\delta\phi_n\rangle\\
=\langle \delta\phi_n|\hat H-\lambda|\phi_n\rangle+\langle \delta\phi_n^* |\hat H-\lambda^*|\phi_n^*\rangle=0
$$
also, $\lambda=\lambda^*$
$$
\begin{cases}
(\hat H-\lambda)|\phi_n\rangle=0\\
(\hat H-\lambda)|\phi_n^*\rangle=0
\end{cases}
$$
Which is Satic state Schrodinger Equation evidently.

2. 满足S的方程可以令 $\delta \langle \phi_n|\hat H|\phi_n\rangle=0$

* Assign : $|\psi_n\rangle=|\phi_n\rangle+|\delta \phi_n\rangle$

* Limited condition :

$$
\langle \psi_n|\psi_n\rangle=1\Rightarrow\\
\langle \phi_n|\delta\phi_n\rangle+\langle \delta\phi_n|\phi_n\rangle+\langle \delta\phi_n|\delta\phi_n\rangle=0
$$

* $\delta  E_n$

$$
\delta E_n=\delta(\langle \psi_n|\hat H|\psi_n\rangle)=\langle \delta\phi_n|\hat H|\phi_n\rangle+\langle \phi_n|\hat H|\delta\phi_n\rangle+\langle\delta \phi_n|\hat H|\delta\phi_n\rangle=-E_n\langle\delta\phi_n|\delta\phi_n\rangle+\langle \delta\phi_n|\hat H|\delta\phi_n\rangle\\
\Rightarrow -E_n \sum_m \langle \delta \phi_n|\phi_m\rangle\langle \phi_m|\delta\phi_n\rangle+\sum_mE_m\langle \delta \phi_n|\phi_m\rangle\langle \phi_m|\delta\phi_n\rangle=-E_n \sum_m |\delta a_m|^2+\sum_mE_m|\delta a_m|^2
$$

therefore, $\delta a_m=0\rightarrow \delta \phi_n=0\Rightarrow \delta E_n=0$

Viz., If $|\phi_n\rangle$ satify Schrodinger equation, $\delta E_n=0$

### 14.1.2 Content and Application

> For any $\hat H$ is difficulty to solve eignefunction, <font color=magenta>We guess a form of eigenfunction with a undermined peremeter $\lambda$.</font>

#### 14.1.2.1 Basic state

<font color=magenta>说明：本分法本身根本就不管是不是基态</font>，必须给出基态含参波函数形式以确定参数。

Assume $|\psi_\lambda\rangle$ <font color=red>要先归一化</font>
$$
|\phi_\lambda\rangle=\frac{|\psi_\lambda\rangle}{\sqrt {\langle \psi_\lambda|\psi_\lambda\rangle}}
$$
于是平均值：
$$
\overline{H}=\langle \phi_0|\hat H|\phi_0\rangle
$$
also $\delta \hat H=0 $
$$
\sum_i \partial_{\lambda_i} \overline H\delta \lambda_i=0
$$
参数一般线性无关，$Viz.,$
$$
\frac{\partial \overline H}{\partial \lambda_i}=0
$$
The we could solve $\lambda_i$

#### 14.1.2.2 Other state

**Assume $|\psi_1\rangle$**

<font color=magenta>Initally, we must make the function indepentent with $|\psi_1\rangle$</font>
$$
\begin{cases}
|f_1\rangle=|\psi_1\rang-|\phi_0\rangle\langle \phi_0|\psi_1\rangle\\
|\phi_1\rangle =\frac{|f_1\rangle}{\sqrt{\langle f_1|f_1\rangle}}
\end{cases}
$$
**Then similarly process the undermined peremeter.**

### 14.1.3 properties

* $\overline H\ge E_0$

试探基态波函数：$|\psi_0\rangle=\sum_n|\phi_n\rangle\langle \phi_n|\psi_0\rangle$
$$
\frac{\langle \psi_0|\hat H|\psi_0\rangle}{\langle \psi_0|\psi_0\rangle}=\sum_{mn}\frac{\langle \psi_0|\phi_m\rangle\langle \phi_m|\hat H|\phi_n\rangle\langle \phi_n|\psi_0\rangle}{\langle \psi_0|\psi_0\rangle}=\sum_{mn}\frac{E_n\langle \psi_0|\phi_m\rangle \langle \phi_m|\phi_n\rangle \langle \phi_n|\psi_0\rangle}{\langle \psi_0|\psi_0\rangle}\ge E_0
$$

### 14.1.4 Cases

#### 14.1.4.1 Virial theory For 幂次势

> 比完全的HF简单一点。
>
> <font color=magenta>该方法核心是$\lambda x$中的$\lambda$是参数，而非表象。与表象变换令dx $\rightarrow d(\lambda x)$不同</font>

Known :
$$
V(\lambda x)=\lambda^nV(x)
$$
**Assume 试探波函数：** <!--这里尺度变换精髓；函数关系已然改变-->
$$
|\psi_\lambda\rangle\\
\langle x|\psi_\lambda\rangle =C \langle \lambda x|\phi_n\rangle\\
\Rightarrow \langle \psi_\lambda|\psi_\lambda\rangle=\int dx\langle \psi_\lambda|x\rangle\langle x|\psi_\lambda\rangle=\int |C|^2 \langle \phi_n|\lambda x\rangle \langle \lambda x|\phi_n\rangle dx=\frac{|C|^2}{\lambda}=1\\
$$

综上，选区$C=\sqrt \lambda$ , mean:
$$
\langle x|\psi_\lambda\rangle=\sqrt \lambda \langle \lambda x|\phi_n\rangle
$$
$Viz.,$
$$
\langle \psi_\lambda|\hat T|\psi_\lambda\rangle=\lambda\int \langle \psi|\lambda x\rangle(-\frac{\nabla^2}{2})\langle \lambda x|\psi\rangle dx=\lambda^2\int \langle \psi|\lambda x\rangle (-\frac{\nabla'^2}{2})\langle \lambda x|\psi\rangle d(\lambda x)=\lambda^2\langle\phi_n| \hat T|\phi_n\rangle\\
\langle \psi_\lambda|\hat V|\psi_\lambda\rangle=\lambda^{-n}\langle \phi_n|\hat V|\phi_n\rangle
$$
综上，
$$
\langle\psi_\lambda|\hat H|\psi_\lambda\rangle=\lambda^2\langle \phi_n|\hat T|\phi_n\rangle+\lambda^{-n}\langle \phi_n|\hat V|\phi_n\rangle
$$

变分法：
$$
\frac{\partial \langle \psi_\lambda|\hat H|\psi_\lambda\rangle}{\partial \lambda}|_{\lambda=1}=0\\
\Rightarrow 2 \langle \phi_n|\hat T|\phi_n\rangle-n\langle \phi_n|\hat V|\phi_n\rangle=0
$$


![[量子力学 卷1 第5版 曾谨言.pdf#page=22&rect=28,354,410,573|量子力学 卷1 第5版 曾谨言, p.V]]

![[Excalidraw/Drawing 2025-11-21 11.01.39.excalidraw]]
![[Excalidraw/Drawing 2025-11-21 10.56.47.excalidraw]]