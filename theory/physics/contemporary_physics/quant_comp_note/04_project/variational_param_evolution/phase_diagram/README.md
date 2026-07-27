# SSH 基态 $Z_R$ 相图

## 方法

1. **截断**：对 8+ 比特系统，先求 SSH 基态 $|\psi_0\rangle$，然后对中间 4 个比特求偏迹，去除边缘自由比特的简并影响
2. **扫描**：在 $(s, \delta) \in [0,1] \times [0,1]$ 参数空间等间距取 $N\times N$ 个格点
3. **计算**：每个格点求基态 $|\psi_0(s,\delta)\rangle$，截断后计算 $Z_R$ 值

## 文件结构

```
phase_diagram/
├── get_ssh_ZR.jl       # 求 SSH 基态并计算 ZR_val（含截断）
├── get_ssh_phase.jl    # 扫描参数空间，保存 npz 数据
├── plot_ssh_phase.py   # 绘制热力图
├── data/               # 数据输出
└── pics/               # 图像输出
```

## 使用

```bash
# 生成相图数据（8 比特，100×100 格点）
julia --project=. phase_diagram/get_ssh_phase.jl

# 绘制热力图
python phase_diagram/plot_ssh_phase.py
```
