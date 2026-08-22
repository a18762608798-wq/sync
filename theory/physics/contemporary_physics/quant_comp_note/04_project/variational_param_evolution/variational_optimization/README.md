# 变分优化实验

"变分电路在量子计算机上做 SSH 基态相分类"这条实验线的两个编号子项目，编号反映实验推进顺序.

## 子项目

| 编号 | 目录 | 内容 |
| --- | --- | --- |
| 01 | [`variational_optimization_01/`](variational_optimization_01/) | 通用变分方案初验：三层优化框架 + 二次 Bézier 演化路径，验证模拟机与 quark 真机可行性 |
| 02 | [`variational_optimization_02/`](variational_optimization_02/) | 真机适配：环形电路 + 直线轨迹 + 噪声对抗，榨取 quark 真机最低能量 |

## 01 → 02 的关系

1. **01 提出问题**: 通用方案在模拟机上可行，但 quark 真机结果不可信——噪声使能量系统性偏高，电路越深偏差越大，连初态保真度都不理想.
2. **02 给出对策**: 接受"真机只能跑极浅电路"的现实，重设计参数化（直线轨迹、解耦 path 与 $\Delta t$、环形电路、参数去边界），并把目标从"验证方案"改为"真机最低能量".

## 公共依赖

* 两个子项目均依赖顶层 [`../src/`](../src/) 的核心代码（`var_optimization.py`、`create_op.py`、`get_cost_val.py` 等）；
* 02 的 `save_ideal_spectrum.jl` 依赖顶层 `../src/var_param_evolution.jl`（Julia）.

## 目录结构

```
variational_optimization/
├── README.md                            # 本文件
├── variational_optimization_01/ # 01: 初始方案初验
│   ├── save_qc_spectrum.py              # 三阶段扫描（DIRECT_L → SLSQP → SPSA）
│   ├── data/                            # aer_direct / aer / quark 三个 npz
│   └── pics/                            # 对比图
└── variational_optimization_02/ # 02: 真机适配
    ├── save_aer_spectrum.py             # 模拟机 DIRECT_L → SPSA
    ├── save_quark_spectrum.py           # 真机 SPSA（以模拟机结果热启动）
    ├── save_ideal_spectrum.jl           # 理想能谱（Julia）
    ├── plot_compare_var.py              # 绘图
    ├── src/                             # 本子项目代码（get_op/get_evolution_qc/objective/optimize_*）
    ├── hardware_test/                   # 真机可信度测试（Bell/初态/演化）
    ├── test/                            # 本子项目单元测试
    ├── data/                            # ideal/direct/aer/quark 结果
    └── pics/                            # 对比图
```
