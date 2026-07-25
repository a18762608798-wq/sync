# Chapter 5: analytical mechanics 

## 5.1 The category of constraint
* whether time is included
$$
\begin{cases}
stability\quad constraint:f(x) = 0\\
unstability\quad constraint: f(x, t) = 0
\end{cases}
$$
* equality or not
$$
\begin{cases}
Unsolvable\quad constraint: f(x,t) = 0\\
solvable\quad constranint: f(x,t) \le 0
\end{cases}
$$
* whether it contains generalized velocities
$$
\begin{cases}
Geometric\quad constraints: f(x,t) = 0\\
Kinematic\quad constraints: f(x,\dot{x},t) = 0
\end{cases}
$$
if kinematic constraints could be integral to geometric constraints, we also call it **holonomic constraints**, or we will call it Nonholonomic constraints.
If a system has nonholonomic constraints, we call it nonholonomic system. or we call it holonomic system.
<span style="color:red">we only research holonomic system generally.</span>
* ideal constraint:
only a constraint:
$$
\sum_{\alpha = 1}^s F_{ri}\cdot \delta_{r_1} = 0
$$
## 5.2 Principle of virtual work
* premise: ideal constraint
* content:
$$
\sum_{i=1}^n(F_i-m_i\ddot{r_i})\cdot \delta r_i = 0
$$
where $F_i$ we only think about applied forces.
* proof: [[./proof_process/Principle_of_virtual_work]]^
## 5.3 Lagrange's equation
### 5.3.1 general rules
* **premise: ideal constraint**
$$
\sum_{\alpha=1}^s F_{ri}\cdot \delta r_i = 0
$$
* content:
$$
\frac{d}{dt}(\frac{\partial T}{\partial \dot{q}_\alpha})-\frac{dT}{\partial q_\alpha}=Q_{\alpha}\quad(\alpha=1,2,3,...,s)
$$
where $Q_{\alpha}$ is generalized force.
* proof: [[./proof_process/Lagrange's_equation]]
### 5.3.2 lagrange's equation of conservative system
$$
\frac{d}{dt}(\frac{\partial L}{\partial \dot{q}_\alpha})-\frac{dL}{\partial q_\alpha}=0\quad(\alpha=1,2,3,...,s)
$$
where:
$$
L=T-V
$$
proof: [[./proof_process/lagrange's_equation_of_conservative_system]]
### 5.3.3 application
#### 5.3.3.1 cyclic coordinate
* Definition: $\frac{\partial L}{\partial q_{\alpha}}=0$
* Property: $\frac{\partial L}{\partial \dot{q_{\alpha}}}=constant$
#### 5.3.3.2 energy integral
* premise: **conservative system**
$$
T=T_0+T_1+T_2 
$$
where:
$$
\begin{cases} 
T_0 = \frac{1}{2}a\\\
T_1 = \sum_{\alpha = 1}^s a_{\alpha}\dot{q}_\alpha\\\
T_2 = \frac{1}{2}\sum_{\alpha,\beta=1,1}^s a_{\alpha\beta}\dot{q}_\alpha \dot{q}_\beta
\end{cases}
$$
* content:
if $T$ is a **homogeneous function(n=2)** of generalized velocity, which mean the **constraint is stabled**.
$$
E=T+V
$$
otherwise:
$$
-T_0+T_2+V = h
$$
* proof: [[./proof_process/energy_integral_of_Lagrange's_equation]]
#### 5.3.3.3 general thinking process
- determination of system freedom.
- chose a group of generalized coordinate equal to freedom degree.
- compute $L$ and solve lagrange's equation.

## 5.5 Hamilton's canonical equations

### 5.5.1 general rule
* premise: **conservative system** and **ideal constraint**
* content:
$$
\begin{cases}
\dot {q}_\alpha = \frac{\partial H}{\partial p_\alpha}\\\
\dot{p}_\alpha = -\frac{\partial H}{\partial q_\alpha}\\\
\frac{\partial H}{\partial t} = -\frac{\partial L}{\partial t}\quad (\alpha = 1,2,...,s) 
\end{cases}
$$
or a elegant form:
$$
\begin{cases}
\dot{p}_\alpha = [p_\alpha, H]\\\
\dot{q}_\alpha = [q_\alpha, H]
\end{cases}
$$
where：
$$
p_\alpha = \frac{\partial L}{\partial \dot{q}_\alpha}\rightarrow \dot{p}_\alpha = \frac{\partial L}{\partial q_\alpha}
$$
* proof: [[./proof_process/Hamilton's_canonical_equations]]
### 5.5.2 application
#### 5.5.2.1 energy integral
* premise: 
$$
\frac{d H}{dt} = [H,H] + \frac{\partial H}{\partial t} = \frac{\partial H}{\partial t} = 0
$$
* conclusion:
$$
H = \begin{cases}
T+V\quad (stabled\quad constraint)\\\
T_2-T_0+V
\end{cases}
$$
* proof: [[./proof_process/energy_integral_of_Hamilton's_canonical_equations]]
5.5.2.2 Poisson bracket
* Definition:
$$
[\varphi,H]=\sum_{\alpha=1}^{s}(\frac{\partial \varphi}{\partial q_{\alpha}}\frac{\partial H}{\partial p_\alpha}-\frac{\partial \varphi}{\partial p_\alpha}\frac{\partial H}{\partial q_\alpha})
$$
it comes from:
$$
\frac{d\varphi}{dt} = \frac{\partial \varphi}{\partial t}+[\varphi, H]
$$
* properties:
If $\varphi=C$ , which means $\varphi$ is a conservative quantum.
$$
\therefore \frac{d\varphi}{dt} = 0 \Rightarrow \frac{\partial \varphi}{\partial t} + [\varphi,H] = 0
$$
meanwhile, if:
$$
\begin{cases}
\varphi_1 = C_1\\
\varphi_2 = C_2
\end{cases}
$$
Evidently:
$$
[\varphi_1, \varphi_2] = C_2
$$
## 5.7  Hamilton's principle
### 5.7.1 foundational form
* premise: 
$$
\begin{cases}
\delta t = 0\\
\delta q_\alpha|_{P_1} = 0\\
indel\quad constraint\\
conservative \quad quantum
\end{cases}
$$
Evidently:
$$
\begin{cases}
[\delta, d]q_\alpha = 0\\
[\delta, \frac{d}{dt}]q_\alpha = 0
\end{cases}
$$
* conclusion:
$$
\delta S=\delta\int_{t_1}^{t_3}  L dt = 0
$$
* proof: [[./proof_process/Hamilton's_principle]]
