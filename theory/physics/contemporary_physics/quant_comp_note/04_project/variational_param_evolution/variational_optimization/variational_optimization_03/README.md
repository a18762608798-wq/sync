---
title: "README"
bibliography: references.bib
collection:
- inbox
---
出于quark上的噪音实在是无法避免, 此子项目用于复现论文 @Yu-Zhao-Wei-2023, 运用其后处理技巧.

## 原论文内容

### Model

演化力学量取原论文的绝热插值形式, 分解为奇/偶键两部分 [@Yu-Zhao-Wei-2023, Eq. (2), (4), (5)]:

$$
\hat{H}(s) = \hat{H}_o(s) + \hat{H}_e(s) = (1-s)\hat{H}_{\mathrm{odd}} + s\,\hat{H}_{\mathrm{XXZ}}
$$

奇数键部分与 $s$ 无关, 即 $\hat{H}_o(s) = \hat{H}_{\mathrm{odd}}$:

$$
\hat{H}_{\mathrm{odd}} = \sum_{j=1}^{N/2} \left( \sigma_x^{[2j-1]}\sigma_x^{[2j]} + \sigma_y^{[2j-1]}\sigma_y^{[2j]} + \Delta\,\sigma_z^{[2j-1]}\sigma_z^{[2j]} \right)
$$

偶数键部分是 XXZ 相互作用乘上插值参数 $s$ 的缩放:

$$
\hat{H}_e(s) = s\sum_{j=1}^{N/2-1} \left( \sigma_x^{[2j]}\sigma_x^{[2j+1]} + \sigma_y^{[2j]}\sigma_y^{[2j+1]} + \Delta\,\sigma_z^{[2j]}\sigma_z^{[2j+1]} \right)
$$

### Ansatz(绝热连接)

- 初始态:仅奇数键有相互作用的 $\hat{H}_{\mathrm{odd}}$ 的基态,即相邻单态的直积(价键态)$|\psi_{\mathrm{singlets}}\rangle = \frac{1}{\sqrt{2^{N/2}}} \prod_{j=1}^{N/2} (|01\rangle-|10\rangle)_{2j-1,2j}$,通过 $\hat{H}(s) = (1-s)\hat{H}_{\mathrm{odd}} + s\hat{H}_{\mathrm{XXZ}}$ 绝热连接到 XXZ 基态(该插值路径对 $\Delta > -1$ 无隙)。
- 变分层:对插值演化算符做 Trotter 离散,得到每层作用在偶/奇键上的两比特门
  $U_{\mathrm{even/odd}}(\{\theta\}) = \prod_{j} e^{-i\theta_x \sigma_x^{[j]}\sigma_x^{[j+1]} - i\theta_y \sigma_y^{[j]}\sigma_y^{[j+1]} - i\theta_z \sigma_z^{[j]}\sigma_z^{[j+1]}}$,即 $N_L$ 层的 $|\psi_{\mathrm{ansatz}}(\{\theta\})\rangle = \prod_{l=1}^{N_L} U^{(l)}_{\mathrm{even}}(\{\theta_e\}) U^{(l)}_{\mathrm{odd}}(\{\theta_o\}) |\psi_{\mathrm{singlets}}\rangle$。

### 后处理方法

论文将云实验能量提取到百分之几精度,依赖误差缓解 [@Yu-Zhao-Wei-2023, Sec. IV]:

1. **读出误差缓解**:超导比特读出误差可达 10% 以上。对每根键的两比特标定 $4\times 4$ 概率混淆矩阵 $M$($\vec{P}_{\mathrm{measured}} = M\vec{P}_{\mathrm{ideal}}$),在理想分布非负约束下反解出缓解后的分布。键分为偶/奇两组并行执行,整套流程只需两套缓解电路,与系统尺寸无关。

2. **门误差 ZNE**:制备 $|\psi_n\rangle = U(U^\dagger U)^n |0\cdots 0\rangle$,对 $O_n = \langle\psi_n|\hat{O}|\psi_n\rangle$ 按 $m = 2n+1 \to 0$ 外推零噪声极限。

3. **rZNE(参考态零噪声外推,本文方法论亮点)**:用 ansatz 族内的参考态——所有变分参数置零的 Bell 对直积态 $|\psi_{\mathrm{singlets}}\rangle = U(\{\theta\}=0)|0\cdots 0\rangle$,其能量精确已知 $E_{\mathrm{Bell}} = -(2+\Delta)N/2$。将参考态与目标态的实验能量分别按 $f_E(m) = a\,e^{-bm} + c$ 拟合(注意存在非零残余项 $c$);由参考态标定 rescale 因子 $r$:$a_B\,r + c_B = E_{\mathrm{Bell}}$;再对目标态施加同一校准 $E_{\mathrm{exp}} = a_E\,r + c_E$。该方法无需随机化编译、无需倍增 CNOT 门,在 102-qubit 链上(单电路最高 3186 个 CNOT、CNOT 深度 63)将能量误差控制在百分之几。

## 复现内容

### model

其中 $s \in [0,1]$ 为插值参数, $\Delta$ 为各向异性参数; **此复现取 $\Delta = 1$** .

### ansatz

设计好演化 H 即可, 门优化交给 qiskit.

- layer = 1 即可.
- $\Delta t \in [0, 1]$, 根据结果考虑是否设置边界保护.
- 注意**odd和even层角度不相同**, 论文中对于 $Δ = 1$ 实际上**又令 $theta_x = theta_y$**, 我们也暂且加上这个限制.

### 后处理方法

**本子项目主要复现第2, 3种误差缓解方法**, 第一点将在更正式的结果中添加.
