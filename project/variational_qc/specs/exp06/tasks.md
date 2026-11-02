# Tasks: exp06 真机测量与比较

**Feature:** exp06

任务必须来源于 `spec.md` 和 `plan.md`。
不得在 tasks 阶段引入新的实验定义。

> 前置阻塞（analyze H1/M1）：
> - H1 已解决（spec `VAL-008` 已加转译验路断言条目，plan §4 已加对应检查）——
>   T003/T007 转译门可按新条目执行。
> - M1 已解决（取证完成，证据见 plan §3 M1 取证结论；旧称统一为
>   `correct=False`）——T000 转为提交前复核：确认提交代码未改动
>   `correct` 默认（`False`）并留存参数。

## Implementation

- [x] T000 提交前复核 `correct` 默认（M1 取证已关闭）：确认提交代码
  未改动 `QuarkOptions.correct` 默认（`False`），提交参数逐批留存备查。
  完成条件：复核通过；若被改动则停，返工 plan，不进 T003。
- [x] T001 实现 `scripts/exp06_circuits.py`：`build_init(a*)`（单态/GHZ，
  与 psi0 解析式逐振幅对照）、`build_ansatz(theta,a*,p,delta)`
  （轨道配对/`δ=0` 减半/子层顺序/`RXX/RYY/RZZ` 单键，对应表写进 docstring）、
  `build_estimator_circuit`（+全 `Z` 测量）、`build_calib_circuits`
  （全 `0` / 全 `X`）。
  完成条件：模块可加载，a*=1/2/3 初态振幅正确（由 T006 锁定）。
- [x] T002 编写 `scripts/exp06_preview.py` 并执行离线预览：S03 读入 →
  稀疏过滤（`s_idx∈{1,4,…,97}`，198 组；S03 缺组标 invalid）→ 66 批划分
  （3 组/批，批次 id 固定）→ 账单（VQE 990 + 标定 132 = 1122 任务，
  快照/S03 引用，`confirmed=false`）。
  完成条件：账单已打印、经人工确认（确认记录留存），零机时，
  未确认前不得进入 T003。
- [x] T003 编写 `scripts/exp06_submit.py`（转译 opt3/显式 coupling_map；
  对账补跑沿用 exp05 模式）并执行真机提交（人工确认 + T000 通过后）：
  逐批（VQE ×5 独立 tid + 标定 2，`correct=False` 参数留存），
  增量落盘 `data/exp06/batches/<bid>/`，中断续跑只补缺失。
  完成条件：66 批全收回（或明确标记），无静默丢弃，无已收回重提。
- [x] T004 编写 `scripts/exp06_assemble.py` 并组装产品（p* 规则变更后需重组装）：S05 矩阵 →
  Kronecker-`M⁻¹` 缓解 + 非负约束 → `S(π)`/string（公式只读复刻 Exp02）→
  写 `data/exp06/exp06_D08.npz`（全量 198 组缓解后均值/全并解析 SE/每重复三件套/
  S03 与 S05 引用 + 每面板 `p*` 选取（规则见 spec `POST-002`：每个
  `(δ,观测量,p)` 数据块独立归一化后与固定模拟 `p=3` 比较，保留最近 70% 点）+
  S06 快照引用与归一化区间）+
  `exp06_manifest.json`（schema `exp06/v1`，含 `p*` 与归一化区间记录）。
  完成条件：D08a–D08d 真机图层 + manifest 落盘，198 组齐全（invalid 组除外，
  另行标记）。
- [x] T005 编写 `scripts/plot_D08.py` 并出图（p* 规则变更后需重出）：D08a–D08d 四张独立图
  （`2δ × {S(π), string}`）：每面板模拟机 `p=1,2,3` 三线（读 S06）+
  真机 `p*` 与模拟 `p=3` 只绘制最近 70% 点及误差棒（只读 T004 的 D08a–D08d 与 S06 出图，
  不生产数据；归一化区间与 manifest 一致）；
  `figure_style.py` 风格，mathtext，矢量 PDF + 300dpi PNG 落 `figs/exp06/`。
  完成条件：组/误差棒与 npz 一致，`p*` 与 manifest 一致，归一化可复算。

