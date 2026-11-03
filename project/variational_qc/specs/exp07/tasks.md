# Tasks: exp07 p=2 分支分辨真机测量与比较

**Feature:** exp07

任务必须来源于 `spec.md` 和 `plan.md`。
不得在 tasks 阶段引入新的实验定义。

> 状态：2026-11-03 T000/T001/T006 已完成（T006 5 项全绿，aer 0.18.2；缓解/Q/窗口/manifest 断言随 T004 扩充）；T002 账单已由用户直接授权确认（2026-11-03，免等待门）；随即进 T003。
>
> T000 记录：qmeas 源码默认 `correct=False`（config.py:56，quark_client:115 透传），T003 须沿用显式 `correct=False` + assert。
> T001 记录：复用 exp06 构造器 + S06 `theta_leg[si,a,p=2]` 分支层，90 点零 invalid。
> T003 记录：token 经服务端建连验证通过（此前报 invalid 系写入多一括号，已修正）；提交进程已挂后台跑（46000 任务串行提交+轮询），日志 /tmp/sub07.log。
> T003 续跑：2026-11-03 18:37:34 +08 按用户要求重启；独立后台会话 PID 1056876，提交 Python PID 1056881，日志 `/tmp/variational-qc-exp07-resume-20261103-183722-whf5d0r6/submit.log`，退出码落同目录 `exitcode`，使用文件锁防止重复启动。
> 续跑核验：18:39:28 +08 已登记 16789 个任务，较重启前新增 128 个；原有 16661 个任务 ID 全部保持一致，counts 仍为 0（全轮提交后统一轮询）；T003 保持进行中。
> 前置：S06 `p=2` 分支参数与 `q_sim_p2` 口径已就绪（exp04 落盘）；
> S04 比特口径沿用 exp06（引用，不重算）。

## Implementation

- [x] T000 提交前复核 `correct` 默认：确认提交代码未改动
  `QuarkOptions.correct` 默认（`False`），提交参数逐批留存备查。
  完成条件：复核通过；若被改动则停，返工 plan，不进 T003。
- [x] T001 实现 `scripts/exp07_circuits.py`（可复用 exp06 构造器并分支化）：
  `build_init(a)`（三初态，与 psi0 解析式逐振幅对照）、
  `build_ansatz(theta,a,p=2,delta)`（轨道配对/子层顺序/`RXX/RYY/RZZ` 单键，
  对应表写进 docstring）、`build_estimator_circuit`（+全 `Z` 测量）、
  `build_calib_circuits`（全 `0` / 全 `X`）。
  完成条件：模块可加载，三分支初态振幅正确（由 T006 锁定）。
- [x] T002 编写 `scripts/exp07_preview.py` 并执行离线预览：S06 `theta_leg`
  的 `p=2` 子集读入 → 分支有效性过滤（`conv`/`stagn` 皆假标 invalid）
  → `92` 电路/单位 × `500` 单位划分 → 账单
  （VQE `45000` + 标定 `1000` = `46000` 任务，快照/S06 引用，
  `confirmed=false`）。
  完成条件：账单已打印、经人工确认（确认记录留存），零机时，
  未确认前不得进入 T003。
- [ ] T003 编写 `scripts/exp07_submit.py`（转译 opt3/显式 coupling_map；
  对账补跑沿用 exp05 模式）并执行真机提交（人工确认 + T000 通过后）：
  逐批提交（VQE + 标定 `2`，`correct=False` 参数留存），
  增量落盘 `data/exp07/joint/units/<unit_id>/`，中断续跑只补缺失。
  完成条件：`500` 单位全收回（或明确标记），无静默丢弃，无已收回重提。
- [ ] T004 编写 `scripts/exp07_assemble.py` 并组装产品：S05 矩阵 →
  归一化 counts、Kronecker 求逆和欧氏概率投影 → `S(π)`/string（公式只读复刻 Exp02）→
  写 `data/exp07/joint/exp07_D10_joint.npz`（全量 `90` 点/单位缓解后均值/
  单位间 SE/每点三件套 + `90` 点 pooled 共用端点 + 最优偶数长度窗口
  （`mean(r_a)` 规则）+ `r_a`/`d_raw,a` + pooled 诊断 + S06/S04/S05 引用）+
  `exp07_manifest_joint.json`（端点/窗口/分支色标记录）。
  完成条件：D10a/b 真机三分支图层 + manifest 落盘，`90` 点/单位齐全
  （invalid 点除外，另行标记）。
