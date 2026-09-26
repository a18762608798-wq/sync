---
title: "Kittel Ch2 Wave Diffraction and Reciprocal Lattice — 主线概念"
bibliography: references.bib
collection:
  - book
---

# Kittel Ch2 Wave Diffraction and Reciprocal Lattice — 主线概念

本书：@Kittel-

## 1. 晶体衍射（书 DIFFRACTION OF WAVES BY CRYSTALS）

### 布拉格定律 (Bragg law)

- 定义：平行晶面系对入射波镜面反射**相干加强的条件**。

$$
2d\sin\theta = n\lambda
$$
其中 $d$ 为平行晶面间距，$\theta$ 从晶面量起(**也即和晶面夹角**)，$n$ 为整数；只由点阵周期决定，不涉及基元成分。

- 例：每面只反射 $10^{-3}$ 到 $10^{-5}$，$10^{3}$ 到 $10^{5}$ 层面共同形成反射束。

## 2. 散射振幅与倒易点阵（书 SCATTERED WAVE AMPLITUDE）

### 电子数密度 (electron number density)

> 对于实空间坐标, a_i的定义只需要考虑基元的整体位置就可以；但是基元内部原子的相对位置可以用这一套坐标

- 定义：晶体中 $\mathbf{r}$ 处单位体积电子数，X 射线直接看到的局域量。
- 性质：平移不变 $n(\mathbf{r}+\mathbf{T})=n(\mathbf{r})$，故傅里叶展开只含倒格矢分量，系数 $n_{\mathbf{G}}$ 决定 $\mathbf{\Delta k}=\mathbf{G}$ 时的 $F=Vn_{\mathbf{G}}$。
- 例：电荷浓度、磁矩密度同属此类局域量；后文拆成 $n(\mathbf{r})=\sum_j n_j(\mathbf{r}-\mathbf{r}_j)$ 即得结构因子。

### 倒格子 (reciprocal lattice，也称倒易点阵)

- 定义：正格子傅里叶空间中的布拉维格子，衍射图即其映射。
- 性质：初基轴矢为

$$
\mathbf{b}_1 = 2\pi\frac{\mathbf{a}_2\times\mathbf{a}_3}{\mathbf{a}_1\cdot\mathbf{a}_2\times\mathbf{a}_3}
$$
轮换得 $\mathbf{b}_2,\mathbf{b}_3$，满足 $\mathbf{b}_i\cdot\mathbf{a}_j = 2\pi\delta_{ij}$；倒格矢 $\mathbf{G}=v_1\mathbf{b}_1+v_2\mathbf{b}_2+v_3\mathbf{b}_3$，$v_i$ 取整数；保证 $n(\mathbf{r}+\mathbf{T})=n(\mathbf{r})$。

- 例：sc 倒易仍为 sc，格常数 $2\pi/a$；bcc 倒易为 fcc；fcc 倒易为 bcc；倒格矢量纲为 $1/$长度。

### 散射振幅 (scattering amplitude)

- 定义：出射方向上全晶体电子浓度加相位因子积分，记为 $F$。
- 物理含义: 其模方是指定方向的散射强度.

$$
F = \int dV\, n(\mathbf{r}) \exp[-i\mathbf{\Delta k}\cdot\mathbf{r}]
$$
其中 $\mathbf{\Delta k} = \mathbf{k}' - \mathbf{k}$；当 $\mathbf{\Delta k} = \mathbf{G}$ 时 $F = V n_{\mathbf{G}}$，偏离任一倒格矢时 $F$ 可忽略。

- 例：基元成分只决定各级衍射相对强度，不改变布拉格位置。

### 散射矢量 (scattering vector)

- 定义：入射波矢与出射波矢之差，记为 $\mathbf{\Delta k} = \mathbf{k}' - \mathbf{k}$。
- 性质：**弹性散射** $|\mathbf{k}'| = |\mathbf{k}|$，$\mathbf{\Delta k}$ 加到 $\mathbf{k}$ 上得到 $\mathbf{k}'$。

### 衍射条件 (diffraction condition)

- 定义：散射矢量等于任一倒格矢时出现衍射束。
- 性质：判据为 $\mathbf{\Delta k} = \mathbf{G}$，等价写为 $2\mathbf{k}\cdot\mathbf{G}+G^2=0$；晶面间距 $d(hkl)=2\pi/|\mathbf{G}|$，$\mathbf{G}=h\mathbf{b}_1+k\mathbf{b}_2+l\mathbf{b}_3$。
- 例：$hkl$ 可含公因子 $n$，对应布拉格 $n$ 级，区别于第一章已约化的米勒指数 (Miller indices)。

### 劳厄方程 (Laue equations)

