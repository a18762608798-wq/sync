# Implementation Plan: exp07 p=2 分支分辨真机测量与比较

**Branch**: `specs/exp07` | **Date**: 2026-11-03 | **Spec**: `specs/exp07/spec.md`

**Input**: Feature specification from `specs/exp07/spec.md`

> 实现进度见 tasks：2026-11-03 T003 提交在途；后处理按本文末的欧氏概率投影修订执行。

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
本地缓解（归一化 counts、张量积求逆、欧氏概率单纯形投影）→ 组装 D10a/b 真机三分支图层（含窗口内共用端点 +
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


## 2026-11-03 后处理修订：欧氏概率投影

- 复用 Exp06 的归一化、求逆、欧氏单纯形投影和逻辑比特升序标定函数，记录相同的 `readout_mitigation` 方法元数据；单位内 SE 标为 multinomial plug-in 诊断。
- 本次修改发生在 assembler，不改变正在运行的提交器。D10 仍须收齐既定单元后按 `POST-002` 组装；缺少 counts 时以本地合成数据验证算法，正式产物保持待完成。
- 验证重点为投影最优性、计数缩放不变性及不同逻辑比特读出率下的位序；共享函数的解析验证在 Exp06 本地测试中执行，Exp07 回归确认同一入口与方法记录。


## 2026-11-03：旧批次停发及独立优化参数重提

- 旧进程组已停止；固定任务 ID 清单，后台逐项核对并取消可撤销远端任务。旧 `data/exp07/joint/` 移至项目外回收站，不进入正式 D10。
- 新批次绑定 `run_id`、优化协议、S06/manifest/S04 哈希；逐组保存参数哈希，逐任务保存 QASM 哈希。`groups`、账单、单元状态、产品 manifest 的身份必须一致；来源变化或旧状态缺少身份时拒绝续跑。
- 只使用 `exp04/v2`、`independent-global-lbfgs-v1` 且全部所用分支已收敛、无 `stagn` 的参数；对全部 $90$ 个测点进行 Qiskit 态矢量能量交叉核验。
- 新账单沿用本轮作者明确授权的 $500$ 单元、每单元 $92$ 电路、每电路 $1024$ shots；生成后记录授权来源，不复用旧批次确认状态。使用独立后台会话和文件锁启动，逐任务增量记账、回收、组装并验收 D10。
