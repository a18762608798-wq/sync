# Julia Union{Nothing, T} 处理 JSON 可选字段

**日期**: 2026-07-20
**分类**: 编程/Julia
**标签**: #julia #json #类型系统 #可选字段

## 背景

在 QMeasPost 项目中，`RandomMeasResult` 结构体需要从 JSON 文件加载数据。JSON 中某些字段（如 `trivial_params`、`trivial_count_group`）可能存在也可能不存在，需要用 Julia 的类型系统优雅处理。

## 内容

对于 JSON 中可选的字段，使用 `Union{Nothing, T}` 类型声明：

```julia
struct RandomMeasResult
    runner::String
    meas_mode::String
    ...
    trivial_params::Union{Nothing, Vector{Dict{String, Matrix{Float64}}}}
    trivial_count_group::Union{Nothing, Vector{Vector{Dict{String, Int}}}}
end
```

对应的解析函数检查 key 是否存在且不为 `null`（`isnothing`），有则解析，无则返回 `nothing`：

```julia
function _opt_parse_params(raw, key)
    if haskey(raw, key) && !isnothing(raw[key])
        return [_parse_param_block(p) for p in raw[key]]
    end
    nothing
end
```

## 要点

- `Union{Nothing, T}` 是 Julia 中表示"可为空的值"的惯用方式，等价于其他语言的 `Optional<T>`
- `haskey(raw, key) && !isnothing(raw[key])` 同时检查 key 存在性和值非空
- 这种做法比用 `Dict{String, Any}` 更类型安全
