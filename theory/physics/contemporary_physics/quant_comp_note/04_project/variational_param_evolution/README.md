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
├── phase_diagram/      # 相图计算与绘制（已完成）
├── symmetry_analysis/  # 对称性分析与约束哈密顿量验证（已完成）
├── concept/            # 概念文档（贝塞尔曲线等）
├── variational_qc/     # 变分量子计算方案设计
├── src/                # 核心源代码
│   ├── create_op.jl            # SSH H、约束 H、SWAP、反射算符
│   ├── get_expect_instance.jl  # ZR 值计算
│   ├── get_spectrum.jl         # 能谱与本征态计算
│   └── var_param_evolution.jl  # 变分演化主入口
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

详见 [`variational_qc/README.md`](variational_qc/README.md)，核心策略：

- **穷举演化起点**，对每个起点到目标态的路径做变分优化，取同相起点组的平均结果
- **代价函数**：$H_c =$ 能量 + 对称性惩罚 + ZR 距离惩罚 + 演化时间惩罚
- **路径参数化**：二次贝塞尔曲线，控制点 $(s_c, \delta_c)$ 作为变分参数
- **电路实现**：`PauliEvolutionGate` 手动绑定演化路径和步长
