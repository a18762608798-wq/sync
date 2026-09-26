---
title: "Kittel Ch1 Crystal Structure — 主线概念"
bibliography: references.bib
collection:
  - book
---

# Kittel Ch1 Crystal Structure — 主线概念

本书：@Kittel-

## 1. 晶体构成

### 基元 (basis)

- 定义：全同重复的结构单元，可为单原子或多原子。
- 性质：基元内第 $j$ 原子相对位置为

$$
\mathbf{r}_j = x_j\mathbf{a}_1 + y_j\mathbf{a}_2 + z_j\mathbf{a}_3
$$
$0 \le x_j,y_j,z_j < 1$。

### 点阵 (lattice，也称晶格、布拉维格子 Bravais lattice)

- 定义：基元代表点即格点 (lattice point，也称阵点)的无限周期集合。
- 性质：点阵平移不变，格矢为

$$
\mathbf{r}' = \mathbf{r} + u_1\mathbf{a}_1 + u_2\mathbf{a}_2 + u_3\mathbf{a}_3
$$
其中 $u_i$ 为整数，$\mathbf{a}_i$ 为晶轴 (crystal axes)。

### 晶体 (crystal)

- 定义：把基元按点阵平移复制填满空间得到的结构。
- 关系：晶体 = 点阵 + 基元。

## 2. 重复单元

### 原胞 (primitive cell，也称初基原胞)

- 定义：体积最小的周期重复单元。
- 性质：每原胞只含 1 格点，体积为

$$
V_c = \mathbf{a}_1 \cdot \mathbf{a}_2 \times \mathbf{a}_3
$$
取法不唯一但体积唯一。

### 晶胞 (unit cell) / 惯用晶胞 (conventional cell)

- 定义：为反映对称性约定的重复单元，常用惯用晶胞。
- 性质：体积为原胞整数倍，可含多个格点。
- 例：只有简单立方 sc (simple cubic)的惯用晶胞同时是原胞，体心立方 bcc (body-centered cubic)含 2 格点，面心立方 fcc (face-centered cubic)含 4 格点。

### WS 原胞 (Wigner-Seitz cell，维格纳-赛兹原胞)

- 定义：以某格点为中心、对近邻连线作中垂面围出的原胞。
- 性质：与基矢选择无关，保留点阵全对称性。

## 3. Bravais 点阵分类

### Bravais 点阵

- 定义：满足点点等价的点阵，即任两格点平移后点阵完全重合。
- 性质：除平移外还允许转动、镜面、反演，转轴只允许 1,2,3,4,6 次，不存在 5 次；2D 有 5 种，3D 有 14 种，分属 7 晶系即三斜 triclinic、单斜 monoclinic、正交 orthorhombic、四方 tetragonal、立方 cubic、三方 trigonal、六方 hexagonal。
- 例：立方系只有 sc、bcc、fcc；惯用晶胞含格点数 1,2,4，近邻 (nearest neighbor)数 6,8,12，填充率 (packing fraction)0.524,0.680,0.740。

## 4. 晶向与晶面

### 晶向 (direction)，记 $[uvw]$

- 定义：一族平行晶列 (lattice row)确定的方向。
- 性质：求法为取该方向矢量在基矢上的分量，化最小整数比；负分量上加横线，如 $[\bar{1}00]$。
- 例：$\mathbf{a}_1$ 轴为 $[100]$，体对角线为 $[111]$。

### 晶面 (lattice plane)，记 $(hkl)$，即米勒指数 (Miller indices)

- 定义：一族平行格点平面确定的面系。
- 性质：求法为取面在三轴截距，取倒数化最小整数比；截距无穷对应指数 0；对称等价面族记 ${hkl}$。
- 例：$(200)\parallel(100)$，立方体面族为 ${100}$。

### 关系

- 一般 $[uvw]$ 与 $(uvw)$ 不垂直，仅立方系有 $[hkl]\perp(hkl)$。

## 5. 典型晶体结构

### NaCl 结构 (sodium chloride structure)

- 定义：fcc 点阵 + Cl 000 + Na $\frac{1}{2}\frac{1}{2}\frac{1}{2}$。
- 例：每个惯用晶胞 4 分子，配位数 (coordination number)6。

### CsCl 结构 (cesium chloride structure)

- 定义：简立方点阵 + 000 + $\frac{1}{2}\frac{1}{2}\frac{1}{2}$。
- 例：1 分子/原胞，8 配位。

### 密堆积 (close packing)

- 定义：单层六配位密排层按不同顺序堆垛。
- 性质：第二层放 $B$ 位，第三层选 $A$ 得 hcp (hexagonal close-packed) $ABAB\ldots$，选 $C$ 得 fcc $ABCABC\ldots$；均为 12 配位，填充率 0.74；理想 hcp $c/a=\sqrt{8/3}=1.633$。

### 金刚石 (diamond) / 闪锌矿 (zinc blende)

- 定义：金刚石点阵为 fcc，原胞基元为 000 + $\frac{1}{4}\frac{1}{4}\frac{1}{4}$ 双全同原子；换为 Zn+S 即闪锌矿即立方硫化锌结构。
- 性质：金刚石每个惯用晶胞 8 原子，四面体 (tetrahedral) 4 配位；闪锌矿无反演中心 (inversion center)。
- 例：Si,Ge 为金刚石；GaAs/AlAs 晶格常数几乎相等，故可做异质结 (heterojunction)。

## 6. 非理想堆垛

### 无规堆垛 (random stacking)

- 定义：密堆层堆垛顺序无规，二维有序而第三维无序。

### 多型性 (polytypism)

- 定义：沿堆垛轴的长周期有序堆垛。
- 性质：机制是生长中位错螺旋台阶，不是长程力。
- 例：ZnS 150+ 种多型，SiC 45+ 种。
