# counts

## 一元计数

```julia
using StatsBase
samples = [1, 1, 2, 3]
support = 1:4 # 就是统计UnitRange中的元素, 不用Vector是效率问题.
counts(samples, support)
```

### counts method

```julia
counts(samples::AbstractArray{<:Integer}, support::UnitRange{<:Integer}) -> Vector{Int}
```

> 统计 `samples` 中每个 `support` 元素的出现次数，返回与 `support` 等长的频数向量；
> `samples` 中不属于 `support` 的值被静默忽略。

* `samples` — 采样结果向量
* `support` — 统计元素
* 返回值 — 与 support 等长的频数向量，`freq[k]` = 值 k 出现的次数
