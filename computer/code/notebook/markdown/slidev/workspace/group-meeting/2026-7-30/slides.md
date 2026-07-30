---
theme: seriph
colorSchema: dark
background: black
title: SSH 模型变分参数演化
info: |
  ## 本周组会
  SSH 模型基态拓扑 ZR 分类的数值实验与变分量子计算方案
class: text-center
drawings:
  persist: false
transition: slide-left
comark: true
duration: 35min
---

# SSH 模型变分参数演化

数值实验与变分量子计算方案

<div class="abs-br m-6 text-xl">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="slidev-icon-btn">
    <carbon:edit />
  </button>
</div>

---

# 项目概览

本项目围绕 SSH 模型，通过拓扑序参量 $Z_R$ 对基态进行三分类：

- 相 +1：$Z_R=1$（平凡）
- 相 -1：$Z_R=-1$（非平凡）
- 相 0：$Z_R=0$（临界）

利用对称性约束打开基态简并，设计变分量子电路实现任意参数点的基态制备与拓扑分类。

| 阶段 | 状态 |
| --- | --- |
| 1. 数值相图绘制与相边界计算 | ✅ 完成 |
| 2. 对称性分析：简并打开、初态选择、约束 H 验证 | ✅ 完成 |
| 3. 变分方案设计与文档 | ✅ 完成 |
| 4. 变分参数演化代码实现与实验 | 进行中 |

<div class="mt-4 text-sm opacity-70">
技术栈：Julia (QuantumToolbox) + Python (PyPlot/Seaborn) + Qiskit
</div>

---

# SSH 模型哈密顿量

交替耦合结构：

$$
H = (1-s) \sum_{i\ \text{odd}} (X_i X_{i+1} + \delta Z_i Z_{i+1}) + s \sum_{j\ \text{even}} (X_j X_{j+1} + \delta Z_j Z_{j+1})
$$

<div grid="~ cols-2 gap-4 mt-4">
<div>

**参数：**

- $J_1 = 1-s$（奇偶对）
- $J_2 = s$（偶奇对）
- $\delta$：各向异性参数
- $(s, \delta) \in [0,1] \times [0,1]$

</div>
<div>

**约束条件：**

- $N$ 必须是 4 的倍数（$4N^+$）
- 最少 8 比特
- 这限制了演化初态旋转和基态对称性

</div>
</div>

---

# $Z_R$ 序参量

<div class="grid grid-cols-2 gap-6">

<div>

**反射算符**：将链关于中心镜面反射

$$
S = \bigotimes_{i=1}^{N/2} \mathrm{SWAP}_{i,\ N-i+1}
$$

**计算公式**：

$$
Z_R = \frac{\mathrm{tr}(\rho S)}{\sqrt{(\mathrm{tr}(\rho_1^2) + \mathrm{tr}(\rho_2^2))/2}}
$$

- $\rho_1, \rho_2$：前后半链偏迹
- 分母：半链纯度 RMS 归一化

</div>
<div>

**实际计算需截断**：去除边缘自由比特

```julia
sub_num = qubit_num - 4
sub_system = ntuple(i -> i + 2, sub_num)
_, ψ0 = get_ssh_group_state(qubit_num, s, δ)
sub_ρ = ptrace(ψ0, sub_system)
ZR_val = get_ZR_val(sub_ρ)
```

| $Z_R$ | 拓扑相 | 区域 |
| --- | --- | --- |
| $+1$ | 平凡 | $s=0$ |
| $-1$ | 非平凡 | $s=1$ |
| $0$ | 临界 | $\delta=0$ |

</div>
</div>

---

# 从理论到数值相图

**ZR 序参量** 定义好后，下一步是数值扫描参数空间，绘制相图：

<div class="grid grid-cols-2 gap-6 mt-6">

<div>

**计算流程：**

1. 离散化参数网格 $(s, \delta) \in [0,1]^2$
2. 逐点构造 SSH 哈密顿量 $H(s, \delta)$
3. 精确对角化求基态 $|\psi_0\rangle$
4. 截断边缘比特，计算偏迹 $\rho_{\text{sub}}$
5. 计算 ZR 值并填入网格

