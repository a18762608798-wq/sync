# 3 Second law of thermodynamics

## 3.1 concepts of evolutionary direction

### 3.1.1 the statement of second law

#### 3.1.1.1 Kelvin's statement

**It is impossible to absorb heat from a single source to make it be totally useful work without other influences.**

Or **the second category of perpetual motion machine could not be made.**

<!--which reflect the non reversibility of the process of "work to heat"-->

#### 3.1.1.2  Clausius' statement

**It is impossible to transmit the heat from cryogenic body to hot body without other influences.**

<!--which reflect the non reversibility of teat transfer strictly.-->

#### 3.1.1.3  the relationship of two statement

**They are equal** and must set up at same time, which could be proof through thinking experiment to construct conflict machine. 

To sum up, all the thermodynamics process have non reversibility.

### 3.1.2 the <span style="color:blue">reversibility process</span> and non

#### 3.1.2.1 non reversibility

* Definition: After the process, the system **could not to recover** without any vary.

* Condition: All the **dissipative effect**(the increase of U not from Q) and unbalanced effect.

* Cases: work to heat, heat transfer. 

#### 3.1.2.2 reversibility

* Definition: After the process, <font color=blue>the system could to recover without any vary.</font>

* Cases: The **ideal quasi-static** process without dissipative effect; <font color=orange>such as the quasi-static circulation without dissipative effect.</font>

## 3.2 The quasi-static circulation

### 3.2.1 The Carnot heat engine

1. Definition: **isothermal and adiabatic** circulation. <font color=magenta>Start from up left and adiabatic with high temperature T_1</font>

2. Effect: 

heat engine
$$
\eta=\frac{A}{Q_{12}}=\frac{Q_{12}+Q_{34}}{Q_{12}}
$$
refrigerator
$$
\varepsilon=\frac{Q_{34}}{A'}=\frac{Q_{34}}{-A}=\frac{Q_{34}}{-(Q_{12}+Q_{34})}\quad ({Q_{34}>0})
$$

### 3.2.1 The Carnot theorem

1. content

* <span style="color:lime">The effect of any reversible heat engine between **two common heat source** is common. </span>

* The effect of reversible heat engine is maximum among any heat engine. 

2. Extent

* ==The effect of Carnot heat is equal with any reversible heat engine **between two common heat source**.==

$$
\eta=1-\frac{T_2}{T_1}
$$

* refrigerator (**similar as Carnot heat**)

$$
\varepsilon=\frac{T_2}{T_1-T_2}
$$

## 3.3 Thermodynamic scale

### 3.3.1 premise

According to the fixed effect of reversible heat engine between two fixed heat source ($\theta_1$,$\theta_2$):
$$
f(\theta_1,\theta_2)=\frac{1}{1-\eta}=-\frac{Q_1}{Q_2}
$$
Because the **general rules**
$$
-\frac{Q_1}{Q_2}=f(\theta_1,\theta_2)=\frac{\varphi(\theta_2)}{\varphi(\theta_2)}
$$
Which is the general law !!! **We could should any form of** $\varphi(\theta)$ .
$$
\varphi(\theta)=CT
$$
Thus :
$$
-\frac{Q_1}{Q_2}=\frac{T_2}{T_1}
$$

### 3.3.2 Definition

$$
\begin{cases}
\frac{T}{T_{tr}}=-\frac{Q}{Q_{tr}}\\
T_{tr}=273.16K
\end{cases}
$$

Which definite temperature <font color=orange>via the absorb the heat(**The process of adiabatic**) of ideal reversibility engine</font> , which just set up from **Carnot theorem** and first law of thermodynamics. 

## 3.4 Entropy

### 3.4.1 Entropy

1. premise

From the thermodynamics scale, Meaning **the isothermal process** of Carnot circulation. 
$$
\frac{Q_1}{T_1}+\frac{Q_2}{T_2}=0
$$

<span style="color:magenta">The adiabatic process $Q=0$ evidently。</span>

Viz., For Carnot circulation(also for **reversible circulation(could be divided into Carnot circulation)**) :

<span style="color:blue">**Clausius equality**</span>
$$
\min\oint \frac{\delta Q}{T}=0
$$

2. Definition

Though Clausius equality, give the definition : <span style="color:magenta">微分关系也要求可逆过程,但是我确实看到一般不加，应该是认为T不变时系统变化慢，准静态过程自然可逆。但是不太严谨，可能化学状态改变。</span>
$$
\begin{cases}
dS=\frac{\delta Q}{T} \text{可逆过程}\\
\Delta S(T,...)=\max\int_{a }^b \frac{\delta Q}{T}
\end{cases}
$$

<span style="color:orange"> 由此可逆绝热过程 $\Delta S=\int_{可逆} \frac{\delta S}{T}=0$ </span>

### 3.4.2 the laws of the addition of entropy 

1. Definition

**in adiabatic system** (include **incentive system**), $\oint \frac{\delta Q}{T}=0$, thus :
$$
\Delta S\ge 0
$$

2. properties

==This law is equal with the second laws of thermodynamic law==

### 3.4.3 应用

对于某过程计算熵增，一般来说等效可逆过程选择**定压和定容**，因为温度态函数好积分。