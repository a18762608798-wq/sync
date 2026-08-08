# 变分参数演化

SSH 模型基态拓扑 $Z_R$ 分类的数值实验与变分量子计算方案。

## 模型

SSH 哈密顿量具有交替耦合结构：

$$
H = (1-s) \sum_{i\text{ odd}} (X_i X_{i+1} + \delta Z_i Z_{i+1}) + s \sum_{j\text{ even}} (X_j X_{j+1} + \delta Z_j Z_{j+1})
$$

**比特总数必须是4的倍数, 最少为8**，这限制了演化初态旋转和基态对称性。

反射算符 $Z_R$ 用于量化空间反演对称性：

$$
Z_R = \frac{tr(\rho S)}{\sqrt{(tr(\rho_1^2) + tr(\rho_2^2))/2}}, \quad S = \bigotimes_{i=1}^{N/2} \mathrm{SWAP}_{i,\,N-i+1}
$$

为打开基态简并，可加入对称性约束：

$$
H_c = H - \epsilon (U_x + 2U_z), \quad U_x = \bigotimes_i X_i, \; U_z = \bigotimes_i Z_i
$$

## 项目结构

```
├── phase_diagram/            # 相图计算与绘制（已完成）
├── symmetry_analysis/        # 对称性分析与约束哈密顿量验证（已完成）
├── concept/                  # 概念文档（贝塞尔曲线等）
├── variational_outline/      # 变分方案设计文档
├── variational_feasibility/  # 变分电路可行性实验
├── src/                      # 核心源代码
│   ├── create_op.py/.jl      # SSH H、约束 H、算符/哈密顿量构造
│   ├── get_evolution_path.py # 二次 Bézier 演化路径采样
│   ├── get_evolution_qc.py   # PauliEvolutionGate 电路构造
│   ├── get_initial_state.py  # 三种相分区初始态
│   ├── get_cost_vals.py      # 能量/settings 估计（AER 与 QUARK 真机）
│   ├── var_optimization.py   # 三层变分优化主入口
│   ├── get_expect_instance.jl # ZR 值计算
│   ├── get_spectrum.jl        # 能谱与本征态计算
│   └── var_param_evolution.jl # Julia 变分演化辅助
└── test/
    └── test_expect_instance.jl # ZR 值测试
```

## 进展

| 阶段 | 状态 |
| ------ | ------ |
| 1. 数值相图绘制与相边界计算 | ✅ 完成 |
| 2. 对称性分析：简并打开、初态选择、约束 H 验证 | ✅ 完成 |
| 3. 变分方案设计与文档 | ✅ 完成 |
| 4. 变分参数演化代码实现与实验 | 进行中 |

## 变分方案要点

详见 [`variational_outline/README.md`](variational_outline/README.md)，核心策略：

- **三种离散演化起点**（对应三个相分区 `pidx ∈ {1,0,-1}`），内层对各起点路径做变分优化，取 cost 最小的分支作为同相判定
- **代价函数**：$H_c =$ 能量 + 对称性惩罚（实际实验仅含此两项，ZR 距离与演化时间惩罚为可选扩展）
- **路径参数化**：二次贝塞尔曲线，控制点用 $(u_s, u_\delta)\in[0,1]$ 线性换元
- **三层优化**：外层扫 trotter 阶数/步数，内层扫起点分支，底层优化连续参数（$v_0, u_s, u_\delta, \Delta t_n, d_n$）
- **电路实现**：`PauliEvolutionGate` 手动绑定演化路径和步长
