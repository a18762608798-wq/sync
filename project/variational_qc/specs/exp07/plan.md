# Implementation Plan: exp07 p=2 分支分辨真机测量与比较

**Branch**: `specs/exp07` | **Date**: 2026-11-03 | **Spec**: `specs/exp07/spec.md`

**Input**: Feature specification from `specs/exp07/spec.md`

> 初稿（实现未开始）：技术路线沿用 exp06，分支维度是唯一增量。真机任务未提交，零机时。

## Summary

在 S04 top1 比特（沿用 exp06 口径）上测 S06 `p=2` 三分支各自最优电路的 hat 量：
一个测量单位 = `90` 点（`15` 个 `s` × `δ∈{0.85,−2}` × 三分支，
每个 `s` 先 `0.85` 后 `−2`，每个 `(s,δ)` 内按 triv→topo→AFM 顺序）
各 `1024` shots + `1` 次 S05 标定（`2` 电路）= `92` 电路同批提交。
关键简化（已由 theory 保证，与 exp06 相同）：
`S(π)` 与 string 皆为全 `Z` 对角观测量，单点只需 **1 个 estimator 电路**。
单轮 `500` 单位跑满（`46000` 电路任务），中途不截停不结算；
收齐后按窗口内 `90` 点 pooled 规则定三分支两线共用端点
（pooled 逐点均值的 top-1 最大值），真机侧统一 max 归一化、
模拟机侧取 S06 现成 `p=2` 获胜分支固定 hat 尺度（`q_sim_p2` 口径，不重算），
两边同公式组 `Q` 后直接比 raw 值（`d_raw,a`）与 `r_a`（report-only，无阈值门）。
技术路线：复用 exp06 电路构造器（`build_init(a)` / `build_ansatz(theta,a,p=2,delta)`，
分支参数改取 S06 `theta_leg` 的 `p=2` 子集），先经 Aer 态矢量与 S06 分支能量
`leg_E` 黄金交叉锁定构造器，再走真机提交（`correct=False`、opt3、显式 coupling_map）；
本地缓解（逐比特 `M⁻¹` + 非负约束）→ 组装 D10a/b 真机三分支图层（含窗口内共用端点 +
最优偶数长度窗口搜索 + `r_a`/`d_raw,a` 报告 + S06 `p=2` 灰线叠放）→ 新开一图出图。
数据独立存档 `data/exp07/`，不与 exp06 混存。

以上均为实现层选择；点位、比特、参数来源、shots/标定、矫正开关、
轮次/窗口/比较规则与验证条件沿用 spec，未改动实验语义。

## Technical Context

**Language/Version**: Python（Qiskit 电路构造 + 真机提交 + 本地缓解/组装；
本实验零 Julia 新增，只只读消费 npz）

**Primary Dependencies**: `qiskit==2.5.1`（电路 + 转译 opt3）+
`qiskit-aer==0.17.2`（黄金交叉态矢量仿真）+ `qmeas`（`quark_client` 提交/
轮询复用；版本记入 manifest）+
`quarkstudio==7.3.9`（提交后端，`correct=False`）+ `numpy`（缓解/观测量）

**Storage**: 两层落盘——原始层 `data/exp07/joint/units/<unit_id>/` 逐单位 JSON
（counts + tid + 提交参数，增量落盘，中断续跑只补缺失）；产品层
`data/exp07/joint/exp07_D10_joint.npz` + `exp07_manifest_joint.json`
（自定 schema，分支三件套均值/标准误 + 端点 + 窗口 + `r_a`/`d_raw,a` +
pooled 诊断 + S05 / S06 / S04 引用）；S04 快照引用 exp05 落盘，不重算。

**Testing**: `pytest`（纯本地：分支参数读取、初态/轨道电路酉对照、Aer 黄金交叉
（抽样 `(δ,s,a)` vs S06 `leg_E` 的 `p=2` 子集，容限 plan 定）、
缓解恒等式、Q 组装、窗口搜索复算、D10a/b 归一化、manifest schema；
零真机调用）

**Target Platform**: Linux（本机编排）+ Baihua 真机（两路 top1 皆 Baihua，
沿用 exp06 比特口径）

## Key Steps（实现时展开）

1. 复用 exp06 电路构造器，分支参数源切换为 S06 `theta_leg[p=2]`；
   Aer 黄金交叉锁定后冻结构造器版本（记入 manifest）。
2. 离线预览打印账单（`90` VQE + `2` 标定 = `92` /单位 × `500` 单位，
   另计 invalid 跳过）→ 人工确认后提交；逐单位增量落盘。
3. 本地缓解 + 组装 `exp07_D10_joint.npz`（端点/窗口/`r_a` 规则见 spec `POST-002`）。
4. 新开 `figs/exp07/exp07_D10.pdf/png`（`1×2`，模拟机灰线 + 三分支散点，
   `(a)(b)` 与 `s` 标签样式沿用 D08D09 新样式）。

## Risks

- 单轮 `46000` 任务约为 exp06 v3 的三倍，账单确认时重点复核费用与配额；
  若超预算，拆轮方案须先回 spec 修 `PRE-007`（不得静默减点）。
- S06 中某分支整段 invalid（`conv`/`stagn` 皆假）会导致该分支散点断裂；
  按 `POST-001` 标记，不插值、不借用他分支参数。
