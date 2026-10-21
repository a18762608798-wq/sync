# Measurement Essence via Decoherence

**INTERPRET:**

证 $S \to A \to E$ 链如何选出偏好基并把 $\rho_{SA}$ 压成对角混合。

**ASSUME:**

$S$ 为量子比特， $A$ 初态为 $|A_0\rangle$ ， $E$ 为 $N$ 个初态相同粒子。

**REQUIRE:**

$S \to A$ 为函数映射， $A \to E$ 以 $A$ 为控制位， $N$ 充分大。

**DEFINITION:**

$$
[H_{AE}, |0\rangle_A\langle 0|] \approx 0 \tag{1}
$$

满足 (1) 的 $\{|0\rangle_A, |1\rangle_A\}$ 称为偏好基。

$$
D_{ji} = \langle E_j'|E_i'\rangle \tag{2}
$$

称为退相干因子。

**NOTE:**

(1) 与 (7) 同一相互作用的无穷小与有限时间形式，偏好基在 $A$ ， $E$ 演化下布居守恒、无跃迁，唯 $E$ 记数，叠加态退相干。

**LET:**

$$
|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} \tag{3}
$$

$$
|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} \tag{4}
$$

**GIVEN:**

$$
|\Psi_0\rangle = |S\rangle \otimes |A_0\rangle \otimes |E_0\rangle \tag{5}
$$

$$
U_{SA} |s_i\rangle \otimes |A_0\rangle = |s_i\rangle \otimes |A_{f(i)}\rangle \tag{6}
$$

$$
U_{AE} = |0\rangle_A\langle 0| \otimes U_0 + |1\rangle_A\langle 1| \otimes U_1 \tag{7}
$$

**BY:**

(3)，(4)

**HAVE:**

$$
\frac{|0\rangle_S|0\rangle_A + |1\rangle_S|1\rangle_A}{\sqrt{2}} = \frac{|+\rangle_S|+\rangle_A + |-\rangle_S|-\rangle_A}{\sqrt{2}} \tag{8}
$$

**BY:**

(5)，(6)，(7)

**HAVE:**

$$
|\Psi\rangle_{SAE} = \frac{|0\rangle_S|0\rangle_A|0\rangle_E + |1\rangle_S|1\rangle_A|1\rangle_E}{\sqrt{2}} \tag{9}
$$

**CONSIDER:**

(9) 在 $|+\rangle$ ， $|-\rangle$ 基下展开。

**BY:**

(9)，(3)，(4)

**HAVE:**

$$
|\Psi\rangle_{SAE} = \frac{|+\rangle_S|+\rangle_A|+\rangle_E + |+\rangle_S|-\rangle_A|-\rangle_E + |-\rangle_S|-\rangle_A|+\rangle_E + |-\rangle_S|+\rangle_A|-\rangle_E}{2} \tag{10}
$$

**BECAUSE:**

(10) 中 $|+\rangle_S$ 复用两次，一个 $S$ 对应两个 $A$ ，按 [CON-Measurement_Requirement](../note/CON-Measurement_Requirement.md) 单值性要求非合法分支形式，三体分解唯一，故唯 (9) 合法。

**BY:**

(7)，(3)，(4)

**HAVE:**

$$
U_{AE} |+\rangle_A|-\rangle_E = |-\rangle_A|-\rangle_E \tag{11}
$$

**BECAUSE:**

$X|+\rangle = |+\rangle$ ， $X|-\rangle = -|-\rangle$ ，故 $0/1$ 下 $A$ 控 $E$ ， $+/-$ 下 $E$ 控 $A$ 。

**BY:**

(5)，(6)，(7)，[CON-Measurement_Requirement](../note/CON-Measurement_Requirement.md)

**HAVE:**

$$
\rho_{SA} = \sum_{i,j} c_i c_j^* D_{ji} \, |s_i\rangle\langle s_j| \otimes |A_i\rangle\langle A_j| \tag{12}
$$

**HAVE:**

$$
\langle E^{(0)}|E^{(1)}\rangle = \prod_{k=1}^N \langle e_k^{(0)}|e_k^{(1)}\rangle \tag{13}
$$

**SUFFICES:**

$D_{ji} \to \delta_{ji}$ 即得对角混合。

**BY:**

(12)，(13)，(2)

**THEREFORE:**

$$
\rho_{SA} \to \sum_i |c_i|^2 |s_i\rangle\langle s_i| \otimes |A_i\rangle\langle A_i| \tag{14}
$$

**PROPERTY:**

(14) 中 $|01\rangle$ ， $|10\rangle$ 布居为 $0$ ； $|\Phi_+\rangle$ 与 $|\Phi_-\rangle$ 各半混合杀死 $+/-$ 关联， $0/1$ 关联永存。

**CHECK:**

$D = 1$ 时 (12) 为纯纠缠； $D = 0$ 时 (12) 化为 (14) ； $N \to \infty$ 时 (13) 趋于 $0$ 。

**CAVEAT:**

(14) 是非真混合；单次结果随机性需诠释补充； $|\alpha|^2 = m/M$ 为底层等权分支计数。

**IMPLICATION:**

$|E_0'\rangle \perp |E_1'\rangle$ 后读 $E$ 即知 $A$ 即知 $|c_i'|^2$ ， $X$ ， $Y$ ， $Z$ 三组频率反演 $\rho_S$ 属数学层析。

**QED**