- 定义：衍射条件分别点乘正格子轴矢得到的分量方程。
- 性质：方程为 $\mathbf{a}_1\cdot\mathbf{\Delta k}=2\pi v_1$，$\mathbf{a}_2\cdot\mathbf{\Delta k}=2\pi v_2$，$\mathbf{a}_3\cdot\mathbf{\Delta k}=2\pi v_3$；几何上要求 $\mathbf{\Delta k}$ 同时落在三个锥面交线上。

### Ewald 作图 (Ewald construction)

- 定义：在倒易空间中以入射 $\mathbf{k}$ 为半径作球判断衍射的几何作图。
- 性质：$\mathbf{k}$ 末端落任一倒格点，以 $\mathbf{k}$ 起点为心作半径 $k$ 球，球交另一倒格点则沿 $\mathbf{k}'=\mathbf{k}+\mathbf{G}$ 出射，夹角即布拉格角。

### 关系

- 布拉格定律 vs 衍射条件：前者是标量面间距表述 $2d\sin\theta=n\lambda$，后者是矢量表述 $\mathbf{\Delta k}=\mathbf{G}$，同事由周期性导出。
- 衍射条件 vs 劳厄方程 vs Ewald 作图：同事一事，矢量式 $\mathbf{\Delta k}=\mathbf{G}$、分量式三锥交线、几何球交点三种表述。
- 正格子 vs 倒格子：正格矢量纲长度，倒格矢量纲 $1/$长度；晶体转动时两者一起转动；bcc vs fcc 互为倒易。

## 3. 布里渊区（书 BRILLOUIN ZONES）

### 布里渊区 (Brillouin zone)

- 定义：倒易点阵中的维格纳-赛兹原胞。
- 性质：边界由倒格矢中垂面构成，波矢从原点引到任一边界即满足衍射条件；第一布里渊区体积等于倒易初基平行六面体体积 $(2\pi)^3/V_c$，$V_c$ 为正格子初基原胞体积。

### 第一布里渊区 (first Brillouin zone)

- 定义：原点周围被中垂面围出的最小闭合体积。
- 性质：sc 为边 $2\pi/a$ 立方体；bcc 为十二面菱形十二面体，由 $12$ 个最短 $\mathbf{G}$ 中垂面围成；fcc 为截角八面体，主要由 $8$ 个最短 $\mathbf{G}$ 定八面体，再由 $6$ 个次短 $\mathbf{G}$ 切角。
- 例：一维倒格基矢长 $2\pi/a$，第一区边界在 $k=\pm\pi/a$。

### 关系

- 布里渊区 vs 维格纳-赛兹原胞：前者是后者在倒易空间的实现，作法同第一章正格子情形，保留点阵全对称性。
- 第一布里渊区 vs X 射线分析：历史上布里渊区不属于 X 射线语言，却是电子能带理论核心。

## 4. 基元傅里叶分析与消光（书 FOURIER ANALYSIS OF THE BASIS）

### 结构因子 (structure factor)

- 定义：单晶胞内基元各原子散射相加的几何因子，记为 $S_{\mathbf{G}}$。
- 性质：表达式为

$$
S_{\mathbf{G}} = \sum_j f_j \exp[-i\mathbf{G}\cdot\mathbf{r}_j] = \sum_j f_j \exp[-i2\pi(x_jv_1+y_jv_2+z_jv_3)]
$$
散射强度正比于 $S^*S$，故 $S$ 可复；bcc 和为奇数 $S=0$，和为偶数 $S=2f$；fcc 奇偶混杂 $S=0$，全奇或全偶允许，全偶 $S=4f$。

- 例：金属 Na 为 bcc，无 $(100),(111),(221)$，有 $(110),(200),(222)$；KCl 因 K 与 Cl 电子数相等，X 射线看成 sc，只有全偶反射，KBr 则 fcc 全现。

### 原子形状因子 (atomic form factor，也称原子散射因子)

- 定义：单原子电子分布的傅里叶分量，记为 $f_j$。
- 性质：球对称时

$$
f_j = \int 4\pi r^2 dr\, n_j(r)\frac{\sin Gr}{Gr}
$$
点电荷极限 $(\sin Gr)/Gr\to 1$ 得 $f_j\to Z$；前向散射 $G\to 0$ 同样 $f_j\to Z$；固体中自由原子值已足够好，不灵敏于价电子小重排。

### 关系

- 结构因子 vs 原子形状因子：前者是基元内原子间干涉，决定有无消光；后者是原子内电子分布干涉，决定包络随 $G$ 衰减。
- bcc 消光 vs fcc 消光：bcc 看指数和奇偶，fcc 看奇偶是否混杂；机制都是中途面相位 $\pi$ 相消。
