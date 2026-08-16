# Chapter 8: Representation transformation and quantum mechanical matrix form

[toc]

## 8.1 Property of Dirac operation

### 8.1.1 Scalar product

* Definition

$$
(\psi,\varphi)=\langle \psi|\varphi\rangle
$$

* property

$$
\begin{cases}
\langle \phi_j|\phi_k\rangle=\delta_{jk}\\
(\langle\psi|\varphi\rangle)^*=\langle \varphi|\psi\rangle\\
(\langle\phi_\alpha'|\phi_k''\rangle)^+=\langle\phi_\alpha''|\phi_k'\rangle可以拿认为是交换上标\\ 
\end{cases}
$$

<font color=magenta>Now $\dagger$ is permit for either mechanical quantities or matrixs</font>

appendix: for matrix elements:

if $\hat A=\hat B^\dagger,A_{nm}^*=B_{mn}$ <!--这个几乎是定义了-->

$$
\langle m|\hat A^\dagger|{n}\rangle=\langle n|\hat A|m\rangle^*=A_{nm}^*\\
=\bra{m}\hat B\ket{n}=B_{mn}
$$

If we direct operate the matrix elements by $\dagger$ ,unmeanl

### 8.1.2 Projection operation

$$
\begin{cases}
P_k=|\phi_k\rangle\langle\phi_k|\\
\sum_k|\phi_k\rangle\langle\phi_k|=I\\
\int dx'|x'\rangle\langle x'|=I\rightarrow \iint dx dy |x\rangle\otimes |y\rangle \langle y|\otimes\langle x|=\iint dxdy |xy\rangle\langle xy|
\end{cases}
$$

有一个实用的例子是，测量得到某力学量得到某个本征值的概率是:
$$
P=\langle \psi|\phi_k\rangle\langle \phi_k|\psi\rangle
$$

## 8.2 Foundation of matrix form

### 8.2.1 Quantum state

* Mechanical matrix form

According to $\ket{\psi}=\sum_k\ket{\phi_k}\bra{\phi_k}\psi\rangle=\sum_k\ket{\phi_k}a_k$

$$
a_k=\langle\phi_k|\psi\rangle
$$

Viz. The state in representation $\phi_k$ is

$$
\langle \phi|\psi\rangle=\begin{Bmatrix}
\langle\phi_1|\psi\rangle\\
\langle\phi_2|\psi\rangle\\
\langle\phi_3|\psi\rangle\\
\langle\phi_4|\psi\rangle\\
...
\end{Bmatrix}
$$

* Representation transformation
1. Introduction，<font color=magenta>注意是坐标变换，不是基本矢量。</font>

According to $\langle\phi'_\alpha|\psi\rangle=\sum_k\langle\phi_\alpha'|\phi''_k\rangle\langle\phi_k''|\psi\rangle$

Which is $\langle\phi''|\psi\rangle\rightarrow\langle\phi'|\psi\rangle$

$$
S_{\alpha k}=\langle\phi_\alpha'|\phi_k''\rangle
$$

2. properties

S is a **unitary matrix :$SS^+=I$**

Viz. Proof $(S^+S)_{\alpha k}=\delta_{\alpha k}$ 运算结果矩阵的(j,k)位置元素可以这样得到。

$$
\sum_i (S_{\alpha i})^+S_{i k}=\sum_i S_{\alpha i}^+S_{i k}=\sum_{i}\langle (\phi_i'|\phi_\alpha''\rangle)^*\langle\phi_i'|\phi_k''\rangle=\sum_i\langle\phi_\alpha''|\phi_i'\rangle\langle\phi_i'|\phi_k''\rangle=\langle\phi_\alpha''|\phi_k''\rangle=\delta_{\alpha k}
$$

3. Utilize

* For any vector

$$
\langle\phi'_\alpha|\psi\rangle=\sum_k\langle\phi_\alpha'|\phi''_k\rangle\langle\phi_k''|\psi\rangle=\sum_k S_{\alpha k}\langle \phi_k''|\psi\rangle
$$

* For mechanical operator

$$
\langle \phi^a_m|\hat F|\phi^a_n\rangle=\sum_{jk}\langle \phi^a_m|\phi^b_j\rangle\langle\phi^b_j|\hat F|\phi_k^b\rangle\langle\phi_k^b|\phi^a_n\rangle=(S\hat F S^\dagger)_{mn}
$$

* <font color=magenta>显然对于变换矩阵的获取，有个有意思的点</font>

对于从 $b$ 表象变化到 $a$ 表象的矩阵元，有如下关系：
$$
S_{mn}^{ab}=\langle \phi_m^a|\phi_n^b\rangle
$$
这显然是$\hat F_b$在$\hat F_a$表象下的本征向量。<font color=lime>换言之，对于从b表象下到a表象的变换矩阵，也是$F_b$在$\hat F_a$表象的本征向量的横向排列。</font>
$$
S^{ab}=\begin{Bmatrix}
\langle\phi_1^a|\phi_1^b\rangle & \langle\phi_1^a|\phi_2^b\rangle &...\\
\langle\phi_2^a|\phi_1^b\rangle & \langle\phi_2^a|\phi_2^b\rangle &...\\
... & ... & ...
\end{Bmatrix}
$$

### 8.2.2 Operator

* Mechanical matrix form

In anticipation of representation $|\phi_k\rangle$

Known:

$$
\begin{cases}
|\psi_1\rangle=\sum_k|\phi_k\rangle\langle\phi_k|\psi_1\rangle\\
|\psi_2\rangle=\sum_k|\phi_k\rangle\langle\phi_k|\psi_2\rangle\\
|\psi_1\rangle=F|\psi_2\rangle
\end{cases}
$$

 cdot $\langle \phi_j|$ then we can get Matrix element of F with representation $|\phi_k\rangle$

$$
\sum_k\langle\phi_j|F|\phi_k\rangle\langle\phi_k|\psi_2\rangle=\sum_k\langle\phi_j|\phi_k\rangle\langle\phi_k|\psi_1\rangle=\langle\phi_j|\psi_1\rangle\\
Viz.\sum_kF_{jk}a_{2k}=a_{1j}
$$

Compare the form we could know :

$$
F_{jk}=\langle\phi_j|F|\phi_k\rangle
$$

* Representation transformation :

According to  $\langle\phi_\alpha''|F|\phi_\beta''\rangle$ turn to $\langle\phi'_j|F|\phi'_k\rangle$

$$
F_{jk}=\langle\phi'_j|F|\phi'_k\rangle=\sum_{\alpha\beta}\langle\phi_j'|\phi_\alpha''\rangle\langle\phi_\alpha''|F|\phi_\beta''\rangle\langle\phi_\beta''|\phi_k'\rangle=\sum_{\alpha\beta}S_{j\alpha}F_{\alpha\beta}(S_{\beta k})^+=(SFS^+)_{jk}
$$

也即对角化。

* Instance :

有个例子莫名重要，谐振子的矩阵元。这个利用到厄米多项式的递推性质，或者产生湮灭算符：

$$
x\psi_n=\frac{1}{\alpha}(\sqrt{\frac{n+1}{2}}\psi_{n+1}+\sqrt{\frac{n}{2}}\psi_{n-1})\\
\Rightarrow\langle m|x|n\rangle=\frac{1}{\alpha}(\sqrt{\frac{n+1}{2}}\delta_{m,n+1}+\sqrt{\frac{n}{2}}\delta_{m,n-1})
$$

这个做矩阵乘法可得

### 8.2.3 Eigenfunction for  any representation

任意态 $|\psi\rangle$, 对于$\hat L |\psi\rangle = L'|\psi\rangle$，注意这里$L'$是一个抽象的变量。已知道$\langle m |\hat L |n\rangle$ 也即$\hat L$在某个表象下形式。

$$
\begin{split}
(\hat L  - L')|\psi\rangle = 0\\
\sum_{mn} |m\rangle \langle m|\hat L -L'|n\rangle\langle n|\psi\rangle = 0\\
\sum_n (\langle m|\hat L|n\rangle - L'\delta_{m,n}) \langle n|\psi\rangle= 0
\end{split}
$$
注意$\langle n|\psi\rangle = \sum_f \langle n|f\rangle \langle f|\psi\rangle$, 数学上一般求的是$\langle n| f\rangle$

### 8.2.4 Mean value

The mean value of any representation is the **diagonal matrix elements** evidently.

$$
\langle F\rangle_n=\langle \psi_n|F|\psi_n\rangle=\int dx'dx''\langle \psi_n|x'\rangle\langle x'|F|x''\rangle\langle x''|\psi_n\rangle
$$

### 8.2.5 The mark of matrix room

#### 8.2.5.1 使用下标或复合符号标记基底：

dirac 和矩阵直接的兼容性不太好，要标记一下
$$
|m_{s_n} = \frac{1}{2}\rangle_{\sigma_z} = \begin{pmatrix}
\cos\left(\frac{\theta}{2}\right) \\
e^{i\phi} \sin\left(\frac{\theta}{2}\right)
\end{pmatrix}
$$

#### 8.2.5.2 表象变换矩阵

从$\sigma_z$到$\sigma_n$
$$
\hat S_{\sigma_z}^{\sigma_n}
$$

##### 8.2.5.3 算符矩阵

$$
[\sigma_x]_z = \begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}
$$

## 8.3 Continuous representation

### 8.3.0  <span style="color: lime;">inspiration</span>

The classic form is **error** technologically:
$$
\hat p \Leftrightarrow -i \nabla
$$
It is **not a totally equal** rule for state function. However: 
$$
\langle x|\hat p|\psi\rangle= -i \nabla\langle x|\psi\rangle
$$

<font color=magenta>The commute relationship is also basic on expression, but all express</font>

Notice it is not equal to $\langle x|\hat p \Leftrightarrow -i\hbar \partial_x$

### 8.3.1 The Fourier transform in quantum mechanical

$$
\begin{cases}
\psi(x)=\frac{1}{\sqrt {2\pi}}\int \varphi(p)e^{ipx}\\
\varphi(p)=\frac{1}{\sqrt{2\pi}}\int \psi(x)e^{-ipx}
\end{cases}
$$

It is similar as traditional Fourier transform, but consider on the normalization of quantum state. Write as :
$$
\langle x|\psi\rangle=\int \langle x|p\rangle dp\langle p|\psi\rangle\\
$$
Evidently we **must** give the eigenfunction of momentum:
$$
\begin{cases}
\langle x|p\rangle=\frac{1}{\sqrt{2\pi}}e^{ipx}\\
\langle p|x\rangle=\frac{1}{\sqrt{2\pi}}e^{-ixp}\\
\end{cases}
$$
The Fourier transform in quantum mechanical

### 8.3.2 Momentum and coordinate representation

#### 8.3.2.1 Eigenvalue

$$
\begin{cases}
\hat x|x'\rangle=x|x\rangle \\
\hat p|p'\rangle=p|p\rangle
\end{cases}
$$

#### 8.3.2.2 Eigenfunction

momentum as the cases
$$
\begin{cases}
\langle x|p\rangle=\frac{1}{\sqrt{2\pi}}e^{ipx}\\
\langle p'|p\rangle=\delta(p-p')\\
\end{cases}
$$

注意连续波无法归一到1, 只会归一到delta函数。
The form of plant wave is form FT ,<span style="color:magenta">But what is the evidence of the form of delta function? :</span>

> $$
 \langle p'|p\rangle=\int \langle p'|x\rangle dx\langle x|p\rangle =\frac{1}{2\pi}\int e^{i(p-p')x}dx=\delta(p-p')
 $$
>
> Or we could utilize another way
> $$
 \langle p|\psi\rangle=\int_{p'} \langle p|p'\rangle dp'\langle p'|\psi\rangle
 $$
> Evidently: $\langle p|p'\rangle =\delta(p-p')$
>
>8.4 Other math properties

数学区域证明过了

* 对角矩阵
1. 对角矩阵$AB-BA=0$ ,反映的是如果有一个表象，A,B都是对角阵即自身表象，说明A,B可以在同一个表象下表示，即对易。

2. 对角化：厄米和幺正算符都可以幺正对角化，因为他们本征基矢组完备。
* 幺正变化空间
1. 不改变**det, trace**, (可能只是厄米和幺正算符的)**本征值**，这是因为

$$
\begin{cases}
\det(AB)=\det(A)\cdot\det(B)\rightarrow \det(S^\dagger AS)=\det(A)\\
\det(AB)=\det(BA)\\
trace(AB)=trace(BA)\rightarrow trace(S^\dagger AS)=trace(A)\\
Known\quad  S^\dagger AS=A_d\quad or\quad AS=SA_d\rightarrow A=SA_dS^\dagger\rightarrow \\UAU^\dagger=(US)A_d(S^\dagger U^{\dagger})
\end{cases}
$$

显然本征值还是$A_d$只是对角化矩阵变了。

这是合理的，因为厄米或幺正算符的对角化也是幺正变化。那么如果还做一次幺正变化，这两次是可以合为一次的。
