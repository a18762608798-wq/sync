For conservative system, $\frac{d}{dt} (\frac{\partial L}{\partial \dot q_\alpha}) - \frac{\partial L}{\partial q_\alpha} = 0$
Let: 
$$
p_\alpha = \frac{\partial L}{\partial \dot q_\alpha}
$$
Evidently: 
$$
\dot p_\alpha = \frac{\partial L}{\partial q_\alpha}
$$
Now we try to Legendere transform from $L$, 
according to [[theory/math/advanced_mathematics#^e7b52e]]
$$
H(p, q, t) = -L(\dot q, q, t) + p_\alpha \dot q_\alpha 
$$
also: 
$$
\begin{split}
dH & = - \frac{\partial L}{\partial \dot q_\alpha} d\dot q_\alpha -\frac{\partial L}{\partial q_\alpha}dq_\alpha + dp_\alpha \dot q_\alpha + p_\alpha d\dot q_\alpha +\frac{\partial L}{\partial t} dt\\
& = -\frac{\partial L}{\partial q_\alpha}dq_\alpha + dp_\alpha \dot q_\alpha + \frac{\partial L}{\partial t} dt\\
& = - \dot p_\alpha dq_\alpha + \dot q_\alpha dp_\alpha + \frac{\partial L}{\partial t} dt
\end{split}
$$
To sum up: 
$$
\begin{cases}
\dot p_\alpha = -\frac{\partial H}{\partial q_\alpha} = [p_\alpha, H]\\
\dot q_\alpha = \frac{\partial H}{\partial p_\alpha} = [q_\alpha, H]\\
\frac{\partial H}{\partial t} = - \frac{\partial L}{\partial t}
\end{cases}
$$
