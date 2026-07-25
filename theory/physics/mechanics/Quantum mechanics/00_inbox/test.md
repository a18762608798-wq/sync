
**问题 1：变换方向不一致**  
开头说 $S|\psi_1\rangle = |\psi_2\rangle$，结尾却写 $S^\dagger \psi_1 = \psi_2$，二者矛盾。应统一为前者。

**问题 2：算符变换的共轭方向反了**  
如果基矢旋转是 $|\phi_i^{(2)}\rangle = S|\phi_i^{(1)}\rangle$（和态矢的主动旋转方向一致），则：

$$
F_2 = \sum_i f_i |\phi_i^{(2)}\rangle\langle\phi_i^{(2)}|
= \sum_i f_i S|\phi_i^{(1)}\rangle\langle\phi_i^{(1)}|S^\dagger
= S F_1 S^\dagger
$$

你写的 $F_2 = S^\dagger F_1 S$ 刚好反了一个 dagger。应该改为 $F_2 = S F_1 S^\dagger$。

此时一切自洽：

$$
\begin{cases}
|\psi_2\rangle = S|\psi_1\rangle \\
|\phi_i^{(2)}\rangle = S|\phi_i^{(1)}\rangle \\
F_2 = S F_1 S^\dagger
\end{cases}
$$

在这套约定下，$F_2$ 在自己基下的矩阵元等于 $F_1$ 在自己基下的矩阵元（分量不变），正是"整套空间旋转"的物理含义。

---

另外可以补充一段与被动表象变换的关系：

> 表象变换（passive）：$S_p|\phi_i^{(1)}\rangle = |\phi_i^{(2)}\rangle$，态不动，分量变。习惯约定中 $S^\alpha_\beta = \langle\phi_\alpha^{(2)}|\phi_\beta^{(1)}\rangle$。
> 
> 幺正操作（active）：$S_a|\phi_i^{(1)}\rangle = |\phi_i^{(2)}\rangle$，态也跟着转，在自己基下分量不变。
> 
> 两者的关系：$S_p = S_a^\dagger$（passive 相当于"反向补偿"）。

要我按这个思路帮你重写幺正操作这一节吗？
