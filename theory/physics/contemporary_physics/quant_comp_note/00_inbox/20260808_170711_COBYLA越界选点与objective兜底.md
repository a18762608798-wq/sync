# COBYLA 越界选点问题与 objective 兜底

**日期**: 2026-08-08 17:07
**分类**: 理论/量子计算
**标签**: #COBYLA #约束优化 #scipy #越界 #调试

## 背景

用 COBYLA 优化变分参数时，`get_evolution_path` 对 `Δtds∈[0,1]` 有硬性 assert，结果 COBYLA 探点时传入 `Δtds=1.5` 导致崩溃。

## 内容

### 为什么 COBYLA 会越界选点

两层原因：

1. **初始单纯形采样**：COBYLA 在起点 `x0` 周围用单纯形采样，初始步长 `rhobeg` 若偏大，单纯形顶点会落在 `x0 ± rhobeg` 而越界（例：`x0` 的 `Δtds=0.5`，`rhobeg` 足够大探到 `1.5`）。
2. **约束只"引导"不"拦截"**：COBYLA 把边界/约束当作目标里的软限制，生成候选点（可能任意越界）后**仍会先调用一次 objective**，靠返回的目标值+约束值判断是否接受。所以约束拦不住"评估这一步"，越界点只是被评估后淘汰。

### 解决方案

在 `objective` 入口兜底，保证任何候选点物理合法。两种：

**夹取（clip）**：
```python
x = x.copy()
x[0:3] = np.clip(x[0:3], 0, 1)
x[3:3+step] = np.clip(x[3:3+step], 1e-2, 10)
x[3+step:3+2*step] = np.clip(x[3+step:3+2*step], 0, 1)
```
优点：数值平滑；缺点：越界点被"合法化"评估，边界附近 COBYLA 拿不到"越界多差"的信号。

**惩罚（BAD_VAL）**：
```python
BAD_VAL = 1e6
if (越界条件): return BAD_VAL
```
优点：越界点明确变差、COBYLA 快速避开；缺点：常数坏值不提供方向信息。

### 推荐

夹取（防崩溃） + 轻微越界惩罚（引导避开）结合：
```python
x_clamped = np.clip(x, lb, ub)
viol = np.maximum(lb - x, x - ub, 0).sum()
return objective(x_clamped) + 1e3 * viol
```

### 最常越的界

- `Δtds` 上界 1（`get_evolution_path` 有硬性 `[0,1]` assert）——最致命。
- `Δts` 下界 0（硬性 `>0` assert）。
- `v0/sp/δp` 越界不 assert，只值不物理。

## 要点

- COBYLA 越界是因为单纯形探点 + 约束不拦截 objective 求值。
- 约束只引导搜索方向，不能防止 objective 被越界点调用。
- 兜底做法：objective 入口 clip 或返回坏值。
- 缩小 `rhobeg` 可从源头减少越界。
