# Implementation Plan: exp06 真机测量与比较

**Branch**: `specs/exp06` | **Date**: 2026-10-04 | **Spec**: `specs/exp06/spec.md`

**Input**: Feature specification from `specs/exp06/spec.md`

## Summary

在 S04 top1 比特上测 S03 `p=1` 最优电路的 hat 量：两线同窗口 `30` 点
（`15` 个 `s` × `δ∈{0.85,−2}`，每个 `s` 先 `0.85` 后 `−2`）组成一个
测量单位（`30` VQE + `2` S05 标定 = `32` 电路同批，`1024` shots）。
关键简化（已由 theory 保证）：
`S(π)` 与 string 皆为全 `Z` 对角观测量，单点只需 **1 个 estimator 电路**。
单轮 `500` 单位跑满，中途不截停不结算；收齐后按窗口内规则定两线共用端点
（pooled `30` 点均值的top-1 最大值），真机侧 max 归一化、
模拟机侧固定 hat 尺度，两边同公式组 `Q` 后直接比 raw 值
（`d_raw`）与 `r`（report-only，无阈值门）。
技术路线：Python/Qiskit 复刻 exp04 拟设，先经 Aer 态矢量与 S06
黄金交叉锁定电路构造器，再走真机提交（`correct=False`、opt3、显式 coupling_map）；
本地缓解（逐比特 `M⁻¹` + 非负约束）→ 组装 D08a/b 真机图层（含窗口内共用端点 +
最优偶数长度窗口搜索 + `d_raw`/`r` 报告 + S06 `p=1,2` 叠放）→ 出图。
v2 分线数据整体归档为 `protoV2`，不与 v3 联测数据混存；v3 跳过试水，
直接正式（Baihua）；跑新任务前先取消旧在途任务。

以上均为实现层选择；点位、比特、参数来源、shots/标定、矫正开关、
轮次/窗口/比较规则与验证条件沿用 spec，未改动实验语义。

## Technical Context

**Language/Version**: Python（Qiskit 电路构造 + 真机提交 + 本地缓解/组装；
本实验零 Julia 新增，只只读消费 npz）

**Primary Dependencies**: `qiskit==2.5.1`（电路 + 转译 opt3）+
`qiskit-aer==0.17.2`（黄金交叉态矢量仿真）+ `qmeas`（`quark_client` 提交/
轮询复用、`benchmark.io` checkpoints 思想复用；版本记入 manifest）+
`quarkstudio==7.3.9`（提交后端，`correct=False`）+ `numpy`（缓解/观测量）

**Storage**: 两层落盘——原始层 `data/exp06/joint/units/<unit_id>/` 逐单位 JSON
（counts + tid + 提交参数，增量落盘，中断续跑只补缺失）；产品层
`data/exp06/joint/exp06_D08_joint.npz` + `exp06_manifest.json`
（schema `exp06/v3`，S05 矩阵随 D08a/b 存档，窗口内共用端点记入）；
v2 分线数据（`data/exp06/dm2/`、`data/exp06/d085/`）整体归档
（`data/exp06_protoV2_*/`），不与 v3 联测混存；旧协议 `δ=0` 线数据
（`data/exp06_protoV1_*`）已删除不再使用（用户 2026-10-30 确认）。

**Testing**: `pytest`（纯本地：初态/轨道电路酉对照、Aer 黄金交叉、
缓解恒等式、Q 组装、窗口搜索复算、D08a/b 归一化、manifest schema；
零真机调用）

**Target Platform**: Linux（本机编排）+ Baihua 真机（两路 top1 皆 Baihua，
单芯片，无跨芯片批次）

**Project Type**: 硬件测量编排（thin orchestration；电路构造器为本 feature
内新写 Julia→Python 复刻，经黄金交叉锁定）

**Performance Goals**: 账单：单轮 500 单位 ×32 电路 = 16000 任务
×1024 shots ≈ 1600 万 shots（由 preview 打印、人工确认覆盖）；
v3 无试水轮，直接正式。

