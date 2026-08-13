# Qiskit SPSA 的 history 记录、最终结果与 resamplings 行为

**日期**: 2026-08-13 13:11
**分类**: 理论/量子计算
**标签**: #Qiskit #SPSA #变分优化 #VQE #鲁棒优化

## 背景

在变分参数演化项目（variational_param_evolution）中，用 Qiskit 的 `SPSA` 优化器对含噪目标函数（真机/Aer 采样）做参数优化。需要记录优化轨迹并理解最终结果含义，排查"history 里很多 `fun` 比 `res.fun` 更优"的疑惑。

## 内容

### 1. 用 callback 记录 SPSA 轨迹（闭包捕获）

SPSA 支持 `optimizer.callback`，每次迭代调用，签名：
`callback(nfev, parameters, value, stepsize, accepted)`。

通过 Python 闭包，callback 可直接引用外层函数的 `history` 列表：

```python
history = []
def callback(nfev, parameters, value, stepsize, accepted):
    if accepted:
        history.append({
            "fun": float(value),
            "t": np.array(parameters, copy=True).tolist(),
        })
optimizer.callback = callback
```

要点：
- 只记录 `accepted=True` 的点（blocking/trust_region 判定真正被接受的更新）。
- 让 objective 收到的 `history=None`，避免 objective 内部重复记录，history 完全由 callback 统一管理。
- 初始点 t0、被拒绝的点都不进 history。

### 2. SPSA 的 result 是"最后一个被接受点"，非最优点

- Qiskit SPSA 本质是随机梯度下降，**默认不维护 best-so-far**。
- `result.x` / `result.fun` 对应**最后一次被接受的迭代点**及其函数值，因此可能比 history 中某些访问过的点更差。
- 想要返回最优，需在 callback 里自己维护：`min(history, key=lambda h: h["fun"])`。

### 3. result.fun 是在最终参数处重新评估一次

同一组参数在 history 中记录的 `value` 与 `res.fun` 可能不同（如 `-2.8918` vs `-2.8544`）：
- 因为 SPSA 结束时用最终 `result.x` **重新评估一次**目标函数，写入 `result.fun`。
- 目标函数含噪（shot noise / 多样本平均）时，同一参数两次评估结果不同。
- 结论：含噪场景下 `res.fun` 或单次 history 值都不稳，应在最优参数处多次评估取均值。

### 4. resamplings 参数：每次迭代都重采样

- `resamplings=N` 表示**每次参数更新（每次迭代）**用 N 个不同扰动向量 Δ 做 N 次梯度估计并取平均，用于压低 shot 噪声。
- 非"只在最后一个点"重采样。
- 代价：每迭代目标评估次数变为 `2 × resamplings`（blocking 时还要额外验算），增大 resamplings 会按比例增加评估开销。

## 要点

- SPSA history = 所有 accepted 更新点的 `{fun, t}` 轨迹，靠 callback + 闭包累积。
- `result.x/fun` = 最后接受点，SPSA 不保留最优，需要自维护。
- `result.fun` = 最终参数处**重测**一次，含噪下与 history 值不一致属正常。
- `resamplings` 是**每次迭代**的梯度重采样平均次数，不是只针对最后一个点。
