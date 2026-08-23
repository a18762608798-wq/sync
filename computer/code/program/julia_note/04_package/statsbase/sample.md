# sample

## 线性采样

```{julia}
using StatsBase
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
probabilities = [0.1, 0.2, 0.05, 0.15, 0.1, 0.1, 0.05, 0.1, 0.05, 0.1]  # 需确保概率和为1
# 无放回抽样（replace=false）
k = 1
test_index = sample(data, ProbabilityWeights(probabilities), k; replace=false)[1]  # size = 1. return vec
```

### `sample` method

```julia
sample(data, weights, k; replace=true)
```

- `data` — 采样空间
- `weights` — 权重，用 `Weights(w)` 或 `ProbabilityWeights(w)` 包装
- `k` — 采样次数
- `replace=true` — 放回抽样

### `Weights` type

- `Weights(vec(prob))` 将普通向量包装为权重类型，`sample` 会自动归一化，不需要事先归一化。
- `ProbabilityWeights(vec(prob))` 要求输入就是归一化的.
