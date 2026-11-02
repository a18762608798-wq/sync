# Tasks: exp04 模拟机 VQE

**Feature:** exp04

任务必须来源于 `spec.md` 和 `plan.md`。
不得在 tasks 阶段引入新的实验定义。

## Implementation

- [x] T001 实现 `src/Exp04/InitStates.jl`：`psi_triv/psitopo/psiafm`
  （`256` 维，基矢约定运行时断言 S01 同字符串）；`src/Exp04.jl` 父模块。
  完成条件：模块可加载，三态范数/`Z_tot`/`X̄`/`R` 构造性正确（由 T007 锁定）。
- [x] T002 实现 `src/Exp04/Ansatz.jl`：`L=8` 轨道/子层元数据（奇 `2` 轨、
  偶 `2` 轨，子层顺序按初态 `F/S`）与 `apply_circuit!`（单键 `4×4` 比特对作用）；
  `nparams`（`δ=0` 减半结构式）、零参数恒等。
  完成条件：单键酉与 kron 参考一致，零参数即初态（由 T007 锁定）。
- [x] T003 实现 `src/Exp04/VQELoop.jl`：`energy`（`H` 期望，`H` 只读自
  `Shared01.Hamiltonian`）、`pshift_gradient`（参数移位精确梯度）、
  `run_leg`（`64+1` 采样 + 前 `4` L-BFGS + 收敛旗/种子记录）、
  `run_point`（三路 + 同路链式 warm `p=2,3` + 取最小路）。
  完成条件：smoke 点（`δ=0/0.85 × s=0.01/0.5/0.99`）可出三路全收敛结果（由 T007 锁定）。
- [x] T004 实现 `src/Exp04/Store.jl`：按 `δ` 分块 `.npz` + 完成表续算；
  组装 `exp04_S06.npz`（三路全量 + 最小路 + 观测量）与 `exp04_S03.npz`
  （`594` 组同值引用）+ `exp04_manifest.json`（schema `exp04/v1`）。
  完成条件：中断续算一致（删块重跑组装不变）。
- [x] T005 编写 `scripts/run_exp04.jl`（模块 API → 分块落盘 → 组装；
  顺序 `δ=0 → 0.85`）并执行全点生产（`198` 点 × 三路 × `p` 链）。
  完成条件：S06/S03 文件 + manifest 落盘，形状与网格定义一致。
- [x] T006 出图与示意：`scripts/plot_S06.py`（4 诊断图 `(δ × {S(π), string})`，
  每图 `p=1,2,3` 三线，mathtext 标签，`figure_style.py` 风格，
  矢量 PDF + 300dpi PNG 落 `figs/exp04/`）与 `scripts/plot_D06.py`
  （拟设示意图，同目录）。
  完成条件：坐标系自检通过，四图顺序正确，D06a–c 人工保真核对通过，
  附 skill 风格检查报告块。

## Validation

- [x] T007 单元测试（`test/runtests.jl` 追加，全绿）：初态三性；
  单键酉 kron 一致；零参数恒等；参数移位梯度 vs 有限差分；
  `δ=0` 参数计数；warm 链 smoke 单调；非法输入拒绝路径。
- [x] T008 生产断言 [VAL-001..VAL-008]（`scripts/verify_exp04.jl`，对正式输出全量执行）：
  `E* ≤ E_init + 1e-8`；守恒量三项容限内；收敛旗全真或棘轮接受
  （`stagnant` 仅 `p>1`，且 `dE_tail` 与棘轮不等式由存档值重算锁定）；
  `a*` 为最小路；
  `E* ≥ E0 − 1e-8`（暴力精确交叉）；
  S03 形状 `594` 组且与 S06 同值；无缺失、无 NaN。

## Follow-up (重编号：D06→D06a–c 三分相 + S06；诊断图保留)

- [x] T009 扩展 `scripts/plot_D06.py` 出 D06a–c 三分相示意图（每相初态 +
  所需拟设电路；triv/afm 首动偶子层、topo 首动奇子层；只画 ansatz.md
  已定义元素）并实跑出图（`figs/exp04/exp04_D06{a,b,c}.pdf/.png`）。
  完成条件：脚本零数据输入，三图可出图，`figure_style.py` 风格。
- [x] T010 人工保真核对 D06a–c（用户目检：初态/轨道配对/子层顺序/`p` 堆叠
  与 ansatz.md、psi0.md 一致，无虚构门）。
  完成条件：用户确认通过。

## Rework (2026-10-22：δ=−2 生产线 + D08a/b + D09a/b)

- [x] T011 代码适配（不跑生产）：`DELTAS` 改 `(−2.0, 0.85)`，线 ID/键前缀
  `d0`→`dm2`（`d085` 不变，旧 `d085` chunk 继续有效）；`run_exp04.jl` 生产顺序
  `δ=−2 → 0.85`；`verify_exp04.jl` 与 `plot_S06.py` 的文件名/断言同步；
  新增 `scripts/plot_D09.py`（读 S06 `p=2` + S01 两行 `E0`，背景按
  `argmin_a C_a` 的相着色，trivial 红/AFM 白/topo 蓝，各相区标最优初态）；
  测试补 D09 相标签与 S01 对齐用例。
  完成条件：`runtests.jl` 全绿；`plot_D09.py` 能在旧数据上干跑自检。