## Validation

- [x] T006 本地单元测试（`test/test_exp06_local.py`，pytest，全绿，
  零真机调用，建议 T002 前先行）：初态振幅对照；单键酉对照；
  **Aer 黄金交叉**（抽样点 vs S06，`1e-8`，不通过不得进 T003）；
  缓解恒等式；D08a–D08d 归一化；manifest 必填字段。
- [x] T007 生产断言 [VAL-001..VAL-008]（归一化语义变更后需重跑；`scripts/verify_exp06.py`，对正式输出全量执行，
  逐条映射 spec Contract F）：每组 5 重复齐全；三件套存档完整性（逐组查 counts +
  缓解前 + 缓解后三样落盘，缺一报错）；`θ` 与 S03 逐元一致
  （`NaN`-pad 区除外）；S05 批次 id 同批；`correct=False` 留存可查；
  转译验路断言（边集落入允许集，见 spec `VAL-008`）；对账一致；
  invalid 任一触发非零退出指明组；诊断输出
  （缓解前后差/离散度标记/D08a–D08d 目检提示，只记录）。
  完成条件：全量通过。

## Follow-up (exp05 重跑后：S04 刷新)

- [x] T008 新 S04 落盘后刷新本 feature 的 S04 引用（plan §3 映射表、
  `exp06_preview.py` 的 `SUBCHAIN_TOP1` 与映射表打印、Q3 问答取值）并重跑
  T002 预览出新账单（旧 `bill.json`/`batches.json` 作废，不沿用 run1 值）。
  完成条件：账单快照与新 S04 一致，经人工确认后才可进 T003。

## Implementation（v2 新协议：单位累计 + 连续窗口，2026-10-24 起）

旧协议任务（T000–T008）全部归档不动；旧协议数据（`δ=0` 线）整体归档，
不与新协议混存。以下任务按 spec `PRE-007` / `POST-002` 执行：

- [ ] T009 试水轮：`50–100` 单位（机器不限，用空闲真机；`task_id` 等过程
  数据全留存，落 `data/exp06_pilot/`）→ 跑通提交→收回→缓解→`Q` 组装→
  窗口搜索→判据全链路；旧数据组 `Q` 做可达性标定参考
 （floor `d≈0.33` / `r≈0.16`，结论：堆单位压不住 bias，达标靠新机质量）。
  完成条件：链路跑通，可达性有结论；试水不计 `N`、不进窗口。
- [ ] T010 新 preview + 首轮账单：`δ=−2` 线 `15` 点 × 只 `p=2` →
  常规轮 `1000` 单位账单（`17000` 任务，`task_id` 预留），人工确认；
  旧 `bill.json` / `batches.json` 随旧数据归档。
  完成条件：账单经人工确认，零机时，未确认前不得进 T011。
- [ ] T011 逐轮提交 + 对账（`δ=−2` 先行）：转译 opt3 / 显式 coupling_map /
  `correct=False` 参数留存；每单位 `15` VQE + `2` 标定同批，增量落盘
  `data/exp06/batches/<unit_id>/`，中断续跑只补缺失。
  完成条件：本轮全收回（或明确标记），`task_id` 清单齐全，无静默丢弃。
- [ ] T012 每轮结算（`δ=−2`）：assemble（缓解→`Q`→全局最优窗口搜索 +
  判据，起步 `d<0.30 & r>0.4`；**每满 100 单位只读中检一次**，
  dm2 在 1000 结算按 ladder 升级）→
  `verify_exp06.py` → `plot_D08.py` 出 D08a →
  目检；达标停线，否则下一轮；到 `5000` 上限取全局最优窗口 + 未达标声明。
  完成条件：`VERIFY-EXP06-OK`；窗口/判据/manifest（`exp06/v2`）可复算。
