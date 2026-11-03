# Feature: exp02 拓扑物理量

> 本 spec 分为两部分：
>
> - **Part I — Scientific Description**：说明科学目标、实验 / 计算定义与输出，面向研究者阅读。
> - **Part II — Specification Contract**：定义边界、前置条件、结果条件、不变量与验证要求，作为可检查的规范性约束。
>
> 两部分必须一致；若存在冲突，应先澄清并修正 spec。

## Part I — Scientific Description

### 1. Objective

由 S01 / S02 基态计算轻采样物理量与归一化量，产出 D03（三相代表点归一化结构
因子 `Ŝ(q)=S(q)/L` 曲线，三条同图）与 D04a–D04d（`Ŝ(π)` / `Ô_str` / `Q` / `~Z_R`
四张热力图）。
落盘的 D03/D04a/D04b 数据即为图中绘制的归一化值，不再在出图阶段二次缩放。

不要在这里写实现方案或验收细节（见 Part II）。

### 2. Experiment / Computation Definition

- 输入：S01 网格每点基态波函数 `ψ0`（`256` 分量，基矢约定见 S01 manifest）；
  D03 取其中 S02 三坐标条目（`PRE-001`）。
- 结构因子（见 `docs/experiment-notes/topological_op.md`）：
  `S(q) = (1/L) Σ_{i,j} e^{iq(i−j)} <Z_i Z_j>`，`L=8`，期望取自 `ψ0`。
- D03 q 网格（`PRE-002`）：`q = 2πk/100`（`k = 1,…,99`），即 `[0,2π]` 作
  101 点均匀划分后去边界，共 99 点，显含 `q=π`（`k=50`）；三代表点共用此网格。
- D04a–D04d 网格（`PRE-003`）：`s` 取 S01 的 99 点；`δ` 在 `[-3,3]` 上取 121 点均匀
  （`δ_j = -3 + 0.05(j-1)`，`j = 1,…,121`），逐点计算，不插值、不平滑。
- D04a–D04d 各量（定义见 `docs/experiment-notes/topological_op.md`，`PRE-004`）：
  - (a) `Ŝ(π) = S(π)/L`：上式取 `q=π` 后除以 `L=8`；
  - (b) `Ô_str = −O_str(d=L/2−1=3)`；
  - (c) `Q = 4/3 − 2 Ô_str − (4/3) Ŝ(π)`；
  - (d) `~Z_R`：按 `docs/experiment-notes/topological_op.md` 定义独立重算（`I=(3,4,5,6)` 等）。
- 简并点处理：统一使用 S01 存储的 `ψ0`，不做特殊处理；
  输出数据集逐点携带简并标记（继承自 S01，`PRE-005`）。
- D04a–D04d 四图版式为 `(a) Ŝ(π)` / `(b) Ô_str` / `(c) Q` / `(d) ~Z_R`
  （`PRE-006`）；出图实现本身由实现层安排，不属实验定义。

### 3. Outputs

- D03：q 网格 + 三代表点归一化结构因子 `Ŝ(q)` 曲线（附相标签 trivial / topo / AFM 与代表点坐标）。
- D04a–D04d：四张热力图数据（`Ŝ(π)`、`Ô_str`、`Q`、`~Z_R` 各 `99×121`，
  与 S01 同坐标 ordering），附参数元数据 `(s,δ,L)`；`δ` 覆盖 `[-3,3]` 的 121 点。
- 来源标注：输入 S01 的 schema 与 manifest 标识；每点简并标记。

本节说明输出的科学含义；精确的约束与验收条件写入 Part II
（`POST-001`–`POST-003`）。

### 4. Theory & References

- `docs/planning/experiment-map.md`（exp02 定义：依赖 S01、S02，产出 D03、D04a–D04d）
- `docs/experiment-notes/topological_op.md`（`S(q)`、string、`Ŝ`/`Ô`、`Q` 定义）
- `docs/planning/paper-outline.md`（D03 三线同图、D04a–D04d 四图版式）

复杂推导和背景保留在 `docs/experiment-notes/`，不复制到 spec。

---

## Part II — Specification Contract

本部分只记录具有规范性、可检查意义的约束。每条独立约束使用稳定 ID。

### A. Boundary

#### In Scope

- `BND-001` D03：S02 三个代表点各自的归一化 `Ŝ(q)` 曲线（同 q 网格、三条同图数据）。
- `BND-002` D04a–D04d：S01 网格上每点的 `Ŝ(π)`、`Ô_str`、`Q`、`~Z_R`
 （四幅热力图数据，`(a)–(d)` 分块见 paper-outline）。

#### Out of Scope

- `BND-003` S01 / S02 基态生产（shared-01，保持开放引用）。
- `BND-004` D01 已退役，不再是论文数据产品；D04d 在本 feature 内独立重算，不与任何遗留数据交叉比较。
- `BND-005` 能隙标度（exp03）、VQE 与真机（exp04–exp06）、
  拟设示意图 D06a–D06c（exp04）。

#### Dependencies

- `DEP-001` S01：`data/shared01/`（schema `shared01/v1`），基态波函数 +
  简并点表。
- `DEP-002` S02：三代表点坐标（S01 网格子集，见 S01 manifest；
  代表点波函数即 S01 同坐标条目）。