</div>

<div>

**绘制内容：**

| 图 | 含义 |
| --- | --- |
| ZR 热力图 | 全参数空间拓扑分类 |
| 能谱图 | 固定 $s$ 或 $\delta$ 扫描能级 |
| 相边界 | ZR 符号翻转位置 |

</div>

</div>

<div class="mt-6 p-3 border border-blue-500/30 rounded bg-blue-500/10 text-sm">
Julia 实现：<code>get_ssh_ZR.jl</code>（单点）→ <code>get_ssh_phase.jl</code>（扫描）→ <code>plot_ssh_phase.py</code>（可视化）
</div>

---

# 数值相图：热力图

<div class="grid grid-cols-2 gap-4">

<div>
<img src="/pics/phase_N8.jpg" class="rounded mx-auto" />
<div class="text-center text-sm">N = 8</div>
</div>

<div>
<img src="/pics/phase_N12.jpg" class="rounded mx-auto" />
<div class="text-center text-sm">N = 12</div>
</div>

</div>

<div class="mt-4 text-sm">

- 左（$s$ 小）：$Z_R = +1$（蓝）· 右（$s$ 大）：$Z_R = -1$（红）
- 相边界为曲线，$\delta \to 0$ 时 $Z_R \to 0$（XX 模型临界特性）
- $N$ 增大时边界过渡更陡峭

</div>

---

# 数值相图：能谱

<div class="text-center">
  <div class="text-sm mb-2">δ 扫描 (k=4)</div>
  <img src="/pics/delta_scan_N8_k4.jpg" class="mx-auto h-80" />
</div>

---

# 数值相图：能谱

<div class="text-center">
  <div class="text-sm mb-2">δ 扫描 (k=8)</div>
  <img src="/pics/delta_scan_N8_k8.jpg" class="mx-auto h-80" />
</div>

---

# 数值相图：能谱

<div class="text-center">
  <div class="text-sm mb-2">s 扫描 (k=4)</div>
  <img src="/pics/s_scan_N8_k4.jpg" class="mx-auto h-80" />
</div>

---

# 数值相图：能谱

<div class="text-center">
  <div class="text-sm mb-2">s 扫描 (k=8)</div>
  <img src="/pics/s_scan_N8_k8.jpg" class="mx-auto h-80" />
</div>

<div class="mt-2 text-sm opacity-80">
低能区存在基态简并，简并度与相区有关
</div>

---

# 相边界计算

**两步法：**

1. **固定 $\delta=1$**：求 $Z_R=0$ 的 $s_p$（Roots.jl bracketing）
2. **以 $s_p$ 分段**：两侧分别固定 $s$，求 $Z_R = \pm 0.5$ 的 $\delta$ 临界值

**分段原因**：$s_p$ 是 $Z_R$ 符号翻转点，两侧目标值不同

<div class="mt-4 text-sm opacity-80">
相边界随比特数增大趋近于某个极限位置
</div>

---

# 相边界图

<img src="/pics/phase_boundary.jpg" class="rounded mx-auto" />

---

# 对称性分析：为什么

<div class="mt-12 text-center">

**核心问题**

SSH 模型的基态在参数空间部分区域存在多重简并（4 重）

因此在简并起点无法保证后续演化不跃迁，除非有对称性保护

<br>

**目标**

根据非简并初态的对称性, 使所有演化初态和目标态有**相同的对称性标记**

保证绝热演化过程中对称性可以保护演化路径

防止简并能级间的跃迁

</div>

---

# 对称性分析：寻找对称性算符

寻找与 $H(t)$ 恒对易的算符：$[P, H(t)] = 0$

<div class="grid grid-cols-2 gap-6 mt-4">

<div>

**方法**：$U$ 满足 $U^2=I$，有 $\pm1$ 两个本征值。
两个对易 $U$ 线性组合得 **4 个本征值**：

$$
P = U_x + 2U_z
$$

本征值：$\{3, -1, 1, -3\}$

</div>

<div>

**候选**：

$$
U_x = \bigotimes X_i,\quad U_y = \bigotimes Y_i,\quad U_z = \bigotimes Z_i
$$

