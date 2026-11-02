# Tasks: exp02 拓扑物理量

**Feature:** exp02

任务必须来源于 `spec.md` 和 `plan.md`。
不得在 tasks 阶段引入新的实验定义。

## Implementation

- [x] T001 实现 `src/Exp02/Correlators.jl`：`zz_correlators(psi)`（`8×8` 实对称，
  对角构造性为 `1`）与 `structure_factor(C, q)` 纯内核；基矢约定运行时断言
  S01 manifest 一致。
  完成条件：模块可加载，直积态关联矩阵正确（由 T006 断言锁定）。
- [x] T002 实现 `src/Exp02/StringOrder.jl`：`string_order(psi)`（`d=3` 对角加权求和），
  纯内核。
  完成条件：S02 三点可出值且有限。
- [x] T003 实现 `src/Exp02/Panels.jl`：逐点组装 `(Sπ, Ostr, Q, Zt)`；
  `Q` 代数组合；`~Z_R` 使用本模块 `ZTilde.jl` 内核（D01 退役后由 exp01 迁入）。
  完成条件：单点四元组完整且 `Q` 恒等式在构造层成立。
- [x] T004 实现 `src/Exp02/Store.jl`：D04a–D04d 按 `δ` 行分块 `.npz` + 完成表续算；
  D03 三曲线独立文件；组装 `exp02_D03.npz`、`exp02_D04.npz` + manifest。
  完成条件：中断续算一致（删块重跑组装不变）。
- [x] T005 编写 `scripts/run_exp02.jl`（S01 输入门控 → 模块 API → 分块落盘 → 组装）
  并执行全网格生产 + D03 三曲线计算。
  完成条件：D03/D04a–D04d 文件 + manifest 落盘，形状与坐标与 S01 一致。
- [x] T006 出图（`scripts/plot_D03D04.py`）：D03 三线同图 + D04 四联 `2×2` 合图
  `exp02_D04.pdf/png`（`(a)–(d)` 按 outline 顺序，mathtext 标签，`figure_style.py` 风格，
  矢量 PDF + 300dpi PNG 落 `figs/exp02/`；D03 横坐标刻度为 `0, π/2, π, 3π/2, 2π`，
  保留 `q=π` 半截竖线（仅从峰值圆点向下）与峰值圆点标记，无额外 `π` 轴外文本）。
  完成条件：坐标系自检通过，三线标签与代表点对应，四联顺序正确，
  D03 刻度与标记检查通过，合图四子图等大且有效字号 `≥8pt`，附 skill 风格检查报告块。

## Validation

- [x] T007 单元测试（`test/runtests.jl` 追加，全绿）：关联矩阵解析小例；
  string 小例；`q=π` 交错和恒等式；S01 输入门控拒绝路径。
- [x] T008 生产断言 [VAL-001..VAL-007]（对正式输出全量执行）：`Ŝ(q) ≥ −1e-12`；
  D03↔D04a `Ŝ(π)` bit 一致；`Q` 恒等式残差 `< 1e-12`；
  `|~Z_R| ≤ 1`；无缺失、无 NaN；简并标记逐点一致。

## Rework（δ∈[-3,3] 网格 + Q 归一化 + D05 迁入）

- [x] T009 网格迁移：`δ` 改为 `[-3,3]` 上 121 点均匀（步长 0.05，依赖 shared-01 按同范围重算）；
  重跑全网格生产与组装，坐标与 S01 逐点一致。
  完成条件：D04a–D04d 形状 `99×121`、`δ` 覆盖 `[-3,3]`，manifest 记录新网格。
- [x] T010 `Panels.jl` 的 `Q` 改为 `4/3 − 2Ô_str − (4/3)Ŝ(π)`（与旧式数值等价），
  同步 `INV-003` 断言。
  完成条件：恒等式残差 `< 1e-12`。
- [x] T011 新增 `scripts/plot_D05.py`：在 D04d 上标注三相起点与同相示范终点，
  输出 `figs/exp02/exp02_D05.pdf` + `.png`。
  完成条件：坐标落在网格内、三起点异相、不遮挡相界。
- [x] T012 生产断言更新为 `VAL-001..VAL-008` 新口径（含网格/S01 一致、D05 校验）；
  `VAL-006` 只记诊断、不设阈值。
- [x] T013 归一化落盘（按新版 paper-outline）：D03 曲线存 `Ŝ(q)=S(q)/L`，
  D04a/D04b 存 `Ŝ(π)`、`Ô_str=−O_str`，键名 `s_hat_pi` / `o_hat_str`；
  出图直接用落盘值，不做二次缩放。
  完成条件：D03↔D04a bit 一致、`Q` 恒等式残差 `< 1e-12`，图上轴/色标为归一化量。

## Rework（D05 拿掉）

- [x] T014 移除 D05：spec 删 D05 全部规范条目；plan 同步；删除
  `scripts/plot_D05.py` 与 `figs/exp02/exp02_D05.*`；
  `verify_exp02.jl` 去 VAL-008 段后重跑通过；`runtests.jl` 全绿。
  完成条件：`VERIFY-EXP02-OK`；库内无 D05 规范残留。
