# Tasks: exp07 p=2 分支分辨真机测量与比较

**Feature:** exp07

任务必须来源于 `spec.md` 和 `plan.md`。
不得在 tasks 阶段引入新的实验定义。

> 状态：2026-11-03 T000/T001/T006 已完成（T006 5 项全绿，aer 0.18.2；缓解/Q/窗口/manifest 断言随 T004 扩充）；T002 账单已由用户直接授权确认（2026-11-03，免等待门）；随即进 T003。
>
> T000 记录：qmeas 源码默认 `correct=False`（config.py:56，quark_client:115 透传），T003 须沿用显式 `correct=False` + assert。
> T001 记录：复用 exp06 构造器 + S06 `theta_leg[si,a,p=2]` 分支层，90 点零 invalid。
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
  Kronecker-`M⁻¹` 缓解 + 非负约束 → `S(π)`/string（公式只读复刻 Exp02）→
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