- $[U_i, H(t)] = 0$，$[U_i, U_j] = 0$
- $U_y$ 冗余：$(-i)^N U_y = U_x U_z$

**最终选择**：$P = U_x + 2U_z$，$N$ 须为 **4 的倍数**

</div>

</div>

---

# 对称性约束哈密顿量

$$
H_c = H_{\text{SSH}} - \epsilon P = H_{\text{SSH}} - \epsilon (U_x + 2U_z)
$$

<div class="grid grid-cols-3 gap-4 mt-8">
<div class="p-3 border rounded text-center">
  <div class="text-lg mb-2">分裂简并能级</div>
  <div class="text-sm opacity-70">不同对称性的态能量分开</div>
</div>
<div class="p-3 border rounded text-center">
  <div class="text-lg mb-2">目标态孤立</div>
  <div class="text-sm opacity-70">⟨P⟩ = 3 的基态能量↓3ϵ</div>
</div>
<div class="p-3 border rounded text-center">
  <div class="text-lg mb-2">ϵ=0.05 小量</div>
  <div class="text-sm opacity-70">太大导致P=3对称性能级降到最低, 不利于观察劈列</div>
</div>
</div>

---
layout: two-cols
---

# 验证实验：ZR 相图

<div class="text-center text-sm mb-2">无约束</div>
<img src="/pics/phase_N8.jpg" class="rounded mb-2" />

::right::

<div class="mt-12"></div>

<div class="text-center text-sm mb-2">有约束 (H_c)</div>
<img src="/pics/constrained_phase_N8.jpg" class="rounded mb-2" />

<div class="mt-4 p-3 border border-green-500/30 rounded bg-green-500/10 text-center text-sm">
<b>结论</b>：ZR 相图无变化，基态本身未改变，只产生了能级分裂
</div>

---

# 验证实验：能谱对比

<div class="text-center">
  <div class="text-sm mb-2">无约束 s-scan k=4</div>
  <img src="/pics/s_scan_N8_k4.jpg" class="mx-auto h-80" />
</div>

---

# 验证实验：能谱对比

<div class="text-center">
  <div class="text-sm mb-2">有约束 s-scan k=4</div>
  <img src="/pics/constrained_s_scan_N8_k4.jpg" class="mx-auto h-80" />
</div>

---

# 验证实验：能谱对比

<div class="text-center">
  <div class="text-sm mb-2">无约束 s-scan k=8</div>
  <img src="/pics/s_scan_N8_k8.jpg" class="mx-auto h-80" />
</div>

---

# 验证实验：能谱对比

<div class="text-center">
  <div class="text-sm mb-2">有约束 s-scan k=8</div>
  <img src="/pics/constrained_s_scan_N8_k8.jpg" class="mx-auto h-80" />
</div>

<div class="mt-4 p-2 border border-green-500/30 rounded bg-green-500/10 text-center text-sm">
<b>结论</b>：简并能级清晰分裂，目标对称性基态被孤立出来 — 在不改变基态本身的前提下
</div>

---

# 初态选择：总原则

<div class="mt-20 text-center text-xl">

初始态的**首要目标**是方便制备

其次是不简并

再不然是可以从简并空间中挑出目标态

</div>

---

# 初态：相 -1（$Z_R = -1$, $s=1$）

<div class="grid grid-cols-2 gap-4">

<div>

$s=1$, $\delta \neq 0$：所有项对易

$$
X_iX_{i+1} = Z_iZ_{i+1} = -1 \quad (i\ \text{even})
$$

$N=4N^+$ 时 $U_x=U_z=1$ → 边界 $X_1 X_N = -1$, $Z_1 Z_N = -1$

守恒量约束退化成了**边界条件约束**，边缘态 = 最低能量 Bell state

对易关系：&#91;XXXX, ZZZZ, XIIX, IXXI, ZIIZ, IZZI, H(0)&#93; = 0

**量子态**：环链 $(\ket{01} - \ket{10})^{\otimes N/2}$

</div>

<div class="text-xs">

