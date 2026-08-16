# Chapter 4

<span style="color:red">本章用矩阵证明要快，但是狄拉克更优雅。有些狄拉克用了标积的写法。</span>
## 4.1 General rules

### 4.1.1 Linear fundamental rules

* $\hat O(c_1\psi_1+c_2\psi_2)$

* $\hat A\hat B|\psi\rangle=(\hat A\hat B)|\psi\rangle$ <font color=magenta>NOTICE：$\hat A$ could not act on $\hat B$ but as a new operator written as $\hat A\hat B$.</font> 

  In a general way, $[\hat A,\hat B]\neq 0$

* Fundamental **commute expression**

$$
\begin{cases}
[\hat A,\hat B\hat C]=\hat B[\hat A,\hat C]+[\hat A,\hat B]\hat C\\
[\hat A\hat B,\hat C]=\hat A[\hat B,\hat C]+[\hat A,\hat C]\hat B\\
[\hat F,\vec {\hat A}\cdot \vec{\hat B}]=\vec A\cdot [\hat F,\vec {\hat B}]+[\hat F,\vec {\hat A}]\cdot \vec{\hat B}\\
[\hat F,\vec {\hat A}\times \vec{\hat B}]=\vec A\times [\hat F,\vec {\hat B}]+[\hat F,\vec {\hat A}]\times \vec{\hat B}
\end{cases}
$$

> Notice：$\hat F$ is a scale. **目前没有矢量对易，矢量和标量爱因斯坦求和协定也只能求但方向。**

* **Reverse operator** : <font color=magenta>If the reverse operator is exist.</font>

$$
\begin{cases}
\hat A\hat A^{-1}=\hat I\\
[\hat A,\hat A^{-1}]=0\\
(\hat A\hat B)^{-1}=\hat B^{-1}\hat A^{-1}
\end{cases}
$$

* The **function of operator**

$$
F(\hat A)=\sum_n C_n \hat A^n
$$

<font color=lime>It function of operator is not the function of all the matrix elements, but the dig elements in eigenrepresation</font> <font color=magenta>Viz., the transform of $\exp{\hat A}$ is $ S* \exp{ \hat A} *S^\dagger$instead of $\exp{(S \hat A S^\dagger) }$</font>

* **Complex conjugate**

$$
\begin{cases}
\langle \psi|\varphi\rangle^*=\langle \varphi|\psi\rangle\\
(\hat A\hat B)^*=\hat A^*\hat B^*
 \end{cases}
$$

### 4.1.2 High-class operators operator

#### 4.1.2.1 Hermitian conjugate

* <font color=blue>Core</font>

<font color=magenta>$\hat F^\dagger$ is act on left bra.</font> For instance, If we assume: $\hat F|n\rangle=f_n|n\rangle$
$$
\langle n|\hat F^\dagger=f_n^* \langle n|
$$

* Definition

$$
\langle \psi|\hat O^\dagger|\varphi\rangle=\langle\hat O \psi|\varphi\rangle\rightarrow \langle \varphi|\hat O|\psi\rangle^*
$$
可以展开得到矩阵元素关系：$\langle m|\hat O^\dagger|n\rangle = (\langle n|\hat O|m\rangle)^*$
* properties

$$
\begin{cases}
\hat O^\dagger=\tilde{\hat O^*}\\
(\hat A\hat B)^\dagger=\hat B^\dagger \hat A^\dagger
\end{cases}
$$

Proof: 
$$
\langle \psi|(\hat A\hat B)^\dagger|\varphi\rangle=\langle \varphi|\hat A\hat B|\psi\rangle^*=\langle \hat A\varphi|\hat B\psi\rangle^*=\langle \hat B\psi|\hat A\varphi\rangle=\langle \psi|\hat B^\dagger\hat A^\dagger|\varphi\rangle
$$
求和容易证明。
#### 4.1.2.2 Hermitian operator

1. Definition

$$
\hat O^\dagger=\hat O
$$
2. properties

   * ==基本假设：力学量（测量量）是厄米算符。==
   * If $[A,B]=0、\hat A^\dagger=\hat A、\hat B^\dagger=\hat B\quad\Rightarrow (\hat A\hat B)^\dagger=\hat A\hat B$ 
* <font color=lime>To the Hermitian operator ,for any state, the mean value is real number.</font> 