**Constraints**: bill 未人工确认不得提交；S03 无对应点判 invalid 不补优化；
平台矫正关闭（提交参数留存备查）；转译绕行仅 topo `0–7` link 允许，
其余候选外纠缠门仍判 invalid

**Scale/Scope**: 真机单轮 500 单位（v3 联测）；D08a/b 两面板
（`δ × Q`，每面板模拟机 `p=1,2` 两线 + 真机 `p=1` 窗口散点；
真机侧共用端点 max 归一化，模拟机侧固定 hat 尺度）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- I（Spec 权威）：点位 / 比特 / 参数 / shots / 标定 / 开关全在 spec；
  本 plan 只定 `basis_gates`、归一化区间、诊断阈值、记录方式等实现细则。
  PASS。
- II（分离）：不碰 `docs/experiment-notes/`；Qiskit 电路复刻以 ansatz/psi0 为准，
  theory 不进代码注释外的定义。PASS。
- III（边界）：S03/S06/S04 只读消费，不复算；提交/轮询复用
  `qmeas.random.quark_client`，不重写；电路构造器归本 feature，
  不建跨 feature 共享框架。PASS。
- IV（可重复）：快照引用（S04）+ 逐任务增量落盘 + manifest（S03 记录引用、
  `θ` 快照、`rng`、标定批次、栈版本、转译参数、schema `exp06/v1`）+
  提交/收回对账 + 缓解前后值双存档。PASS。
- V（正确性优先）：Aer 黄金交叉先行（构造器锁定后才碰真机）；
  转译 opt3 是 spec 语义（用户确认），抽样审计 CZ 行为只记录；
  预览零机时；无嵌套并行（提交并发由工具链内部控制）。PASS。
- VI（风格）：Python 经 qmeas env 统一解释器；出图走
  `scripts/figure_style.py`，mathtext，矢量 PDF + 300dpi PNG。PASS。

## Project Structure

### Documentation (this feature)

```text
specs/exp06/
├── spec.md               # 实验定义（已定，Q1–Q5 全闭）
├── plan.md               # 本文件
└── tasks.md              # tasks 阶段产出（非本 plan 创建）
```

### Source Code (repository root)

```text
scripts/
├── exp06_circuits.py     # 初态制备 + orbit 拟设 Qiskit 构造器（θ,S03,a*→电路；§3）
├── exp06_preview.py      # 离线：S03 点位映射（15 点/线，只 `p=1`）→ 轮划分（1000 单位/轮，试水轮单独）→ 账单（零机时）
├── exp06_submit.py       # 真机提交：转译（opt3/coupling_map）→ 逐轮提交 → 对账 → 补跑（含试水轮，`task_id` 留存）
├── exp06_assemble.py     # 本地缓解（S05 M⁻¹+非负）→ `Q` 组装 → 全局最优窗口搜索 + 判据 → exp06_D08.npz（含窗口+全量单位+S05）+ manifest（v2）
├── verify_exp06.py       # 生产断言（见 §4）
├── plot_D08.py           # D08a/b 两面板：模拟机 `p=1,2` 两线 + 真机 `p=1` 窗口散点，各自归一化 → figs/exp06/
data/exp06/
├── batches/<unit_id>/    # 逐单位 JSON（counts/tid/提交参数；中断续跑只补缺失）
├── exp06_D08.npz / exp06_manifest.json   # schema exp06/v2
data/exp06_pilot/         # 试水单位（不计 N，链路验证 + ε 标定参考）
figs/exp06/
test/
└── test_exp06_local.py   # pytest（零真机调用；Aer 黄金交叉为核心门）
```

**Structure Decision**: 薄编排 + 单一新构造器。Julia 侧零新增；`qmeas.estimator`
runner 不直接复用（其按 Pauli 分组提交多电路；本实验全 `Z` 对角只需单电路，
自写更薄的提交循环，但提交/轮询原语复用 `quark_client`）。

## 1. 实现思路