```text {maxHeight:'300px'}
     ┌───┐┌───┐          
q_0: ┤ X ├┤ H ├───────■──
     ├───┤├───┤       │  
q_1: ┤ X ├┤ H ├──■────┼──
     ├───┤└───┘┌─┴─┐  │  
q_2: ┤ X ├─────┤ X ├──┼──
     ├───┤┌───┐└───┘  │  
q_3: ┤ X ├┤ H ├──■────┼──
     ├───┤└───┘┌─┴─┐  │  
q_4: ┤ X ├─────┤ X ├──┼──
     ├───┤┌───┐└───┘  │  
q_5: ┤ X ├┤ H ├──■────┼──
     ├───┤└───┘┌─┴─┐  │  
q_6: ┤ X ├─────┤ X ├──┼──
     ├───┤     └───┘┌─┴─┐
q_7: ┤ X ├──────────┤ X ├
     └───┘          └───┘
```

<div class="text-xs opacity-70">
首尾比特 0 和 7 通过 H + CNOT 闭合为环
</div>

</div>
</div>

---

# 初态：相 1（$Z_R = +1$, $s=0$）

<div class="grid grid-cols-2 gap-4">

<div>

$s=0$, $\delta \neq 0$：

$$
X_iX_{i+1} = Z_iZ_{i+1} = -1 \quad (i\ \text{odd})
$$

**无边缘简并**，非简并基态 $U_x = U_z = 1$

Bell pair 结构，耦合从边界开始 (1,2), (3,4)...，**无环闭合**

</div>

<div class="text-xs">

```text {maxHeight:'300px'}
     ┌───┐┌───┐     
q_0: ┤ X ├┤ H ├──■──
     ├───┤└───┘┌─┴─┐
q_1: ┤ X ├─────┤ X ├
     ├───┤┌───┐└───┘
q_2: ┤ X ├┤ H ├──■──
     ├───┤└───┘┌─┴─┐
q_3: ┤ X ├─────┤ X ├
     ├───┤┌───┐└───┘
q_4: ┤ X ├┤ H ├──■──
     ├───┤└───┘┌─┴─┐
q_5: ┤ X ├─────┤ X ├
     ├───┤┌───┐└───┘
q_6: ┤ X ├┤ H ├──■──
     ├───┤└───┘┌─┴─┐
q_7: ┤ X ├─────┤ X ├
     └───┘     └───┘
```

</div>
</div>

---

# 初态：相 0（$Z_R = 0$, $\delta=0$）

<div class="grid grid-cols-2 gap-4">

<div>

$\delta=0$, $s \neq 0,1$（XX 模型），所有项对易

基态 $X_iX_{i+1} = -1$，**二重简并**：

$$
\ket{\phi^+} = \ket{+-+-...},\quad \ket{\phi^-} = \ket{-+-+...}
$$

$U_x$ 不区分（本征值同为 1），$U_z$ 在简并空间：

$$
U_z^{\phi^\pm} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
$$

对角化 → $\ket{\psi^\pm} = \frac{1}{\sqrt{2}}(\ket{\phi^+} \pm \ket{\phi^-})$

目标 $U_z=1$：$\frac{1}{\sqrt{2}}(\ket{\phi^+} + \ket{\phi^-})$

**X 表象下的 GHZ 态**

</div>

<div class="text-xs">

```text {maxHeight:'300px'}
     ┌───┐     ┌───┐┌───┐                              
q_0: ┤ H ├──■──┤ X ├┤ H ├──────────────────────────────
     └───┘┌─┴─┐└───┘├───┤                              
q_1: ─────┤ X ├──■──┤ H ├──────────────────────────────
          └───┘┌─┴─┐└───┘┌───┐┌───┐                    
q_2: ──────────┤ X ├──■──┤ X ├┤ H ├────────────────────
               └───┘┌─┴─┐└───┘├───┤                    
q_3: ───────────────┤ X ├──■──┤ H ├────────────────────
                    └───┘┌─┴─┐└───┘┌───┐┌───┐          
q_4: ────────────────────┤ X ├──■──┤ X ├┤ H ├──────────
                         └───┘┌─┴─┐└───┘├───┤          
q_5: ─────────────────────────┤ X ├──■──┤ H ├──────────
                              └───┘┌─┴─┐└───┘┌───┐┌───┐
q_6: ──────────────────────────────┤ X ├──■──┤ X ├┤ H ├
                                   └───┘┌─┴─┐├───┤└───┘
q_7: ───────────────────────────────────┤ X ├┤ H ├─────
                                        └───┘└───┘     
```