### B. Notation

只定义本 feature 特有且理解 Contract 所必需的符号。

- `S(q) = (1/L) Σ_{i,j} e^{iq(i−j)} ⟨Z_i Z_j⟩`，`L=8`，期望取自 `ψ0`。
- `Ŝ(q) = S(q)/L`：归一化结构因子；`Ŝ(π)` 即 `q=π` 处取值。
- `O_str`：`d = L/2−1 = 3` 的 string 算符期望。
- `Ô_str = −O_str`：归一化 string 量（取反使拓扑相为正）。
- `Q = 4/3 − 2 Ô_str − (4/3) Ŝ(π)`。
- `~Z_R`：按 `docs/experiment-notes/topological_op.md` 定义（`I=(3,4,5,6)` 等）。

### C. Preconditions

定义合法计算开始前必须成立的条件。

- `PRE-001` 输入：S01 网格每点基态波函数 `ψ0`（`256` 分量）；
  S01 存在且 schema 为 `shared01/v1`、基矢约定一致，否则拒绝执行。
- `PRE-002` D03 q 网格：`q = 2πk/100`（`k = 1,…,99`），`[0,2π]` 作 101 点
  均匀划分后去边界，共 99 点，显含 `q=π`（`k=50`）；三代表点共用此网格。
- `PRE-003` D04a–D04d 网格：`s` 取 S01 的 99 点；`δ` 在 `[-3,3]` 上取 121 点均匀
  （`δ_j = -3 + 0.05(j-1)`，`j = 1,…,121`），逐点计算，不插值、不平滑。
- `PRE-004` D04a–D04d 各量：(a) `Ŝ(π) = S(q=π)/L`；(b) `Ô_str = −O_str(d=3)`；
  (c) `Q = 4/3 − 2 Ô_str − (4/3) Ŝ(π)`；(d) `~Z_R` 按 theory 定义独立重算。
- `PRE-005` 简并点：统一使用 S01 存储的 `ψ0`，
  不做特殊处理；输出数据集逐点携带简并标记（继承自 S01）。
- `PRE-006` D04a–D04d 四图版式：`(a) Ŝ(π)` / `(b) Ô_str` / `(c) Q` / `(d) ~Z_R`。

### D. Postconditions

定义一次成功计算完成后必须成立的条件（除注明外，均按网格点计）。

- `POST-001` D03：q 网格 + 三代表点归一化 `Ŝ(q)` 曲线（附相标签 trivial / topo /
  AFM 与代表点坐标）。
- `POST-002` D04a–D04d：四张热力图数据（`Ŝ(π)`、`Ô_str`、`Q`、`~Z_R` 各 `99×121`，
  与 S01 同坐标 ordering），附参数元数据 `(s,δ,L)`。
- `POST-003` 来源标注：输入 S01 的 schema 与 manifest 标识；每点简并标记；
  具体落盘格式与存储路径由 plan 确定；须保证出图可按 `(s,δ)`（D04a–D04d）
  与按 q（D03）检索。

### E. Invariants

定义在指定计算区间或状态内始终必须成立的条件。

- `INV-001` `S(q) ≥ 0`，故 `Ŝ(q) ≥ 0`（功率谱非负；数值容限 `Ŝ(q) ≥ −1e-12`）。
- `INV-002` D03↔D04a 内洽：D04a 每点等于 D03 同代表点 `q=π` 处取值
  （代表点重合处必一致）。
- `INV-003` `Q` 与 (a)(b) 满足线性组合恒等式（`Q − (4/3 − 2Ô_str − (4/3)Ŝ(π))` 残差 `< 1e-12`）。
- `INV-004` 无缺失、无 NaN；网格坐标与 S01 逐点一致。

### F. Validation

定义如何判断结果满足本 spec。Validation 引用其验证的 Contract ID，
而不是重新定义对应约束。

- `VAL-001` → verifies `INV-001`：`Ŝ(q) ≥ −1e-12`。
- `VAL-002` → verifies `INV-002`：D03 代表点 `q=π` 取值与 D04a 同坐标条目
  bit 一致。
- `VAL-003` → verifies `INV-003`：`Q − (4/3 − 2Ô_str − (4/3)Ŝ(π))` 残差 `< 1e-12`。
- `VAL-004` → verifies `POST-002`、`INV-004`、`POST-003`：无缺失、无 NaN；
  网格坐标（`s` 99 点、`δ` 在 `[-3,3]` 上 121 点）与 S01 逐点一致；
  简并标记与 S01 逐点一致。
- `VAL-005` → verifies `PRE-001`：S01 输入门控（缺失 / schema 不符 /
  基矢约定不符均拒绝）。
- `VAL-006`（诊断，只记录）：D03 三曲线峰位摘要。
  `Ŝ(π)` 作 AFM 标签的解释归论文正文，本 feature 只保证计算正确性。
- `VAL-007`（invalid-run）→ verifies `PRE-001`、`INV-002`、`INV-003`、
  `POST-003`：S01 输入缺失或 schema 不符；D03↔D04a 代表点 `Ŝ(π)` 内洽不符；
  `Q` 恒等式不符；简并标记丢失——出现任一情况相关点（或整批）判 invalid，
  不得静默出图。