- [ ] T013 `δ=0.85` 线重复 T010–T012，出 D08b；判据用加严版
  （`d<0.08`、`r>0.9`，窗口固定 `20`，只搜起点，无 ladder）。
  完成条件：同 T012；两线各自独立停线。
- [ ] T014 收尾：旧协议数据归档（`data/exp06_protoV1_*`）+ manifest `v2` 冻结；
  披露字段核对（累计 `N`、窗口起止 / 长度、判据与搜索规则、试水声明）。
  完成条件：披露齐全，可供论文方法引用。

## Validation（v2）

- [ ] T015 `test_exp06_local.py` 更新并全绿（零真机调用）：Q 组装对照、
  窗口搜索复算（含并列规则）、`[-1,1]` 归一化、manifest `v2` 必填字段；
  Aer 黄金交叉抽样改为 `(a*,p=2,δ∈{−2,0.85})`，`1e-8` 不通过不得进 T011。
- [ ] T016 生产断言 [VAL-001..VAL-008]（`scripts/verify_exp06.py` v2，
  对正式输出全量执行）：单位齐全、三件套完整、`θ` 与 S03 `p=2` 逐元一致、
  S05 同单位、`correct=False` 留存、转译验路、对账（含试水 `task_id`）、
  窗口复算 + 披露齐全；invalid 任一触发非零退出指明单位 / 窗口。
  完成条件：全量通过。

## Implementation（v3 联测：两线同窗口 30 点，2026-10-26 起）

旧协议任务（T000–T016）全部归档不动；v2 分线数据（dm2 正式 593 +
d085 在途）整体归档为 `data/exp06_protoV2_*/`，不进 v3 窗口搜索。
以下任务按 spec `PRE-007` / `POST-002`（v3）执行：

- [x] T017 取消旧在途任务：d085 在途约 `17000` 待收回任务服务端
  mass-cancel；dm2 确认服务端无 pending（早前已取消 6915 未收回）。
  完成条件：两线服务端 pending 清零（本地记录备查）；之后才许 T020。
- [x] T018 旧数据归档 + 新目录就位：`data/exp06/dm2/`、`data/exp06/d085/`
  移入 `data/exp06_protoV2_20261026/`（原样保留 groups/units/manifest）；
  新建 `data/exp06/joint/`（units + groups.json + bill.json + manifest）。
  完成条件：旧目录只剩归档引用，新目录结构与 plan §2 一致。
- [x] T019 新 preview + 账单：`30` 点联合单位（每 `s` 先 `δ=0.85` 后 `δ=−2`）
  → 单轮 `500` 单位账单（`16000` 任务 ≈1600 万 shots），人工确认；
  旧 `bill.json` 随 v2 数据归档作废。
  完成条件：账单经人工确认，零机时，未确认前不得进 T020。
- [x] T020 单轮提交 + 收回（Baihua，直接正式无试水）：
  先取消 `p=2` 在途任务（服务端 mass-cancel + 本地确认 pending 清零）；
  `data/exp06/joint/` 已清空（`p=2` 数据归档 `data/exp06_protoV3p2*/`），从 unit1 起重提 `p=1`；转译 opt3 /
  显式 coupling_map / `correct=False` 参数留存；每单位 `30` VQE + `2` 标定
  同批，增量落盘 `data/exp06/joint/units/<unit_id>/`，中断续跑只补缺失。
  2026-10-30 串行重提：首轮 `SUBMIT_CONCURRENCY=20` 并发打散时间相邻性，
  已 `mass-cancel` 全部旧 tid 并清空本地 `tids`/`counts`（`tids_history` 留存），
  改 `=1` 按 `(uid, g序)` 逐个直发后重提；轮询并发不限；
  2026-11-01 收齐 `16000/16000`（`500` 单位全满）；平台侧另有 `139` 个键
  因转译/空结果被自动重提（history 3–4 条），重提时刻不保证与同单位相邻。
  完成条件：`500` 单位全收回（或明确标记），`task_id` 清单齐全，
  无静默丢弃，无已收回重提。