</div>
</div>

---

# 初态制备：Qiskit 实现

```python {maxHeight:'380px'}
def get_initial_state(N, phase_idx=1):
    qc = QuantumCircuit(N, N)
    if phase_idx == 1:          # ZR = +1, s=0
        for i in range(0, N, 1):
            qc.x(i)
        for i in range(0, N, 2):
            qc.h(i)
        for i in range(0, N - 1, 2):
            qc.cx(i, i + 1)
    elif phase_idx == -1:       # ZR = -1, s=1
        for i in range(0, N, 1):
            qc.x(i)
        for i in range(1, N - 1, 2):
            qc.h(i)
        for i in range(1, N - 2, 2):
            qc.cx(i, i + 1)
        qc.h(0)
        qc.cx(0, N - 1)         # 环闭合：首尾连接
    elif phase_idx == 0:        # ZR = 0, δ=0
        qc.h([0])
        qc.cx([i for i in range(N - 1)], [i for i in range(1, N)])
        qc.x([2 * i for i in range(N // 2)])
        qc.h([i for i in range(N)])
    else:
        raise ValueError("The value of phase_idx must be 1, -1, 0.")
    return qc
```

---

# 变分方案：关键观察 (1/2)

<div class="space-y-4 mt-4">

<div class="p-3 border border-blue-500/30 rounded bg-blue-500/10">

**1. 无需测量保真度**

判断态是否相同，只需 $H_c$ 期望取最小。**能量和对称性都满足的态就是目标基态**（非简并区唯一，简并区通过 $\epsilon$ 分裂后也唯一）。代价函数直接用 $H_c$ 期望，无需 fidelity 基准。

</div>

<div class="p-3 border border-orange-500/30 rounded bg-orange-500/10">

**2. 不能只在三个特殊点学习**

$(s=0,\delta=1)$、$(s=1,\delta=1)$、$(s=0.5,\delta=0)$ 都远离相边界。**拓扑分类的核心挑战是边界附近的连续过渡区域**。用三个远离边界的点去预测边界行为，信息量严重不足。

</div>

</div>

---

# 变分方案：关键观察 (2/2)

<div class="space-y-4 mt-4">

<div class="p-3 border border-red-500/30 rounded bg-red-500/10">

**3. 经典拟合不是量子机器学习**

把相图离散网格点的 ZR 当训练数据做经典拟合，和量子计算无关 —— 只是对数值结果的经典后处理。**如果经典计算机已经能算任意点的 ZR，那根本不需要量子计算机。** 量子计算的价值须体现在经典难以完成的任务上（大系统基态制备）。

</div>

<div class="p-3 border border-purple-500/30 rounded bg-purple-500/10">

**4. ZR 三分类替代精确值**

NISQ 噪声下 ZR 精确数值不可信，应关注**分类结果**（+1 / -1 / 0）。classical shadow 的纠错收益有限 —— 主要降低统计噪声而不改变测量相对大小。若直接测量已无法区分 ±1，shadow 也很难救回。

</div>

</div>

---

# 关键事实：同相出发线上的初态完全相同

<div class="mt-8 text-lg">

**三个相的初态只需各一个电路模板。**

</div>

<div class="grid grid-cols-3 gap-4 mt-6">
<div class="p-3 border rounded text-center">
  <div class="text-amber-400 font-bold mb-2">相 +1 出发线</div>
  <div class="text-sm">全部起点使用同一 Bell pair 态</div>
  <div class="text-xs opacity-60 mt-2">耦合 (1,2), (3,4), ...</div>
</div>
<div class="p-3 border rounded text-center">
  <div class="text-amber-400 font-bold mb-2">相 -1 出发线</div>
  <div class="text-sm">全部起点使用同一环链 Bell pair 态</div>
  <div class="text-xs opacity-60 mt-2">耦合 (2,3), (4,5), ... + 首尾环闭合</div>
