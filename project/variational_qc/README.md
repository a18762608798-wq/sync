# variational_qc

变分量子计算实验项目：SSH-XXZ 自旋链的基态、序参量与 VQE 研究。

## 内容

- `src/`：数值核心（Julia）
  - `Shared01/`：哈密顿量、基态求解、数据读写
  - `Exp02/`：ZTilde 序参量、弦序、关联函数与面板数据
  - `Exp03/`：能隙求解、截面基组与交叉拟合
  - `Exp04/`：变分拟设、初态与 VQE 循环
- `scripts/`：`run_*.jl`（实验运行）、`verify_*.jl`（结果校验）、
  硬件任务提交（`exp05_*`、`exp06_*`）与论文绘图（`plot_*.py`）
- `specs/`：exp02–exp06、shared-01 的 spec / plan / tasks
- `docs/`：[文档导航与固定路径约定](docs/README.md)，含 `planning/`、`status/`、`theory/` 与 `paper/`
- `assets/fonts/`：Noto 中文论文字体与 Times New Roman 绘图字体，分别保留授权说明
- `figs/`：论文插图（矢量 PDF 与 PNG 预览）
- `test/`：`runtests.jl` 及相关测试
- `.agents/skills/`：Codex 的 Spec Kit skills（`speckit-*`）
- [论文看板](docs/status/paper.html) / [实验看板](docs/status/experiments.html)：论文与实验进度总览
  （浏览器在线查看：[论文看板](https://a18762608798-wq.github.io/variational_qc/docs/status/paper.html) /
  [实验看板](https://a18762608798-wq.github.io/variational_qc/docs/status/experiments.html)）

## 追踪规则

- 忽略：`data/`、`*.npz`、`*.pdf`、各类缓存（`__pycache__`、`.pytest_cache` 等）、本地环境（`.CondaPkg/`、`node_modules/`）
- 保留：`*.png`（论文插图）

## 环境

- Julia：项目使用 Julia 1.12.7；`Project.toml` / `Manifest.toml` 管理 Julia 依赖，`CondaPkg.toml` 管理项目本地 Python 环境。

```bash
julia --project=. --startup-file=no -e 'using Pkg; Pkg.instantiate(); using CondaPkg; CondaPkg.resolve()'
```

- Python 绘图：`scripts/figure_style.py`（Okabe-Ito / Tol 配色，colorblind-safe）；自动加载 `assets/fonts/times-new-roman/` 中的四种字形，无需系统安装；数学字体用 STIX。字体与路径规则见 [docs/README.md](docs/README.md)。

## Spec Kit / Codex

本项目的默认集成为 `codex`，skills 位于 `.agents/skills/`（`speckit-*`）。
新项目初始化使用 `specify init --here --integration codex --script sh`；已有项目切换使用
`specify integration switch codex --script sh`，不要强制重建实验 spec。

## 非真机验证

```bash
OPENBLAS_NUM_THREADS=1 julia --project=. --startup-file=no -t 8 test/runtests.jl
OPENBLAS_NUM_THREADS=1 julia --project=. --startup-file=no -t 8 scripts/verify_production.jl
julia --project=. --startup-file=no scripts/verify_exp02.jl
julia --project=. --startup-file=no scripts/verify_exp03.jl
julia --project=. --startup-file=no scripts/verify_exp04.jl
OPENBLAS_NUM_THREADS=1 julia --project=. --startup-file=no scripts/smoke_simulation.jl
.CondaPkg/.pixi/envs/default/bin/python -m unittest discover -s test -p test_figure_fonts.py
```

`smoke_simulation.jl` 在隔离的 `data/validation/` 下重新计算代表点、五种尺寸的能隙和两条 VQE 线的抽样点；不覆盖正式数据，也不提交真机任务。完整生产网格重算不包含在 smoke 测试内。
历史产物校验与新计算测试分别报告，不能把新计算通过视为旧数据自动通过。