- [ ] T021 收齐后组装：`500` 收齐 → 扫描偶数长度子段，对每个候选窗口
  用其 pooled `30` 点均值的 top-1 最大值做端点记入 manifest（Q14）→ 同公式组 `Q`（真机除端点 / 模拟固定 hat，
  不二次归一化）→ 最优偶数长度窗口搜索（`r` 最大，并列 `d_raw` 最小，
  再并列更长，再并列更早）+ `d_raw`/`r` 报告 → 写
  `data/exp06/joint/exp06_D08_joint.npz` + manifest `v3`。
  2026-11-01 选窗参照层改 `p=1`（原 `p=2`）：`counts` 不变，重跑
  T021/T025/T022。
  完成条件：`VERIFY-EXP06-OK`（v3 口径）；端点先冻结再搜索可复算。
- [ ] T022 出图 D08a/b：S06 `p=1,2`（固定 hat）+ 真机窗口散点
  （共用端点归一化后逐点平均 + 单位间标准误）；散点按 D09 分段着色。
  完成条件：点位/误差棒与 npz 一致，端点与窗口记录正确。
- [ ] T023 收尾：manifest `v3` 冻结；披露字段核对（`N=500`、窗口起止 /
  长度、共用端点与冻结方式、偶数长度按 `r` 选优规则、无阈值门 report-only）。
  完成条件：披露齐全，可供论文方法引用。
- [x] T026 `p*=2→p*=1` 切换归档：`data/exp06/joint/`（`p=2`，`N=355`）
  移入 `data/exp06_protoV3p220261030/`（原样保留 units/manifest），
  `joint/` 清空供 `p=1` 重跑（T020）。
  完成条件：旧目录只剩归档引用新目录就位。
- [x] T027 D03 三代表点真机测量（`PRE-008`）：S02 三点各 `1` estimator
 （D09 `p=1` 获胜分支初态 + S03 同点 `p=1` θ*）+ `2` S05 标定同批，
  `Z` 基 `1024` shots 三点独立测量；落盘 `data/exp06/d03hw/`（counts +
  缓解后观测量 + multinomial SE + S03/θ* 引用 + S05 引用）。
  完成条件：三点齐全、`θ` 与 S03 同点 `p=1` 一致、S05 同点。
- [x] T028 D03 真机组装 + 出图验证（`POST-008`）：`⟨ZiZj⟩` Fourier 组
  `S(q)` 除以 `L` + multinomial SE 复算 → 扩展 `plot_D03D04.py` 出
  真机 overlay（同 `q` 网格同归一化三条 + 三点散点）→ 目检 AFM 标签。
  完成条件：npz 与模拟机同网格可比、图点位一致、论文 D03 图更新。

## Validation（v3）

- [x] T024 `test_exp06_local.py` 更新并全绿（零真机调用）：hat 组装对照、
  共用端点（top-1 最大值，窗口内）复算、偶数窗口搜索复算（含并列规则）、
  `d_raw`/`r` 复算、manifest `v3` 必填字段；
  Aer 黄金交叉抽样改用 `(a*,p=1,δ∈{−2,0.85})` 并重跑全绿，`1e-8` 不通过不得进 T020。
- [ ] T025 生产断言 [VAL-001..VAL-008]（`scripts/verify_exp06.py` v3，
  对正式输出全量执行）：每单位 `30` 点齐全、三件套完整、`θ` 与 S03 `p=1`
  逐元一致、S05 同单位、`correct=False` 留存、转译验路、对账、
  端点冻结先于搜索 + 窗口复算 + 披露齐全；
  invalid 任一触发非零退出指明单位 / 窗口。
  完成条件：全量通过。