</div>
<div class="p-3 border rounded text-center">
  <div class="text-amber-400 font-bold mb-2">相 0 出发线</div>
  <div class="text-sm">全部起点使用同一 X 表象 GHZ 态</div>
  <div class="text-xs opacity-60 mt-2">|φ⁺⟩ + |φ⁻⟩</div>
</div>
</div>

<div class="mt-6 p-3 border border-amber-500/30 rounded bg-amber-500/10 text-sm">
变分优化的自由度完全集中在 <b>演化路径</b> 上，初态制备不需针对每个离散起点单独设计
</div>

---

# 策略：穷举起点 + 路径优化 + 平均判别

<div class="mt-10">

对于相图中任一点 $(s,\delta)$：

<div class="grid grid-cols-3 gap-4 mt-6">
<div class="p-4 border rounded text-center">
  <div class="text-2xl mb-2">1</div>
  <div>穷举<b>三个相的起点</b></div>
  <div class="text-sm opacity-70 mt-2">每起点到目标点做变分优化</div>
</div>
<div class="p-4 border rounded text-center">
  <div class="text-2xl mb-2">2</div>
  <div>对比**同相起点组**的平均代价</div>
  <div class="text-sm opacity-70 mt-2">取平均值消去起点位置偶然性</div>
</div>
<div class="p-4 border rounded text-center">
  <div class="text-2xl mb-2">3</div>
  <div>代价最低的组 = 目标拓扑相</div>
  <div class="text-sm opacity-70 mt-2">同一相的起点路径天然更优</div>
</div>
</div>

<div class="mt-6 text-sm opacity-80">
也可通过所有线路的最优解直接计算 ZR 并分类 — 或将两者结合（起点ZR与终点ZR的距离作为惩罚项）
</div>

</div>

---

# 代价函数

$$
\begin{aligned}
H_c &= (1-s)\sum_{i\ \text{odd}} (X_i X_{i+1} + \delta Z_i Z_{i+1}) + s\sum_{j\ \text{even}} (X_j X_{j+1} + \delta Z_j Z_{j+1}) \\
&-\frac{\epsilon_1}{3}(U_x + 2U_z)  \quad \text{—— 对称性约束（此时 }\epsilon_1\text{ 不必取小量）}\\
&+ \epsilon_2|zr - ZR_p|^2  \quad \text{—— 终点 ZR 与起点相 }ZR_p\text{ 的距离惩罚}\\
&- \frac{\epsilon_3}{\tau} \cdot T  \quad \text{—— 演化时间惩罚（倾向短时间）}
\end{aligned}
$$

<div class="grid grid-cols-3 gap-4 mt-6">
<div class="text-sm">ϵ₁：权衡对称性与能量</div>
<div class="text-sm">ϵ₂：对 ZR 测量结果的信任程度</div>
<div class="text-sm">ϵ₃：限制演化时间，与经典模拟时间 τ 成反比</div>
</div>

---

# 演化路径：Bézier 曲线

**假设**：最优路线是始终靠近目标点的光滑曲线（无拐点，曲率不变号）

**二次 Bézier**：

$$
\begin{aligned}
s(t') &= (1-t')^2 s_0 + 2t'(1-t') s_c + t'^2 s_1 \\
\delta(t') &= (1-t')^2 \delta_0 + 2t'(1-t') \delta_c + t'^2 \delta_1
\end{aligned}
$$

$t' = t/T \in [0,1]$

**控制点** $(s_c, \delta_c)$ = 起点切线与终点切线的交点

范围：$s_c \in [s_0, s_1]$, $\delta_c \in [\delta_0, \delta_1]$（不回头）

---

# Bézier 曲线示意

<img src="/pics/bezier_demo.png" class="rounded mx-auto mt-8" />

---

# 变分参数

| 参数 | 含义 | 范围 |
| --- | --- | --- |
| $s_c, \delta_c$ | 二次 Bézier 控制点 | $[s_0,s_1] \times [\delta_0,\delta_1]$ |
| $\Delta t_i$ | 各离散步演化时间 | $\sum \Delta t_i = T$ |
| 步数 | 离散段数 | 极小步可省略对应门 |
| $T$ | 总演化时间 | 无约束 |
| Trotter 阶数 | 分解精度 | 视效果而定 |