- 数据流：读 S03（`meta=(δ_idx,s_idx,p,a*)`，`a*∈{1,2,3}=triv/topo/afm`；
  `θ` 行 `NaN`-pad）→ 稀疏点过滤（`s_idx∈{1,8,…,99}`，两线各 `15` 点，
  只取 `p=1`；S03 缺点直接标 invalid）→ 组 `30` 点联合单位
  （每 `s` 先 `δ=0.85` 后 `δ=−2`，`g[2i]=0.85`、`g[2i+1]=−2`）
  → preview 账单（单轮 500 单位，`16000` 任务）→ **人工确认** →
  电路构造（§3）→ Aer 黄金交叉（见下，通过后才提交；构造器 v2 已锁定，
  联测只复用，不改参数）→ 转译抽样审计 → 逐单位提交（每单位
  `30` VQE + `2` 标定同批，`correct=False`）→
  对账补跑 → 本地缓解 → 组装 D08a/b 真机图层（全量单位三件套/
  单位内传播 SE /S03 与 S05 引用 + 收齐后窗口内共用端点 +
  最优偶数长度窗口搜索 + `d_raw`/`r` 报告）→
  S06（`p=1,2`，固定 hat 尺度）叠放 → verify → 出图；无阈值门，
  不截停，报告完即收尾（manifest `v3` 冻结）。
- Aer 黄金交叉（构造器锁定门，零机时；v2 已通过，v3 联测沿用构造器，
  只对新 `30` 点组合作出图前复核，不重锁定）：每 `(a*,p=1,δ∈{−2,0.85})`
  抽样点，Qiskit 电路经 Aer 态矢量仿真求 `S(π)`/string/`Q`/能量，
  与 S06 同点值比对（容限 `1e-8`，转译前逻辑电路比对，绕开硬件噪声）；
  任一超差即停。
- Aer 黄金交叉（构造器锁定门，零机时）：对每 `(a*,p=1,δ∈{−2,0.85})` 抽样点，
  Qiskit 电路经 Aer 态矢量仿真求 `S(π)`/string/`Q`/能量，与 S06 同点值比对
  （容限 `1e-8`，转译前逻辑电路比对，绕开硬件噪声）；任一超差即停，
  修构造器（多半是轨道配对/子层顺序问题）。
- 缓解：每单位由 2 标定电路得 8 比特各自 `M`（全 `0` 电路给 `P(·|0)` 列，
  全 `X` 给 `P(·|1)` 列）；对 256 维经验分布做 Kronecker-`M⁻¹`
  （逐比特独立），负值截零重归一；缓解前后观测量双存档。
- D08a/b 叠放：真机窗口曲线（段内单位逐点平均除以本窗口共用端点）与
  S06 模拟 `p=1,2` 的 `Q` 值（固定 hat 尺度组出，同 `30` 点）
  直接比 raw（`d_raw`）+ `r`；模拟 `p=1` 曲线同口径并列展示
  （只看趋势，不进比较）；组合 `Q` 不做二次归一化。
  共用端点（`S_max`、`O_max`、top-1 最大值（窗口内））独立记录
  （plan 级细则，记入 manifest），同图比较只看形状与位置。

## 2. 代码与模块结构

- `scripts/exp06_circuits.py`：`build_init(a*)`（单态：`X+H+CX` 相位正确；
  GHZ：`H` + CNOT 链；与 `Exp04.InitStates` 逐振幅对照测试）、
  `build_ansatz(theta,a*,p,delta)`（轨道配对 `O_j↔O_{M+1-j}` /
  `E_j↔E_{M-j}`、子层顺序按初态 `F/S`、
  每键 `RXX(tx)RYY(tx)RZZ(tz)`；与 `Exp04.Ansatz` 语义逐项对应，
  对应表写进模块 docstring）、`build_estimator_circuit(...)`
  （初态 + 拟设 + 全 `Z` 测量；topo 用环状 coupling 信息仅作逻辑标注，
  物理映射在 submit 侧）、`build_calib_circuits(n)`（全 `0` / 全 `X`）。
- `scripts/exp06_preview.py`：S03 读入（只 `p=1`）→ 稀疏过滤（两线各 `15` 点）
  → 组 `30` 点联合单位（每 `s` 先 `δ=0.85` 后 `δ=−2`）→ 单轮 `500` 单位账单
  （`16000` 任务 ≈1600 万 shots；快照/S03 引用）→
  `bill.json`（`confirmed=false`）。
