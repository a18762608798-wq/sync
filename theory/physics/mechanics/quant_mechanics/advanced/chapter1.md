---
bibliography: references.bib
collection:
  - book
---

第一章 §1.2–§1.3（§1.1 为卷I回顾，不记），依 @zeng2014quantum2 书页 p.12–25（PDF p.44–57）：一词一条，页码指 PDF 页，与 Zotero 标注一一对应。

## §1.2 密度矩阵

### 密度算符 density operator (PDF p45)

定义：与纯态 $|\psi(t)\rangle$ 相应的 $\rho(t) = |\psi(t)\rangle\langle\psi(t)|$，是量子态的另一种描述。

性质：

- $\rho^\dagger = \rho$，纯态还有 $\rho^2 = \rho$。
- 矩阵元 $\rho_{nn'} = C_n C_{n'}^*$，对角元 $\rho_{nn} = |C_n|^2 \ge 0$ 即测得 $F_n$ 的概率，$\mathrm{tr}\rho = 1$。
- $\rho_{nn'} \ne 0$ 要求 $n,n'$ 成分在 $|\psi\rangle$ 中都不缺，且携带相对相位。

### 平均值公式 trace formula (PDF p46)

定义：$\langle G\rangle = \mathrm{tr}(\rho G) = \mathrm{tr}(G\rho)$。

性质：

- 测 $F$ 得 $F_n$ 的概率 $P(F_n) = \mathrm{tr}(P_n\rho) = |C_n|^2$。
- 密度算符运动方程 $i\hbar \frac{d \rho}{d t} = [H,\rho]$（von Neumann 方程），
对比 Heisenberg 绘景力学量演化多一负号。
- 能量表象是其特例的直接推论（见下条）。

### 能量表象演化 energy-representation evolution (PDF p47)

定义：以 $H$ 本征态为基时 $i\hbar\dot\rho_{nn'} = (E_n - E_{n'})\rho_{nn'}$。

性质：

- 非对角元以 $\omega_{nn'} = (E_n - E_{n'})/\hbar$ 振荡，对角元不随时间变。
- 坐标表象"矩阵元" $\rho(r,r') = \psi^*(r')\psi(r)$，动量表象类似。

### 坐标表象概率密度 position distribution (PDF p47)

定义：对角元 $\rho(r,r) = |\psi(r)|^2 \equiv W(r)$，动量表象 $W(p) = |\phi(p)|^2$。

性质：

- 单给 $W(r)$ 或 $W(p)$ 都定不了量子态，皆因丢失相位；两者都给一般仍不够（思考题 1，Pauli 1958，Gale 1968）。
- 更深层原因：量子态信息含相对相位，概率分布只含模方。

### 自旋 1/2 密度矩阵 spin-1/2 example (PDF p48)

定义：$\sigma_x = +1$ 本征态在 Pauli 表象的密度矩阵。

性质：

- 对角元 $1/2$ 表示测 $\sigma_z$ 得 $\pm 1$ 各半，非对角元非零表示 $\sigma_z$ 本征态的相干叠加。
- 换到 $\sigma_x$ 表象则密度矩阵对角化为 $\mathrm{diag}(1,0)$，验证 $\rho^2 = \rho$、$\mathrm{tr}\rho = 1$。

例：

- $\sigma\cdot n$ 本征态投影算符显式（式 1.2.33），$\vartheta = \pi/2,\varphi = 0$ 回到例 1。
- $\langle\sigma\rangle = \mathrm{tr}(\rho\sigma) = n$ 即极化方向。

### 流密度 probability current (PDF p47)

定义：$K = [P(r)r\cdot p + p\cdot rP(r)]/2m$ 在 $|\psi\rangle$ 下平均值即流密度 $j(r)$。

性质：

- $j = (i\hbar/2m)(\psi\nabla\psi^* - \psi^*\nabla\psi)$，属计算样板：算符平均值化为密度与梯度。

### 混合态 mixed state (PDF p50)

定义：体系以概率 $p_k$ 处于纯态 $|\psi_k\rangle$ 的统计混合，
$\rho = \sum_k p_k|\psi_k\rangle\langle\psi_k|$，$0 \le p_k \le 1$，$\sum_k p_k = 1$。

性质：

- 除 $\rho^2 = \rho$ 不再成立，其余纯态性质照旧：
$\rho^\dagger = \rho$、$\mathrm{tr}\rho = 1$、$i\hbar d\rho/dt = [H,\rho]$。
- $\mathrm{tr}\rho^2 \le 1$，等号只对纯态成立。
- 平均值公式形式不变：$\langle G\rangle = \mathrm{tr}(\rho G)$。

例：

- 炉中蒸发原子、自然光源非偏振光都不能用单个波函数描述。

### 布居 population (PDF p51)

定义：混合态下 $\rho_{nn} = \sum_k p_k|C_n^k|^2$，即测得体系处于 $|n\rangle$ 的概率。

性质：

- 取表象 $F = L$（制备基）时密度矩阵对角化，对角元即各纯态权重 $p_n$。