- [x] T012 生产：归档旧 `δ=0` 线，跑 `δ=−2` 全网格（99 点 × 3 路 × `p=1,2,3`）
  → 与既有 `d085` 线组装 S06/S03 → `verify_exp04.jl` 全量通过。
  完成条件：`VERIFY-EXP04-OK`；manifest `deltas=[-2.0,0.85]`。
- [x] T013 出图：重出 S06 诊断图（`dm2`/`d085`）与 D09a/b，目检相区背景、
  最优初态标记与精确 `E0` 曲线。
  完成条件：`figs/exp04/exp04_D09a.pdf/.png`、`exp04_D09b.pdf/.png` 存在且自检通过。
- [x] T014 D09 色带改物理相区：新增 `src/Exp04/D09.jl`（读 S01 精确基态，
  算 `Ŝ(π)`、`Z̃_R`，`AFM ⟺ Ŝ(π)>0.5`，其余按 `Z̃_R` 正负分 trivial/topo，
  连同 `E0` 写 `exp04_D09.npz`）；`run_exp04.jl` 组装后调用；
  `plot_D09.py` 改读 D09 npz 并按相区着色、每区标最优初态；
  `verify_exp04.jl` 增加相位重算与 `E0` 对齐断言。
  完成条件：`VERIFY-EXP04-OK`；D09a 为 triv→topo 两段、D09b 为
  triv→AFM→topo 三段，无碎带。
- [x] T015 D09 切 `p*=1` + S06 诊断图改画 Q：`plot_D09.py` 取 `p=1` 子集
  （`P_STAR=1`，数据不重算）；`plot_S06.py` 重写为 2 张 Q 诊断图
  （每线一张，`p=1,2,3` 同图；`Q` 由存档 `S(π)`/string 组合）；
  `verify_exp04.jl` 同步；删孤儿 `figs/exp04/exp04_S06_d0_*`；
  重出 S06 诊断图与 D09a/b 并目检。
  完成条件：`VERIFY-EXP04-OK`；D09a/b 每区最优初态与所在相一致。
- [x] T016 D09 判相改零点+拐点：`D09.jl` 整线分类（`Ŝ` 最陡升/降定 AFM 带，
  峰不显著则无；其余按 `Z̃_R` 过零点插值分 trivial/topo），
  `verify_exp04.jl` 同函数重算锁定；重跑 `run_exp04.jl` 重出 D09 npz，
  重出 D09a/b 并目检。
  完成条件：`VERIFY-EXP04-OK`；D09a 为 triv→topo 两段（界≈0.64），
  D09b 为 triv→AFM→topo 三段；无阈值残留。
- [x] T018 诊断性全局 p=2/p=3 全网格存档（不进生产口径）：
  新增 `scripts/run_exp04_global.jl`（每路 `p=1,2,3` 全部全局采样，
  与 S06 同键名落 `data/exp04_global/` + 独立 manifest），后台跑完 198 点，
  抽查 `θ*`/能量自洽（与 S06 `p=1` 逐点一致）后归档。
  完成条件：`data/exp04_global/exp04global_S06.npz` + manifest 存在；
  生产 `data/exp04/` 未动。
- [x] T017 S06 诊断图加精确 Q：`D09.jl` 一并存档 `ostr_exact`；
  `plot_S06.py` 改精确 `Q` 蓝实线 + `p=1,2,3` 统一黑虚线；
  `verify_exp04.jl` 同步；重出 S06 Q 图并目检。
  完成条件：`VERIFY-EXP04-OK`；精确 Q 与 `p` 曲线同图、无遮盖。
- [x] T019 D09 分段改回 `p=1` 获胜初态：`D09.jl` 改读 S06 `a*` 列作分段
  （去 `classify_line` 零点+拐点路径，`E0`/精确叠加量仍取 S01）；
  `run_exp04.jl` 组装调用同步；`verify_exp04.jl` 改分段重算锁定；
  重跑 `run_exp04.jl` 重出 D09 npz，重出 D09a/b 并目检。
  完成条件：`VERIFY-EXP04-OK`；D09a 为 triv→topo 两段（界 `s=0.59→0.60`），
  D09b 为 triv→AFM→topo 三段（界 `0.42→0.43`、`0.79→0.80`）。

## Rework（2026-10-29：D06/D09 合图 + 标签下方）

- [x] T020 D06 合图：`plot_D06.py` 改出 `1×3` 单图 `exp04_D06.pdf/png`
  （三相面板复用同源绘制函数，三子图等大，`(a)(b)(c)` 标签置于各子图下方）；
  删除 `exp04_D06{a,b,c}.pdf/png`；论文 `06-ansatz(.zh).tex` 改单引合图；
  D06 人工保真核对按 `VAL-006` 重做。
  完成条件：合图三面板与旧分图逐面板一致；`VERIFY-EXP04-OK` 不受影响（零数据输入）。
- [x] T021 D09 合图：`plot_D09.py` 改出 `1×2` 单图 `exp04_D09.pdf/png`
  （两线面板同源数据，`(a)(b)` 标签置于各子图下方）；
  删除 `exp04_D09{a,b}.pdf/png`；论文 `06-ansatz(.zh).tex` 改单引合图。
  完成条件：合图两面板与旧分图逐点一致（背景分区/`E0`/最优点）；`VERIFY-EXP04-OK`。