- `scripts/exp06_submit.py`：读 `bill.json`（须 confirmed）→ 转译抽样审计
  （opt3 下记录 CZ 数/深度行为，topo 绕行预期内）→ 单轮提交（每单位
  VQE 30 + 标定 2 同批，`correct=False` 参数留存）→ checkpoints 增量落盘
  → 对账补跑（`task_id` 清单留存）
  （exp05 同模式：有 tid 只轮询不重提，Failed 显式 query）。
  跑新任务前先取消旧在途任务（服务端 mass-cancel + 本地确认 pending 清零）。
  （exp05 同模式：有 tid 只轮询不重提，Failed 显式 query）。
  转译后电路摘要（CZ 边集）随 checkpoints 留存，供 verify 验路断言。
- `scripts/exp06_preview.py`：S03 读入（只 `p=1`）→ 稀疏过滤（两线各 `15` 点）
  → 组 `30` 点联合单位（每 `s` 先 `δ=0.85` 后 `δ=−2`）→ 单轮 `500` 单位账单
  （`16000` 任务 ≈1600 万 shots；快照/S03 引用）→
  `bill.json`（`confirmed=false`）。
- `scripts/exp06_submit.py`：读 `bill.json`（须 confirmed）→ 转译抽样审计
  （opt3 下记录 CZ 数/深度行为，topo 绕行预期内）→ 单轮提交（每单位
  VQE 30 + 标定 2 同批，`correct=False` 参数留存）→ checkpoints 增量落盘
  → 对账补跑（exp05 同模式：有 tid 只轮询不重提，Failed 显式 query）。
  转译后电路摘要（CZ 边集）随 checkpoints 留存，供 verify 验路断言。
  跑新任务前先取消旧在途任务（服务端 mass-cancel + 本地确认 pending 清零）。
- `scripts/exp06_assemble.py`：读 joint units → S05 矩阵 → 缓解 →
  `Ŝ(π)`、`Ô_str` 组装（公式只读复刻 Exp02/TopoOp）→ 对每个候选窗口
  用其 pooled `30` 点均值的 top-1 最大值做端点 → 同公式组 `Q`
  （真机除端点 / 模拟固定 hat，不二次归一化）→ 最优偶数长度窗口搜索
  （`r` 最大规则）+ `d_raw`/`r` 报告 →
  写 `data/exp06/joint/exp06_D08_joint.npz`
  （全量单位 + 端点 + 窗口 + S05 随附）+ `exp06_manifest.json`
  （schema `exp06/v3`：S03/S04/S06 引用、点位、`θ` 快照、单位表、转译参数、
  栈版本、窗口/端点/report-only 声明）。
- D03 真机三点数据流（`POST-008`）：读 S03 同点 `p=1`（三代表点 D09 获胜分支
  初态 + 最优 `θ*`）→ 组 estimator（含 S05 标定 2 电路）→ `Z` 基 `1024` shots
  三点独立测量 → S05 缓解 → 全部 `⟨ZiZj⟩` Fourier 组 `S(q)` 除以 `L`
  → 写 `data/exp06/d03hw/` + multinomial SE；overlay 出图待数据到后扩展
  `plot_D03D04.py` 落（T028）。
- `scripts/plot_D08.py`：D08a/b 两面板（`δ × Q`）：每面板模拟机
  `p=1,2` 两线（固定 hat 尺度组出）+ 真机 `p=1` 窗口散点及单位间误差棒
  （真机侧除以本窗口共用端点；两面板共用同一窗口端点，不各自归一化；
  真机点按 D09 获胜分段着色；只读 assemble 与 S06 出图，不生产数据）。
- `scripts/exp06_d03hw.py`（T027 新建）：D03 三代表点 estimator + S05 标定
  电路组装与提交/收回（复用 `exp06_circuits` 构造器与 submit 对账原语）、
  S05 缓解、`Ŝ(q)` 组装 + multinomial SE、落盘 `data/exp06/d03hw/`。
