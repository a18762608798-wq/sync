Basic on: 
$$
\begin{cases}
\delta t = 0\\
\delta q_\alpha |_{P_1} = \delta q_\alpha |_{P_2} = 0
\end{cases}
$$
we could create the relationship: 
$$
\begin{split}
q_\alpha + dq_\alpha + \delta(q_\alpha + dq_\alpha) & = (q_\alpha + \delta q_\alpha) + d(q_\alpha + \delta q_\alpha) \\
\rightarrow \delta(dq_\alpha) & = d(\delta q_\alpha)
\end{split}
$$
meanwhile: 
$$
\begin{split}
\delta(\frac{dq_\alpha}{dt}) & = \frac{\delta (dq_\alpha) dt}{dt^2} - \frac{dq_\alpha \delta(dt)}{dt^2} \\
& = \frac{\delta(dq_\alpha)}{dt} - \frac{dq_\alpha d(\delta t)}{dt^2} \\
& = \frac{d}{dt} (\delta q_\alpha)
\end{split}
$$
Therefore: 
$$
\begin{cases}
[\delta, d]q_\alpha = 0\\ 
[\delta, \frac{d}{dt}] q_\alpha = 0
\end{cases}
$$
so much for this, now we formally proof Hamilton's principle, construct: 
$$
\int_0^\tau\{ [\frac{d}{dt}(\frac{\partial L}{\partial \dot q_\alpha})-\frac{\partial L}{\partial q_\alpha}]\delta q_\alpha \} dt= 0
$$
<span style="color:red">Notice: system must be on a common process when t=0 and t=\tau</span>
where: 
$$
\frac{d}{dt}(\frac{\partial L}{\partial \dot q_\alpha})\delta q_\alpha = \frac{d}{dt}(\frac{\partial L}{\partial \dot q_\alpha}\delta q_\alpha) - \frac{\partial L}{\partial \dot q_\alpha}\delta \dot q_\alpha
$$

To sum up: 
$$
\frac{\partial L}{\partial \dot q_\alpha}\delta q_\alpha|_0^\tau - \int_0^\tau [\frac{\partial L}{\partial \dot q_\alpha}\delta \dot q_\alpha + \frac{\partial L}{\partial q_\alpha}\delta q_\alpha] dt = 0
$$
because $\delta q_\alpha|_0 = \delta q_\alpha|_\tau = 0$, therefore: 
$$
\int_0^\tau \delta L dt = 0 \rightarrow \delta S = \delta \int_0^\tau L dt = 0
$$
