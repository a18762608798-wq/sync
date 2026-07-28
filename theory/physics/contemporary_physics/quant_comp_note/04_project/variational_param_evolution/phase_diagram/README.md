# SSH 基态 $Z_R$ 相图

## 方法

### 计算相图热力图

1. **截断**：对 8+ 比特系统，先求 SSH 基态 $|\psi_0\rangle$，然后对边缘 4 个比特求偏迹.
2. **扫描**：在 $(s, \delta) \in [0,1] \times [0,1]$ 参数空间等间距取 $N\times N$ 个格点
3. **计算**：每个格点求基态 $|\psi_0(s,\delta)\rangle$，截断后计算 $Z_R$ 值

### 计算相边界

1. 固定 $\delta = 1$, 求 $Z_R=0$ 点作为相边界, 记录此时的 $s_p$
2. 以 $s_p$ 作为中分点，在上下 $s$ 区间分别取若干固定 $s$ 的垂线，记录此时相边界对应的 $δ_p$
3. 做图描述 $s_p$ 以及 $δ_p$ 随 $N$ 变化.

## 文件结构

```
phase_diagram/
├── get_ssh_ZR.jl          # 求 SSH 基态并计算 ZR_val（含截断）
├── get_ssh_phase.jl       # 扫描参数空间，保存 npz 数据
├── get_phase_boundary.jl  # 计算相边界（ZR=0 的临界点）
├── plot_ssh_phase.py      # 绘制热力图
├── plot_phase_boundary.py # 绘制相边界图
├── data/                  # 数据输出
└── pics/                  # 图像输出
```

## 使用

```bash
# 生成相图数据（8 比特，100×100 格点）
julia --project=. phase_diagram/get_ssh_phase.jl

# 绘制热力图
python phase_diagram/plot_ssh_phase.py

# 生成相边界数据
julia --project=. phase_diagram/get_phase_boundary.jl

# 绘制相边界图
python phase_diagram/plot_phase_boundary.py
```