- `scripts/plot_D08D09.py`：纸面层 `2×2` 合图（spec `POST-003` 末段）：
  上排复用 D09 两面板（`exp04_D09.npz`，`δ=−2` / `0.85` 代价函数），
  下排复用 D08 两面板（`exp06_D08_joint.npz`，固定 hat 曲线 + 真机窗口散点），
  标签 `(a)–(d)` 置于各子图左下方；只读上述 npz，不重算、不覆盖
  `exp04_D09` 与 `exp06_D08` 两个原产品。
- `test/test_exp06_local.py`：初态振幅对照（vs 解析式）、单键酉对照、
  Aer 黄金交叉（抽样点 vs S06，`1e-8`）、缓解恒等式、hat 组装、
  共用端点（top-1 最大值，窗口内）复算、偶数窗口搜索复算（`r` 选优并列规则）、
  manifest `v3` 必填字段。

## 3. 数值与技术决策

- 解释器：全 Python 经 qmeas env（Qiskit + Aer + qmeas 同 env，
  与 exp05 一致）；manifest 记解释器路径 + `qiskit`/`qiskit-aer`/
  `qmeas`(git commit)/`quarkstudio` 版本。
- `basis_gates`：`["rz", "rx", "ry", "cz"]`（与 exp05 同；单/双比特门集
  覆盖单态制备与 `RXX/RYY/RZZ` 分解；记入 manifest）。
- 物理比特映射：逻辑 `0..7` 按 S04 序列映射物理比特（run1 取值示例：
  链 top1 `[77,…,70]`；topo 用 D07c Rank1 子链 `[84,83,82,69,70,71,72,73]`，
  Baihua；以新 S04 落盘值为准，preview 打印映射表备查）；topo 转译
  `coupling_map` = 子链 7 边 + `0–7` 闭合边
  （首尾经环剩余比特绕行由优化器定，见 §1 link 语义）。
- GHZ 初态采用中间发起版（手写，逻辑同
  `qmeas.models.xxz.get_initial_state(8, pidx=0)`：H 打中间比特、两路 CNOT
  向左右散开、翻奇位；纠缠级联深度 `~n/2`，真机退相干更小）。手写而不用
  qmeas 原函数的原因：三初态构造器保持零外部依赖、单源可审计，避免只有
  GHZ 一路依赖 qmeas 的不对称。替换原因：端点起链版深度 `~n`，中间发起减半；
  已逐振幅比对 `docs/experiment-notes/psi0.md` 解析式一致（`{85,170}` 均为 `+1/√2`）。
  不得回退到端点版（以 psi0 解析式为准）。
- 单位与重复策略：单位即重复——同单位内 `30` 点（两线交错）+ `2` 标定
  同批提交（自然时间相邻，防漂移，两线共漂移）；图上误差棒用展示窗口内
  单位间标准误（逐点跨单位 SE）；单位内 multinomial 解析标准误经 hat 量
  定义传播，只存档备查（诊断 / 权重线索，不上图）。
- 轮次与顺序（plan 级细则）：v3 单轮 `500` 单位一次跑满（Baihua），
  中途不截停、不结算；收齐后搜窗口、报告（端点按窗口内规则定）；
  提交严格串行交替：`SUBMIT_CONCURRENCY=1`，按 `(uid, g序)` 逐个直发
  （`g` 序即每 `s` 先 `δ=0.85` 后 `δ=−2` + `2` 标定殿后），直发顺序即
  平台排队顺序，同单位 `32` 任务自然时间相邻；轮询并发不限
  （只收数，不影响芯片侧执行序）；
  v3 无试水轮；跑新任务前先取消旧在途任务（d085 在途约 `17000` 待收回，
  服务端 mass-cancel；dm2 确认无 pending 后再动手）。
