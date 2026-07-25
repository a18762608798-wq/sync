Basic on: 
$$
T = \sum_{i,o}\frac{1}{2} m_i \dot r_i^o \dot r_i^o \tag{1}
$$
where: 
$$
\dot r_i^o = \sum_\alpha \frac{\partial \dot r_i^o}{\partial q_\alpha} \delta \dot q_\alpha + \frac{\partial r_i^o}{\partial t} \tag{2}
$$
substitute equation (2) into equation (1).
$$
\begin{split}
T  &= \frac{1}{2}\sum_{i,o} m_i (\sum_\alpha \frac{\partial \dot r_i^o}{\partial q_\alpha} \delta \dot q_\alpha + \frac{\partial r_i^o}{\partial t})(\sum_\beta \frac{\partial \dot r_i^o}{\partial q_\beta} \delta \dot q_\beta + \frac{\partial r_i^o}{\partial t}) \\
& =\frac{1}{2} \sum_{i, o, \alpha, \beta}m_i \frac{\partial \dot r_i^o}{\partial q_\alpha}\frac{\partial r_i^o}{\partial q_\beta}\delta \dot q_\alpha \delta \dot q_\beta + \sum_{i,o,\alpha,\beta}m_i\frac{\partial \dot r_i^o}{\partial q_\alpha}\frac{\partial r_i^o}{\partial t}\delta \dot q_\alpha + \frac{1}{2}\sum_{i,o,\alpha,\beta} \frac{\partial r_i^o}{\partial t}\frac{\partial r_i^o}{\partial t}\\
&= \frac{1}{2}\sum_{\alpha \beta}a_{\alpha,\beta}\delta\dot q_\alpha\delta\dot q_\beta + \sum_{\alpha,\beta} a_\alpha \delta\dot q_\alpha + \frac{1}{2}a\\
& = T_2 + T_1 + T_0 
\end{split} \tag{3}

$$

so much for that, now we proof the integral form.
Basic on(**conservative system**), and t is not a variable of V.
$$
\frac{d}{dt} (\frac{\partial T}{\partial \dot q_\alpha}) - \frac{\partial T}{\partial q_\alpha} = -\frac{\partial V}{\partial q_\alpha} = -\frac{d V}{dq_\alpha}  
$$
times $\dot q_\alpha$,  and $V(q_\alpha)$
$$
\frac{d}{dt} (\frac{\partial T}{\partial \dot q_\alpha})\dot q_\alpha - \frac{\partial T}{\partial q_\alpha}\dot q_\alpha = -\frac{d V}{d q_\alpha}\dot q_\alpha = -\frac{dV}{dt}  \tag{4}
$$
where: 
$$
\frac{d}{dt}(\frac{\partial T}{\partial \dot q_\alpha})\dot q_\alpha = \frac{d}{dt}(\frac{\partial T}{\partial \dot q_\alpha} \dot q_\alpha) - \frac{\partial T}{\partial \dot q_\alpha}\ddot q_\alpha  \tag{5}
$$
substitute (5) into (4), notice $T_2, T_1$ is a homogeneous equation of $q_\alpha$  
$$
\begin{split}
\frac{d}{dt}(\frac{\partial T}{\partial \dot q_\alpha}\dot q_\alpha) - \frac{dT}{dt} = -\frac{dV}{dt} \\
left = \frac{d}{dt}(2T_2+T_1-T)=\frac{d}{dt}(T_2 - T_0)\\
\end{split}
$$
Viz.,
$$
\frac{d}{dt}(T_2 - T_0 + V) = 0
$$
generally written: 
$$
T_2 - T_0 + V = h
$$
if the system is stability, mean $T_1 = T_0 = 0$, Viz,:
$$
T + V = E
$$
QED.