$$
   \langle \psi|\hat O|\psi\rangle =
   \langle \psi|\hat O|\psi\rangle^*
$$
* <font color=lime>If the mean value is real number for any state, The operator is Hermite operator</font> 
  
   > This proof  need to take apart the state : $|\psi\rangle=|\psi_1\rangle+\lambda|\psi_2\rangle$ solve $\langle \psi|\hat O|\psi\rangle$ and set $\lambda=1,i$, then addition.

   * $\langle n|\hat F^\dagger\hat F|n\rangle\ge 0 \rightarrow \langle n|\hat O^2|n\rangle\ge 0$ for $\hat O$ is a hermitian operator.
   * <font color=lime>To the Hermitian operator ,for any eigenstate, the mean value is real number.</font> proof similar as mean value
   * <font color=lime>To the Hermitian operator ,for **different eigenvalue**, relevant eignefunction is orthometric;for **common eigenvalue**, relevant eignefunction is not  necessarily orthometric,but we could find a goups of $Q_n$ meet $\langle m\alpha|m\alpha'\rangle=\delta_{\alpha\alpha'}$</font> 
   
   > Proof :
   >
   > 1. different eigenvalue
   >
   >  For a hermitian operator, Known
   >$$
    \begin{cases}
    \hat O|m\rangle= O_m|m\rangle\\
    \hat O|n\rangle= O_n|n\rangle\\
    \end{cases}\\
    \Rightarrow 
    \langle m|\hat O|n\rangle=\begin{cases}
    O_n\langle m|n\rangle\\
    \langle n|\hat O|m\rangle^*=O_m^*\langle m|n\rangle\\
    \end{cases}\\
    \Rightarrow (O_m-O_n)\langle m|n\rangle=0
    $$
   > Evidently, For hermitian operator, if $m\neq n$, $\langle m|n\rangle=0$
   > 
   > 2. common eigenvalue
   >
   > exit the way to find a group of basic vector of $O_m$ meet:
   >$$
    \langle m\alpha|m\alpha'\rangle=\delta_{\alpha\alpha'}
$$
   > <font color=magenta> Therefore, directly using groups of quantum numbers (eigenvalues) to label quantum states is not entirely precise. However, we can assume that a state labeled by a set of quantum numbers is a linear combination of the degenerate states associated with those quantum numbers, satisfying $\langle \lambda' m'|\lambda m\rangle=\delta_{\lambda'\lambda}\delta_{m'm}$</font>


补充：

* $(i\hat F)^\dagger=-i\hat F^\dagger$ 
* If $\hat F|n\rangle =f_n|n\rangle$ Now the question : $\langle m|\hat F^\dagger=f_m^* \langle m|$ <font color=magenta>But it could act on right ket</font>