---

# 方法优势

<div class="mt-10 space-y-6">

<div class="flex gap-4 items-start">
  <div class="text-2xl text-amber-400">1</div>
  <div>仅在 ZR 三分类的意义下，纠错不是必须的</div>
</div>

<div class="flex gap-4 items-start">
  <div class="text-2xl text-amber-400">2</div>
  <div>增加比特数<b>不直接增加电路深度</b></div>
</div>

<div class="flex gap-4 items-start">
  <div class="text-2xl text-amber-400">3</div>
  <div>Hc 测量 settings 恒为 <b>2</b>（只需全X 和 全Z 两种 Pauli 基），理论上可充分发挥量子计算机优势</div>
</div>

<div class="flex gap-4 items-start">
  <div class="text-2xl text-amber-400">4</div>
  <div>如需精确估计更多算符期望值，可引入 classical shadow 等纠错方案</div>
</div>

</div>

---

# 电路实现

- Qiskit `QAOAAnsatz` 只支持 $H(0)$ 和 $H_{\text{end}}$，演化路径不被天然支持
- **方案**：直接用 `PauliEvolutionGate`，手动绑定演化路径、步长、步数、分解阶数

<div class="mt-8 p-4 border border-gray-500/30 rounded bg-gray-500/10 font-mono text-sm">

QAOAAnsatz 结构（固定深浅交替，无路径绑定）：

```
      ┌──────────┐   ┌──────────┐         ┌──────────┐   ┌──────────┐
|ψ₀⟩ ─┤ e⁻ⁱᵝH(0) ├───┤ e⁻ⁱᵞH_end ├───···───┤ e⁻ⁱᵝH(0) ├───┤ e⁻ⁱᵞH_end ├──
      └──────────┘   └──────────┘         └──────────┘   └──────────┘
       p=1 layer         ↕ 固定 β, γ         最后层         步长不绑
```

PauliEvolutionGate 方案（路径感知）：

```
                                     ↙ Bézier 路径 → H(t'ₖ) 逐层不同
      ┌─────────────┐   ┌─────────────┐         ┌─────────────┐
|ψ₀⟩ ─┤ e⁻ⁱΔt₁H(t'₁) ├───┤ e⁻ⁱΔt₂H(t'₂) ├───···───┤ e⁻ⁱΔtₙH(t'ₙ) ├──
      └─────────────┘   └─────────────┘         └─────────────┘
        Δt₁, 步数, Trotter 阶数均为变分参数
```

</div>

---
layout: two-cols
---

# 下一步（待实现）

<div class="space-y-3 mt-6 text-sm">

1. **代价函数 Qiskit 实现**：四项代价 → 可测量期望

2. **Bézier 路径 PauliEvolutionGate 绑定**：离散路径 Trotter 分解

3. **经典优化器对接**：SPSA / COBYLA 优化变分参数

4. **三起点穷举流程**：遍历三起点分别优化取最优组

5. **噪声模型测试**：模拟噪声下验证 ZR 三分类鲁棒性

</div>

::right::

<div class="mt-6"></div>

---

# 对称性标记方案

<div class="text-xl mt-8 space-y-3">

1. SSH 有 4 重基态简并 → 需标记
2. 找全局守恒量 $U_x, U_z$ → 与 $H(t)$ 对易
3. 构造 $P = U_x + 2U_z$ → 四个本征值
4. $H_c = H - \epsilon P$ → 简并能级分裂
5. $\langle P \rangle = 3$ → 目标对称性基态
6. 对称性守恒 → 禁止简并能级间跃迁

</div>

---

# 变分拓扑分类

<div class="text-xl mt-8 space-y-3">

1. 同相基态有相同对称性标记
2. 同相出发路径代价天然更优
3. 穷举三起点 → 最低代价组 = 目标相
4. 精确 ZR 测量 → 三分类 → 容噪性强
5. Bézier 路径参数化 → 变分自由度可控

</div>

---

<div class="mt-48 text-center text-4xl opacity-70">
谢谢！
</div>
