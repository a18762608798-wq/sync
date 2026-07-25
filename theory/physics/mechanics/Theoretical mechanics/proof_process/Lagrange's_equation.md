Basic on ideal constraint, we has known:
$$
\begin{cases}
\delta r_i = \frac{\partial r_i}{\partial q_\alpha}\delta q_\alpha + \frac{\partial r_i}{\partial t}\delta t = \frac{\partial r_i}{\partial q_\alpha}\delta q_\alpha\\
(F_i - (m \ddot{r})_i)\cdot \delta r_i = 0
\end{cases}
$$
Evidently:
$$
F_i \cdot \frac{\partial r_i}{\partial q_\alpha}\delta q_\alpha - (m \ddot{r})_i\cdot \frac{\partial r_i}{\partial q_\alpha}\delta q_\alpha = 0
$$
Let:
$$
\begin{cases}
Q_\alpha = F_i \cdot \frac{\partial r_i}{\partial q_\alpha}
 \\
P_\alpha = (m \ddot{r})_i\cdot \frac{\partial r_i}{\partial q_\alpha} = \frac{d}{dt}[(m\dot{r})_i\frac{\partial r_i}{\partial q_\alpha}] - (m\dot r)_i\frac{d}{dt}\frac{\partial {r_i}}{\partial q_\alpha}\tag{1}
\end{cases}
$$
so much for that, now we proof a commute relationship:
premise:
$$
\dot r_i = \frac{\partial r_i}{\partial q_\alpha}\cdot \dot{q}_\alpha + \frac{\partial r_i}{\partial t} 
$$
therefore:
$$
\frac{\partial \dot{r_i}}{\partial \dot q_\alpha} = \frac{\partial r_i}{\partial q_\alpha} \tag{2}
$$
Evidently $\frac{\partial r_i}{\partial q_\alpha}$ is a function of $q_\alpha$ and $t$, therefore: 
$$
\frac{d}{dt}[\frac{\partial r_i}{\partial q_\alpha}]=
\frac{\partial ^2r_i}{\partial q_\alpha \partial q_\beta}\dot q_\beta + \frac{\partial^2 r_i}{\partial q_\alpha \partial t} = \frac{\partial}{\partial t} \dot{r}_i
$$
therefore:
$$
[\frac{d}{dt}, \frac{\partial}{\partial q_\alpha}]r_i = 0 \tag{3}
$$

To sum up, substitute equation (3),(2) into equation (1).
$$
P_\alpha = \frac{d}{dt}[(m\dot{r})_i^o\frac{\partial \dot r_i^o}{\partial \dot q_\alpha}] - (m\dot r)_i^o \frac{\partial \dot r_i^o}{\partial q_\alpha} = \frac{d}{dt}(\frac{\partial T}{\partial \dot q_\alpha}) - \frac{\partial T}{\partial q_\alpha}
$$
where: 
$$
T = \frac{1}{2}(m \dot r)_i^o r_i^o
$$
also:
$$
(Q_\alpha - P_\alpha)\cdot \delta q_\alpha = 0
$$
which is meet for all the $q_\alpha$, so evidently: 
$$
\frac{d}{dt}(\frac{\partial T}{\partial \dot q_\alpha}) - \frac{\partial T}{\partial q_\alpha} = Q_\alpha 
$$