- [ ] T005 编写 `scripts/plot_D10.py` 并出图：D10a/b 合一张 `1×2` 图
  （`δ=−2` / `0.85` 各一面板，`(a)(b)` 标签置于各子图下方，
  `s` 轴标签每面板各一居中正下方）：
  每面板 S06 模拟机 `p=2` 获胜分支 `Q` 灰色单线 +
  真机 `p=2` 三分支窗口散点（初态本色：triv 红 / topo 蓝 / Néel 黑，
  共用端点归一化后逐点平均 + 单位间标准误，不二次归一化）；
  只读 T004 产品与 S06 出图，不生产数据；
  `figure_style.py` 风格，mathtext，矢量 PDF + 300dpi PNG 落 `figs/exp07/`。
  完成条件：点/误差棒与 npz 一致，端点/窗口与 manifest 一致，归一化可复算。

## Validation

- [x] T006 本地单元测试（`test/test_exp07_local.py`，pytest，全绿，
  零真机调用，建议 T002 前先行）：分支参数读取（与 S06 `theta_leg[p=2]`
  一致）；初态振幅对照；单键酉对照；
  **Aer 黄金交叉**（抽样 `(δ,s,a)` vs S06 `leg_E` 的 `p=2` 子集，
  容限 plan 定，不通过不得进 T003）；
  缓解恒等式；D10a/b 归一化；manifest 必填字段。
- [ ] T007 生产断言 [VAL-001..VAL-008]（`scripts/verify_exp07.py`，
  对正式输出全量执行，逐条映射 spec Contract F）：每单位 `90` 点齐全；
  三件套存档完整性；任务对账；窗口/端点/`r_a` 复算；转译验路；
  manifest schema；诊断分布记录；invalid-run 门。


## 维护：欧氏概率投影（2026-11-03）

- [x] T008 assembler 复用 Exp06 的归一化反演与欧氏单纯形投影、逻辑比特升序标定；manifest 必填方法记录；本轮 Exp06/Exp07 本地回归共 25 项通过。正式 D10 的组装与验收仍归 T004/T007，待原计划 counts 收齐。


## 维护：2026-11-03 退役旧参数批次并重提

上文 T003 的 warm start 批次已停发，不计为现行正式采集完成；历史记录保留。新一轮按现行 `PRE-002` 与下列维护任务执行。

- [x] T009 固定旧批次任务清单，停止本地提交和自动重提，核对/取消可撤销远端任务；旧数据移至项目外回收站，仅保留处置记录。完成证据：`data/validation/warm-retirement-20261103-_l8l6tpr/cancel-progress.json` 共 $35445$ 项（已终结 $2342$ ／已取消 $33103$ ）；`remaining-queue-summary.json` 旧批次待处理 $0$ ；`trash-manifest.json` 记录旧数据已移至项目外，`run-info.json` 保留处置记录。
- [x] T010 增加优化协议及批次来源绑定，拒绝旧协议和不同参数/QASM 状态续跑；来源、参数读取和防混批验证通过。完成证据：`scripts/optimization_source.py` 固定 `independent-global-lbfgs-v1` 并拒绝旧协议；`data/exp04/exp04_manifest.json` 与 `data/exp07/joint/groups.json` 均为该协议；`exp07-circuit-verification.json` 共 $90$ 电路，最大态保真度偏差 $4.44\times 10^{-15}$ 。
- [x] T011 使用新 S06 对全部 $90$ 个测点进行态矢量能量交叉核验，生成独立新账单并记录本轮重提授权。完成证据：同上 $90$ 点交叉核验通过；`data/exp07/joint/rounds/r001/bill.json` 为独立新账单，共 $46000$ 任务（`VQE` $45000$ ＋标定 $1000$ ），`confirmed=true` 并注明仅限本轮替换批次。
- [ ] T012 独立新会话提交 $46000$ 个新任务，增量回收；完成后按 T004/T005/T007 组装、出图与执行全部正式验证。