- 窗口与比较（plan 级细则）：不对端点做全局冻结——扫描时对每个候选
  偶数长度子段，用其 pooled 逐点均值（`30` 点）取每 hat 量 top-1 最大值记
  `S_max`、`O_max` 并随窗口记入 manifest；真机侧除以本窗口端点（窗口内
  最大→`1`，最小不管），模拟机侧固定 hat 尺度（`Ŝ=S/8`、`Ô=−O`）；
  两边同公式组 `Q`，组合后不做二次归一化；
  窗口曲线 = 段内单位逐点平均后直接比 raw（`d_raw`）+ `r`（`30` 点）；
  `Q_sim` 参照层取 `p=1`（`p=2` 仅图示对照，不参与选窗）。
  搜索偶数长度（`10,12,14,…`，上限为收齐时 `N`），取 `r` 最大
  （并列取 `d_raw` 最小，再并列取更长，再并列取更早）；
  report-only，无阈值门、无达标即停；阈值待数据出来后再定。
  试水 + 旧数据组 `Q` 只做可达性标定参考，不反向调参。
- 修订记录：2026-10-28（窗口内端点 Q14）：取消共用端点全局冻结，
  每个候选窗口用自己 `30` 点 pooled 均值的 top-1 最大值做端点并随窗口记录；
  搜索即组装（端点按窗口算），verify 同口径复算。
- 修订记录：2026-10-30（串行交替提交）：`SUBMIT_CONCURRENCY=20` 并发打散
  同单位时间相邻性，`mass-cancel` 旧 `16000` tid 后按 `(uid, g序)`
  串行（`=1`）重提；轮询并发不限。
- 修订记录：2026-11-01（选窗参照层）：原代码取 S06 `p=2` 列作 `Q_sim`，
  与"真机 `p=1` 对模拟 `p=1`"口径不符；改为 `p=1` 列，`p=2` 只作图内对照。
  窗口与端点为派生量，重跑组装/验证/出图，`counts` 不变。
- 缓解数值：`M` 条件数检查（`cond > 1e6` 标可疑，诊断不设硬门）；
  Kronecker 逆经 `numpy`，256 维可忽略。
- 离散度诊断阈值（spec 授权 plan，只记录）：某点单位间标准差
  超同线中位数 `5` 倍则标记（需人工看是否为漂移段）。
- D08a/b 比较：真机窗口曲线（段内单位逐点平均除以本窗口共用端点）与
  S06 模拟 `p=1,2` 的 `Q` 值（固定 hat 尺度组出，同 `30` 点）
  直接比 raw（`d_raw`）+ `r`；模拟 `p=1` 曲线同口径并列展示
  （只看趋势，不进比较）；组合 `Q` 不做二次归一化。
  共用端点（`S_max`、`O_max`、top-1 最大值（窗口内））独立记录
  （plan 级细则，记入 manifest），同图比较只看形状与位置。
- M1 取证结论（2026-10-04 已办，T000 关闭）：平台读出矫正开关是 task
  payload 的 `options.correct`（quark `quafu.py` 任务文档：
  `'correct': False, # readout error correction`），与
  `QuarkOptions.mitigation` 无关；`submit_quark`
  （`qmeas/random/quark_client.py:104`）已透传 `"correct": opts.correct`，
  默认 `False` 即关闭。exp06 提交保持默认并留存参数，verify 查
  `correct=False`；spec/plan/tasks 内旧称 `mitigation=False` 一律改
  `correct=False`（术语修正，语义不变）。

## 4. 验证方案（覆盖 spec Contract F）

- `test_exp06_local.py` 先行全绿（含 Aer 黄金交叉门），否则不得提交。
- `verify_exp06.py` 对正式输出全量执行：
  - 每单位 `30` 点齐全；缓解前后双存档；`θ` 与 S03 同点 `p=1` 逐元一致
    （`NaN`-pad 区除外）；S05 单位 id 与 VQE 同单位；
    提交参数 `correct=False` 留存可查。
  - D03 三点（`POST-008`）：`θ` 与 S03 同点 `p=1` 记录一致；counts +
    缓解后 `Ŝ(q)` + multinomial SE 三件套齐全；S05 同点引用；
    `Ŝ(q)` 与模拟机同 `q` 网格同归一化可直接 overlay。
  - 转译验路断言（spec `VAL-008` 条目）：转译后电路的 `CZ` 边集须落入
    允许集（链：子链相邻 `7` 边；topo：子链 `7` 边 + `0–7` 绕行
    `0-10-9-7`），边集由 checkpoints 留存的转译摘要重算比对；
    未落入即相关单位 invalid。
  - 对账：任务数 == 收回数 + 明确标记（`task_id` 清单）；
    无静默丢弃；无已收回重提。
  - 窗口复算：连续性、偶数长度 `≥10`、`r` 选优并列规则、`d_raw`/`r`、
    共用端点与 manifest 一致（按窗口内规则复算）、
    披露字段齐全；任一不合即相关窗口判 invalid。
  - invalid 任一触发即相关单位（或整窗）判 invalid，非零退出指明点位。
  - 诊断输出：缓解前后差值分布、离散度标记、D08a/b 目检提示。
