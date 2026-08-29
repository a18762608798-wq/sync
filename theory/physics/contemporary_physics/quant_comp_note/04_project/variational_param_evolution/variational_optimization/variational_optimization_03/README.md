---
title: "README"
bibliography: references.bib
collection:
- inbox
---
出于quark上的噪音实在是无法避免,
此子项目用于复现论文 [@Yu-Zhao-Wei-2023, TABLE I], 运用其后处理技巧.

## 原论文内容

### Model

演化力学量取原论文的绝热插值形式,
分解为奇/偶键两部分 [@Yu-Zhao-Wei-2023, Eq. (2), (4), (5)]:

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

### Ansatz (绝热连接)

- 初始态:

  $$
  |\psi_{\mathrm{singlets}}\rangle = \frac{1}{\sqrt{2^{N/2}}} \prod_{j=1}^{N/2} (|01\rangle-|10\rangle)_{2j-1,2j}
  $$

- 变分层: 对插值演化算符做 Trotter 离散,
  得到每层作用在偶/奇键上的两比特门
  - $U_{\mathrm{even/odd}}(\{\theta\}) = \prod_{j} e^{-i\theta_x \sigma_x^{[j]}\sigma_x^{[j+1]} - i\theta_y \sigma_y^{[j]}\sigma_y^{[j+1]} - i\theta_z \sigma_z^{[j]}\sigma_z^{[j+1]}}$
  - 即 $N_L$ 层的 $|\psi_{\mathrm{ansatz}}(\{\theta\})\rangle = \prod_{l=1}^{N_L} U^{(l)}_{\mathrm{even}}(\{\theta_e\}) U^{(l)}_{\mathrm{odd}}(\{\theta_o\}) |\psi_{\mathrm{singlets}}\rangle$.

### 后处理方法

论文将云实验能量提取到百分之几精度,
依赖误差缓解 [@Yu-Zhao-Wei-2023, Sec. IV]:

1. **读出误差缓解**: 超导比特读出误差可达 10% 以上.
   对每根键的两比特标定 $4\times 4$ 概率混淆矩阵 $M$
   ($\vec{P}_{\mathrm{measured}} = M\vec{P}_{\mathrm{ideal}}$),
   在理想分布非负约束下反解出缓解后的分布.
   键分为偶/奇两组并行执行, 整套流程只需两套缓解电路,
   与系统尺寸无关.

   **Bell 基测量的缓解**同理, 原理更好理解:
   设 $U$ 为 Bell 态制备电路
   ($|00\rangle \xrightarrow{U}$ Bell 态, 如 CNOT + $H$),
   则 Bell 基测量 = 固定变换 $U^\dagger$ 后接计算基测量;
   四个 Bell 态对应 $P\,U|00\rangle$ ($P \in \{I,X,Z,XZ\}$),
   因此四个标定电路形如 $U^\dagger P\,U|00\rangle$——
   **测量端固定, 只换输入端的单比特 Pauli**.
   理想无噪下各电路确定地返回一个经典比特串,
   $M_{\mathrm{Bell}} = I$; 任何偏差来自 $U$ 的门误差 + 读出误差.
   其中 $P=I$ 即 $U^\dagger U|00\rangle$,
   与门误差 ZNE 的恒等插入 $U(U^\dagger U)^n$ 同构.

2. **门误差 ZNE**: 制备 $|\psi_n\rangle = U(U^\dagger U)^n |0\cdots 0\rangle$,
   对 $O_n = \langle\psi_n|\hat{O}|\psi_n\rangle$
   按 $m = 2n+1 \to 0$ 外推零噪声极限.

3. **rZNE (参考态零噪声外推, 本文方法论亮点)**:
   用 ansatz 族内的参考态——所有变分参数置零的 Bell 对直积态
   $|\psi_{\mathrm{singlets}}\rangle = U(\{\theta\}=0)|0\cdots 0\rangle$,
   其能量精确已知 $E_{\mathrm{Bell}} = -(2+\Delta)N/2$.
   **注意该理论值与插值参数 $s$ 无关**

## 复现内容

### model

其中 $s \in [0,1]$ 为插值参数, $\Delta$ 为各向异性参数;
**此复现取 $\Delta = 1$, 演化起点 s=0, 终点 s=1.**

### ansatz

设计好演化 H 即可, 门优化交给 qiskit.

- layer = 1 即可.
- $\Delta t \in [0, 1]$, 根据结果考虑是否设置边界保护.
- 注意**odd和even层角度不相同**, 论文中对于 $Δ = 1$ 实际上
  **又令 $\theta_x = \theta_y = \theta_z$**, 我们也暂且加上这个限制.
- **门序至关重要(even 层必须先作用)**:
  初态 $|\psi_{\mathrm{singlets}}\rangle$ 恰好是 $H_{\mathrm{odd}}$ 的本征态
  (每奇键 singlet 本征值 $-3$, 总能 $-12$), 因此

  $$
  e^{-i\theta_o H_{\mathrm{odd}}}|\psi_{\mathrm{singlets}}\rangle = e^{i\,12\,\theta_o}|\psi_{\mathrm{singlets}}\rangle
  $$

  只是全局相位.

### 后处理方法

**本子项目主要复现第2, 3种误差缓解方法**,
第一点将在更正式的结果中添加逐比特对易的out纠正.

## 实际问题

### quark 平台后编译

quark平台对于提交电路会再次编译,
*特别是直接删除接近0角度的门*, 这点完全不是我们想要的效果.

这一点几乎*无法控制*,
因为不同的量子计算机似乎删除下限也不尽相同, 十分讨厌.

由此需要**设置下边界 $5.1e-4$**.

### qiskit 转译优化

是否存在qiskit优化电路对于不同数值的电路结构不同?
不能确定, 可以**看一下实际效果再决定是否需要手动 transpile 电路**.

> 结论: 不需要.

### ZNE 指数拟合的初值问题

`rZNE_exemplary.py` 中用 `scipy.optimize.curve_fit`
对 $a e^{-bm} + c$ 拟合时, 若**不提供初值**(默认 `p0=[1,1,1]`),
优化器会落入平凡解:

当 $b$ 增大, 指数项 $\to 0$、梯度消失, $a, b$ 变得不可辨识;

**修复**: 传入数据驱动的初值 `p0=[y[0]-y[-1], 0.3, y[-1]]`
(振幅取首尾差, 衰减率取经验值, 渐近项取末值), 拟合即恢复正常.

### quark 量子计算机校正问题

校正后 `Baihua` 质量明显下降, 原因不明. 暂用 `Shenglian` 替代之.

ZNE 和 rZNE 拟合点数大概是:

- `Baihua`: $n_m$ = 3 or 4
- `Shenglian`: $n_m$ = 2 or 3