### 相干 coherence (PDF p51)

定义：非对角元 $\rho_{nn'}$ 表征 $|n\rangle$ 与 $|n'\rangle$ 在混合态下的相干性，为零即不相干。

性质：

- 把纯态展开系数模方误读为"已处于"各分支的比例，会推出 $1/2$ 变 $1/4$ 一类荒谬结论（式 1.2.53–54 反例）。
- 波函数预言的概率是潜在预期，不是既成分布。

### 极化矢量 polarization vector (PDF p51)

定义：$P = \langle\sigma\rangle$，自旋 1/2 密度矩阵一般形 $\rho = (I + P\cdot\sigma)/2$。

性质：

- $\det\rho = (1 - P^2)/4 \ge 0$ 得 $0 \le |P| \le 1$，$P$ 落在 Bloch 球内。
- $|P| = 1$ 完全极化纯态，$|P| < 1$ 部分极化，$P = 0$ 完全不极化混合态 $\rho = I/2$。

例：

- 不同制备可得相同密度矩阵：各向同性无规指向与 $z/\bar z$ 各半混合都是 $I/2$，注意此时 $\rho^2 \ne \rho$ 并不违反纯态性质因它本是混合态。
- 完全极化态 $\rho(n) = (1 + \sigma\cdot n)/2$。

## §1.3 复合体系

### 直积态与纠缠态 product and entangled states (PDF p53)

定义：复合体系纯态可写成子系态直积即直积态，否则为纠缠态，$|\Psi\rangle_{AB} = |\psi\rangle_A \otimes |\phi\rangle_B$ vs 不可分解。

性质：

- 推广到 $N$ 体：全可分解才算直积态。
- 混合态纠缠复杂得多(MPO? 暂不讨论.)，见 Horodecki RMP 2009。
- EPR 佯谬是最早的非定域性表述，Schrödinger 猫态见第 3 章。

### 约化密度矩阵 reduced density matrix (PDF p54)

定义：$\rho_A = \mathrm{tr}_B\,\rho_{AB}$，只算子系 $A$ 可观测量时替代全矩阵用。

性质：

- $\langle Q_A\rangle = \mathrm{tr}_A(\rho_A Q_A)$，$Q = Q_A \otimes I_B$。
- $\rho_A \ge 0$、$\mathrm{tr}_A\rho_A = 1$，可对角化，本征值非负求和为 1。
- 一般 $\rho_A^2 \ne \rho_A$：整体纯态的子系一般是混合态。

### 直积判据 product criterion (PDF p55 注 3)

定义：$\rho_{AB} = \rho_A \otimes \rho_B$ 则直积，否则纠缠，可推广多体。

性质：

- 这是密度矩阵语言下直积/纠缠的充要判据，与 §1.3.1 矢量定义等价。
- 在MPO语言中是两个系统中间 link dim 为 1(**但是$D \ge 2$的时候不一定纠缠**)

### Schmidt 分解 Schmidt decomposition (PDF p55–56)

定义：两体纯态总可写成 $|\psi\rangle_{AB} = \sum_n \sqrt{p_n}\,|\psi_n\rangle_A|f_n\rangle_B$，$\sqrt{p_n}$ 为 Schmidt 系数，项数 $M$ 为 Schmidt 数。

性质：

- $M = 1$ 直积态，$M > 1$ 纠缠态；约化矩阵 $\rho_A = \sum_n p_n|\psi_n\rangle\langle\psi_n|$，$\rho_B$ 同谱，秩相同。
- $M$ 本身不宜作纠缠度，宜用其函数即部分熵。

### von Neumann 熵 von Neumann entropy (PDF p56)

定义：两体纯态纠缠度 $E = S(\rho_A) = S(\rho_B)$，$S(\rho) = -\mathrm{tr}(\rho\log\rho) = -\sum_n \lambda_n\log\lambda_n$（对数以 2 为底）。

性质：

- 直积态 $E = 0$，两比特最大纠缠（Bell 基）$E = 1$。
- "局域比全局更混乱"是纯量子特征，经典概率分布得不出。
- 三体以上无 Schmidt 分解，纠缠复杂得多。

### 测量与退相干 measurement and decoherence (PDF p56–57)

定义：把待测系 $A$ 与装置 $B$ 看成复合体系，人们只关心子系 $A$ 时用约化矩阵描述测量结果。

性质：

- 耦合后整体纯（多为纠缠）$\to$ 子系约化矩阵非对角元全部消失，只剩 $p_n = |c_n|^2$ 的混合态，此即统计诠释的含义。
- 文献观点（Cantil–Scully）：测量问题应如此处理，而非直接对 $A$ 用纯态解释。

关系（§1.3 内）：全局纯 vs 局域混——$|\Psi\rangle_{AB}$ 纯而 $\rho_A$ 混是常态，信息藏在关联里；纠缠 vs 经典关联——前者使局域熵大于零而整体熵为零，后者做不到；本节测量观 vs Born 统计诠释——前者是后者的复合体系实现，退相干机制通向第 3 章。