- 出图前人工核对：D08a/b 点位/误差棒与 npz 一致、共用端点与窗口记录正确。
- 修订记录：2026-10-25（窗口统一 `len=20`）：两线展示窗口固定长度 20，
  只搜起点（dm2 原 12 与 20 的 `d` 几乎并列 0.07555/0.07560）；阈值不变。
- 修订记录：2026-10-25（中检粒度）：`N=500` → **每满 100 单位**一次
  只读 assemble（达标即停线）；ladder 升级点仍在首轮 `N=1000` 结算。
- 修订记录：2026-10-25（Q 归一化改 `[-1,1]`）：与 `Q` 定义值域一致，
  原 `[0,1]`；`d` 阈值按 ×2 换算（dm2 v2.0/v2.1/v2.2 = 0.30/0.40/0.50、
  d085 = 0.08），`r` 阈值不变；出图与判据同口径。
- 修订记录：2026-10-25（d085 加严）：`δ=0.85` 线判据改 `d<0.04`、`r>0.9`、
  窗口长度固定 `12`（只搜起点），无 ladder；dm2 维持 v2.0 ladder。
  2026-10-26（判据 ladder）：v2.0（`d<0.15`）→ `N=500` 中检
  远达不到（最优 `d` 超目标 `0.1`）则 v2.1（`d<0.2`）→ 首轮 `N=1000` 结算
  仍远达不到则 v2.2（`d<0.25`）FINAL 封顶；`r>0.4` 不变；升级后重扫。
  2026-10-24（v2 新协议）：`δ∈{0,0.85}×33点×p=1,2,3` 退役，
  改 `δ∈{−2,0.85}×15点×只p=2`；测量单位（15 点×1024 + 1 次 S05 标定），
  轮 `1000` 单位 / 上限 `5000` 每线，先 `δ=−2` 后 `δ=0.85`；
  全局最优连续窗口（`≥10`）达标即停（`d<0.15 & r>0.4`，暂定，试水后锁死）；
  D08 四面板退役为 Q 两面板（模拟 `p=1,2` + 真机 `p=2` 窗口）；
  旧 `δ=0` 数据归档，manifest 升 `exp06/v2`。
- 修订记录：2026-10-26（v3 联测）：测量单位改为两线同窗口 `30` 点
  （每 `s` 先 `δ=0.85` 后 `δ=−2`）+ S05 共 `32` 电路；单轮 `500` 单位跑满，
  中途不截停不结算；v2 分线数据归档 `protoV2` 废弃；真机侧共用端点
  （pooled 前二大均值冻结）max 归一化、模拟机侧固定 hat 尺度，
  组 `Q` 后比 `d_raw` + `r`，不二次归一化；偶数长度按 `r` 选最优窗口；
  report-only 无阈值门；跳过试水直接正式；manifest 升 `exp06/v3`。
- 修订记录：2026-10-28（端点改 top-1）：共用端点由前二大均值改为
  pooled `30` 点均值的 top-1 最大值（Q13），归一化后恒 `≤1`；
  规范与脚本同步改，10-26 记录原文保留。
- 修订记录：2026-10-30（真机深度 `p*=2` 改 `p*=1`）：已收 `355` 个
  `p=2` units 废弃归档（`data/exp06_protoV3p2_*/`），重测单轮 `500` 个
  `p=1` 联测单位（规则同 v3）；规范与脚本 `p=2` 字样同步改 `p=1`，
  Q12–Q14 记录原文保留。

## Complexity Tracking

本次 plan 无宪法违反，无需记录。