Proof(哪有那么复杂，当时不熟):
>$$
\langle m|\hat F^\dagger|n\rangle=\sum_m \langle m|\hat F^\dagger|m'\rangle\langle m'|n\rangle=\sum_{m'} \langle m'|\hat F|m\rangle^*\langle m'|n\rangle\\
=\sum_{m'}f_m^*\langle m|m'\rangle \langle m'|n\rangle=f_m^*\langle m|n\rangle
$$
>

#### 4.1.2.3 Transposed operator

1. Definition
$$
\langle \psi|\tilde {\hat O}|\varphi\rangle=\langle \varphi^*|\hat O^\dagger|\psi^*\rangle^*=\langle \psi|(\hat O^\dagger)^ *|\varphi\rangle
$$
2. properties
$$
\tilde{(\hat A\hat B)}=\tilde{\hat B}\tilde{\hat A}
$$
<font color=magenta>Proof:</font> 
$$
\langle \psi|\tilde{(\hat A\hat B)}|\varphi\rangle=\langle \psi|{(\hat A\hat B)^\dagger }^ *|\varphi\rangle=\langle \psi|{(\hat B^\dagger\hat A^\dagger) }^ *|\varphi\rangle=\langle \psi|\tilde{\hat B} \tilde {\hat A} |\varphi\rangle
$$
## 4.2 Commute relationship and CSCO

### 4.2.1 Uncertainty relation

1. Definition
$$
\Delta \hat A\Delta \hat B\ge\frac{|\langle[\hat A,\hat B]\rangle|}{2}
$$
proof: $|\phi\rangle = \hat A + i\lambda \hat B |\psi\rangle, where \langle \psi|\psi \rangle =1, \lambda = real. \therefore \langle \phi |\phi\rangle \ge 0$, then solve the function of $\lambda$.
2. Meaning

* For **non-commute mechanical quantities**, They have <font color=lime>no precise measure value at a same time, generally.</font> 
* For **commute mechanical quantities**, <font color=lime>They must have a simultaneous states.</font>
* for different state$|n\beta'\rangle$ and $|n\beta\rangle$ , $B_{\beta'}=B_\beta$ could be apparent. Then we need more quantities to open degenerate to determine the single state of system when $\Delta A=0,\Delta B=0$ <font color=magenta>这种属于完全简并，也就两组本征值完全相同；对于给这两个力学量找个共同本征态可以认为完成了，但是现在不能用这组基矢组成csco，必须加力学量。这是自由度要求。</font>
* <font color=magenta> Therefore, directly using groups of quantum numbers (eigenvalues) to label quantum states is not entirely precise. However, we can assume that a state labeled by a set of quantum numbers is a linear combination of the degenerate states associated with those quantum numbers, satisfying $\langle \lambda' m'|\lambda m\rangle=\delta_{\lambda'\lambda}\delta_{m'm}$</font>

>For the second point, it is tough to proof. 
>
>assume there are two mechanical quantities :$[\hat A,\hat B]=0$ 
>
>1. non-degenerate state
>
><font color=lime>Assume there a **non-degenerate state** $|n\rangle$ for $\hat A$。Then $|n\rangle$ have been the basic of $\hat A$ and $\hat B$</font>
>
>
>2. degenerate state
>
>
>> 这里只是证明**对易力学量一定有共同本征态**，但：
>>
>> 1. 关于CSCO未提及。
>> 2. <font color=magenta>没有说不对易就没有共同本征态。也没有说有共同本征态就对易了。</font>
>> 3. 一个物理图像，以表示共同本征态，也即使用两个力学量测量某个态,交换作用三次。
>>
>> 对于所有作用结果可能，有：
>> $$
>> \sum_{a'ab}|\psi_{a'}\rangle \langle \psi_{a'}|\psi_b\rangle \langle \psi_b|\psi_a\rangle \langle \psi_a|\psi\rangle
>> $$
>> 如果有共同本征态，也即$\langle \psi_b |\psi_a\rangle$

### 4.2.2 判断是是否是共同本征态

4.2.2.1 唯一标准

对于$|\psi\rangle、\hat A、\hat B$满足
$$
\begin{cases}
\hat A|\psi\rangle=a|\psi\rangle\\
\hat B|\psi\rangle=b|\psi\rangle
\end{cases}
$$
a、b是常数。

4.2.2.2 找非对易但是有共同本征态

我们可以通过$[\hat A,\hat B]|\psi\rangle=\hat C|\psi\rangle=0$ 去找$|\psi\rangle$

> Case: $[\hat j_z,j_+]|\overline m\rangle=j_+|\overline m\rangle=0$

### 4.2.3 CSCO and CSCCO

#### 4.2.3.1 CSCO

1. Definition 

* <font color=blue>Independent</font> and

* <font color=blue>**mutually** commuting</font> 

* <font color=blue>Hermitian operators</font> 

* <font color=lime>Completeness and **Uniqueness**</font>

 form a set of observables in a system.

>关于 CSCO, 再做几点说明: 
>
>(1) <font color=magenta>满足上述条件确实一定可以找到CSCO,但是不容易证明。</font>
>
>(2) CSCO 是限于最小集合, 即从集合中抽出任何一个可观测量后, 就不再构成体系的 CSCO. 所以要求 CSCO 中各观测量是函数独立的.
>
>(2) 一个给定体系的 CSCO 中, 可观测量的数目一般等于体系自由度的数目, 但也可以大于体系自由度的数目 (见下列练习 1.2).
>
>(3) 一个给定体系往往可以找到多个 CSCO, 或 CSCCO. 在处理具体问题时, 应视其侧重点来进行选择. 一个 CSCCO 的成员的选择, 涉及体系的对称性.

2. Properties

* <font color=lime>We do not permit groups of mechanical quantities to be completely degenerate in a CSCO. If this occurs, add more observables to reconstruct the CSCO in order to maintain Completeness and Uniqueness.</font>
$$
  [E_i, p_i, \ldots] \neq [E_j, p_j, \ldots]
$$

In contrast to the above statement, we further ensure the uniqueness of the system.

> <font color=magenta>Therefore, directly using groups of quantum numbers (eigenvalues) to label quantum states is not entirely precise. However, we can assume that a state labeled by a set of quantum numbers is a linear combination of the degenerate states associated with those quantum numbers, satisfying $\langle \lambda' m'|\lambda m\rangle = \delta_{\lambda'\lambda} \delta_{m'm}$.</font>

* <font color=lime>Any state of this system could be expressed the addition of this common state groups</font>
$$
|\psi\rangle =\sum_{n\alpha...}|n\alpha...\rangle\langle n\alpha...|\psi\rangle
$$
#### 4.2.3.2 CSCCO

1. Definition

* <font color=blue>CSCO</font>
* <font color=blue>$\hat H$ without time is in this set</font>

2. Properties

* All the Hermitian operators in this set are conserved quantities.
* <font color=lime>Natural system could belong to CSCCO</font>

### 4.2.4 Specific cases

#### 4.2.4.1 Angular momentum

##### 4.2.3.4.1 Fundamental commute relationship

* Definition
$$
l_i=\epsilon_{ijk}x_jp_k
$$
* commute relationship
$$
\begin{cases}
[x_i,p_j]=i\delta_{ij}\\
[l_i,x_j]=i\epsilon_{ijk}x_k\\
[l_i,p_j]=i\epsilon_{ijk}p_k\\
[l_i,l_j]=i\epsilon_{ijk}l_k\\
[l^2,l_i]=0
\end{cases}
$$
* **proof cases**:
$$
\begin{cases}
[l_i,x_j]=\varepsilon_{i\beta\gamma}[x_\beta p_{\gamma},x_j]=\varepsilon_{i\beta\gamma}x_\beta[p_\gamma,x_j]=-i\varepsilon_{i\beta\gamma}x_\beta\delta_{\gamma j}=i\varepsilon_{ij\beta }x_\beta\\
[l_i,l_j]=\epsilon_{j\beta \gamma}[l_i,x_\beta p_\gamma]=\epsilon_{j\beta\gamma}(x_\beta[l_i,p_\gamma]+[l_i,x_\beta]p_\gamma)=i\epsilon_{j\beta\gamma}\epsilon_{i\gamma n}x_\beta p_n+i\epsilon_{j\beta\gamma}\epsilon_{i\beta o}x_op_\gamma \\
=i(\delta_{nj}\delta_{i\beta}-\delta_{n\beta}\delta_{ij})x_{\beta}p_n+i(\delta_{o\gamma}\delta_{ij}-\delta_{oj}\delta_{i\gamma})x_op_\gamma =ix_ip_j-i\delta_{ij}x_\beta p_\beta+i\delta_{ij}x_op_o-ix_jp_i\\=i(x_ip_j-x_jp_i)+i\delta_{ij}(x_op_o-x_\beta p_\beta)=i(x_ip_j-x_jp_i)=i\epsilon_{ijk}l_k
\end{cases}
$$
##### 4.2.3.4.2 CSCO For $[\hat l^2,\hat l_z]$

* Premise
$$
\hat l_z|\psi\rangle=m|\psi\rangle
$$
* Equation
$$
\hat l^2 |\psi\rangle=\lambda^2 |\psi\rangle
$$
* Solution
$$
|lm\rangle,where\begin{cases}
\lambda^2=l(l+1)\\
l\in {\N}\ \
m=-l,-l+1,...,l
\end{cases}
$$
Specific representation :
$$
\langle \theta ,\varphi|lm\rangle=Y_l^m(\theta.\varphi)=N_l^m P_l^m(\cos\theta)e^{im\varphi}\\
where \quad N_l^m=(-1)^m\sqrt{\frac{(l-m)!}{l(l+m)!}\frac{(2l+1)}{4\pi}}
$$
* properties
$$
\begin{cases}
\langle lm|l'm'\rangle=\delta_{ll'}\delta_{mm'}\\
\langle \theta\varphi|\hat P|lm\rangle=\langle -\theta \varphi|\hat {P}|lm\rangle
\end{cases}
$$
> $$
> \begin{cases}
> \theta=\arctan(\frac{\sqrt {x^2+y^2}}{z})\\
> \varphi=\arctan(\frac{y}{x})
> \end{cases}
> $$

##### 4.2.3.4.2 algebraic method For $[\hat l^2,\hat l_z]$

1. premise

* Definition of angular momentum :
$$
\begin{cases}
[j_\alpha,j_\beta]=i\epsilon_{ijk}j_\gamma\\
[j^2,j_\alpha]=0
\end{cases}
$$
According to $[j^2,j_z]=0$, assume they common eigenstate :$|\lambda m\rangle$.

> <font color=magenta> Therefore, directly using groups of quantum numbers (eigenvalues) to label quantum states is not entirely precise. However, we can assume that a state labeled by a set of quantum numbers is a linear combination of the degenerate states associated with those quantum numbers, satisfying ⟨λ' m'...|λ m...⟩ = δ_{λ'λ} δ_{m'm}...</font>
$$
\begin{cases}
\langle\lambda' m'|j^2|\lambda m\rangle=\lambda\delta_{\lambda'\lambda}\delta_{m'm}\\
\langle\lambda' m'|j_z|\lambda m\rangle=m\delta_{\lambda'\lambda}\delta_{m'm}\\
\end{cases}
$$
Construct : 
$$
\begin{cases}
j_+=j_x+ij_y\\
j_-=j_x-ij_y=(j_+)^\dagger
\end{cases}
$$
commute relations
$$
\begin{cases}
[j_z,j_\pm]=\pm j_\pm\\
[j_+,j_-]=2j_z\\
\{j_+,j_-\}=2(j^2-j_z^2)
\end{cases}
$$
2. <font color=lime>quantum numbers groups range</font>
$$
\begin{cases}
j\in\frac{\N}{2}\\
m=-j,-j+1,...,j\\
\lambda^2=j(j+1)\\
\end{cases}
$$
> Proof :
>
> <font color=magenta>m、$\lambda$ is real numbers</font>
>
> * $\lambda$ room demand
>
> $$
> \langle\lambda' m' |[j^2,j_\pm]|\lambda m\rangle=0\Rightarrow(\lambda'-\lambda)\langle \lambda' m'|j_\pm|\lambda m\rangle=0\\
> Viz., \langle \lambda' m'|j_\pm|\lambda m\rangle=\delta_{\lambda'\lambda}\langle \lambda' m'|j_\pm|\lambda m\rangle
> $$
>
> * $m$ room demand
>
> $$
> \langle \lambda' m'|[j_z,j_\pm]|\lambda m\rangle=\pm\langle \lambda' m'|j_\pm|\lambda m\rangle
> \Rightarrow (m'-m\mp1)\langle \lambda m'|j_\pm|\lambda m\rangle=0\\
> Viz., \langle \lambda' m'|j_\pm|\lambda m\rangle=\delta_{m'm\pm 1}\langle \lambda' m'|j_\pm|\lambda m\rangle
> $$
>
> In conclusion, 
> $$
> \langle \lambda' m'|j_\pm|\lambda m\rangle=\delta_{\lambda'\lambda}\delta_{m'm\pm 1}\langle \lambda' m'|j_\pm|\lambda m\rangle
> $$
>
> * m and $j$ number range demand
>
> According to
> $$
> \langle m|[j_+,j_-]|m\rangle=\begin{cases}
> \langle m|2j_z|m\rangle=2m\\
> |\xi_{m-1}|^2-|\xi_m|^2
> \end{cases}\\
> where\quad \xi_m=\langle m+1|j_+|m\rangle
> $$
> Viz., 
> $$
> \begin{cases}
> |\xi_{m-1}|^2-|\xi_m|^2=2m\\
> |\xi_m|^2\ge0
> \end{cases}
> $$
> assume the form of solution :
> $$
> |\xi_m|^2=C-m(m+1)\ge0\rightarrow m(m+1)\le C
> $$
> Evidently exist $\overline{m}$ and $\underline{m}$ . Then $|\underline{m}-1\rangle$ or $|\overline {m}+1\rangle$ should be not exist. The core conflict is how to explain: 
> $$
> \begin{cases}
> \xi_\overline{m}=\langle \overline m+1|j_+|\overline m\rangle\\
> \xi_\underline{m}=\langle \underline m-1|j_-|\underline m\rangle^*\\
> \end{cases}
> $$
>
> <font color=magenta>Year, they should not exist, we must make the questions disappear before they exist </font>, which means:
> $$
> \begin{cases}
> j_+|\overline{m}\rangle=0 \rightarrow \xi_\overline{m}=0\\
> j_-|\underline{m}\rangle=0 \rightarrow \xi_\underline{m}=0
> \end{cases}\\
> \Rightarrow \overline{m}=-\underline{m}
> $$
> Assume $\overline{m}=j$ , Evidently:
> $$
> j-(-j)=\N\quad \text {m changes in steps of 1:}\\
> \Rightarrow\begin{cases}
> j\in\frac{\N}{2}\\
> m=-j,-j+1,...,j\\
> C=j(j+1)
> \end{cases}
> $$
> * The relationship of $j$ and $\lambda$
>
> According to: $\{j_+,j_-\}=2(j^2-j_z^2)$
> $$
> \langle \lambda m|j^2|\lambda m\rangle=\langle \lambda m|\frac{1}{2}\{j_+,j_-\}+j_z^2|\lambda m\rangle\\
> \Rightarrow\lambda^2=\frac{1}{2}(\sum_{m'}\langle m|j_+|m'\rangle\langle m'|j_-|m\rangle+\sum_{m'}\langle m|j_-|m'\rangle\langle m'|j_+|m\rangle)+m^2\\
> \Rightarrow\lambda^2=\frac{1}{2}(|\langle m|j_+|m-\rangle|^2+|\langle m+1|j_+|m\rangle|^2)+m^2\\
> Viz.,\lambda^2=j(j+1)
> $$

3. The Matrix elements
$$
\begin{cases}
\langle j' m'|j_+|j m\rangle=\sqrt{\lambda^2-m(m+1)}\delta_{j'j}\delta_{m'm\pm 1}\\
\langle j' m'|j_-|j m\rangle=\langle j m|j_+|j' m'\rangle^*
\end{cases}
$$

> Proof :
>
> Known:
> $$
 \begin{cases}
 \langle \lambda' m'|j_\pm|\lambda m\rangle=\delta_{\lambda'\lambda}\delta_{m'm\pm 1}\langle \lambda' m'|j_\pm|\lambda m\rangle\\
 \xi_m=\langle m+1|j_+|m\rangle\\
 |\xi_m|^2=j(j+1)-m(m+1)
 \end{cases}
 $$
> <font color=magenta>Because the phase uncertainty, we choose:</font>
> $$
 \begin{cases}
 \langle m+1|j_+|m\rangle=\sqrt{j(j+1)-m(m+1)}\\
 \langle m-1|j_-|m\rangle=\langle m|j_+|m-1\rangle^*
 \end{cases}
 $$


## 证明问题

* stationary state $\rho$, $j$, $\langle F \rangle$, $\langle m|n\rangle$ is stationary.
* proof $AA^{-1} = I$, $AA^{-1} = \hat I$
* Why does matrix multiplication satisfy the combination rate.
* proof $(AB)^\dagger=B^{\dagger}A^{\dagger}$, $A^\dagger$
* Drive the definition of transposition
* if A, B is Hermitian operator, proof $(AB)^\dagger$ properites
* if $\hat O$ is a Hermitian operator, proof $\langle \hat O\rangle$ is real; if $\langle \hat O \rangle$ is real constantly, prrof $\hat O$ is a Hermitian operator.
* proof $\langle \hat O^2 \rangle \ge 0$ for hermitian operator. Proof $\langle \hat F^\dagger \hat F \rangle \ge 0$
* proof eigenstate is orthogonal for differ eigenvalue for hermitian operator.
* 不确定度关系证明
* $|\psi\rangle = \hat F |\phi\rangle$, 如果$|\phi\rangle$是量子态，$|\psi\rangle$ 一定是量子态吗？$\langle \psi|\psi\rangle$为什么大于等于0？
* $[A, B]=0$ 是其有共同本证态的什么条件？
* 证明$[A, B] = 0$下，一定可以找到A,B的共同本证态。
* CSCO和CSCCO定义
* 为什么力学量用线性厄米算符表示？