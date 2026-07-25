# Julia `CartesianIndex` 访问方式与 N 维数组迭代

**日期**: 2026-07-20 22:30
**分类**: 编程/Julia
**标签**: #Julia #数组 #迭代 #CartesianIndex

## 背景

在 N 维数组（如 `Array{Int, N}`）的处理中，需要遍历所有元素或获取多维坐标，涉及 `CartesianIndex` 的访问方式和 `eachindex` / `CartesianIndices` 两种迭代模式的选择。

## 内容

### 访问 `CartesianIndex` 的各维度坐标

`CartesianIndex` 底层的元组通过 `I.I` 获取，支持多种访问方式：

```julia
I = CartesianIndex(2, 1, 2, 2, 2)

I[1]      # 2   — 第 1 维坐标（零开销，编译期优化）
I[2]      # 1   — 第 2 维坐标
I[5]      # 2   — 第 5 维坐标
I.I       # (2, 1, 2, 2, 2)  — 底层 Tuple，零开销
Tuple(I)  # (2, 1, 2, 2, 2)  — 同上
Vector(I) # [2, 1, 2, 2, 2]  — ❌ 转 Vector 多此一举，堆分配
```

`I.I isa Tuple` —— 永远不需要转成 `Vector`。

### N 维数组的两种迭代方式

```julia
A = rand(Int, 3, 4, 2)  # Array{Int, 3}
```

| 方式 | 返回类型 | 适用场景 | 性能 |
|------|---------|----------|------|
| `eachindex(A)` | `Int` 线性索引 | 只遍历所有元素，不关心坐标 | **最佳** |
| `CartesianIndices(A)` | `CartesianIndex{N}` | 需要各维度坐标或创建同样形状的新数组 | 略慢（需构造对象） |
| `for x in A` | 元素值 | 只需值，不需要索引 | 与线性索引等价 |

```julia
# 线性索引（推荐，最快）
for i in eachindex(A)
    println(A[i])           # 列主序
end

# 笛卡尔索引（需要多维坐标）
for idx in CartesianIndices(A)
    println(idx)            # CartesianIndex(2, 3, 1)
    println(A[idx])         # 用 CartesianIndex 访问
    A[idx] += 1
end

# 两者互相转换
ci = CartesianIndices(A)[1]  # 线性 → Cartesian
li = LinearIndices(A)[ci]    # Cartesian → 线性
```

### N 维数组常见处理模式

```julia
function process_counts(counts::Array{Int, N}) where N
    # 只需值
    total = sum(counts)

    # 需要坐标（例如创建同样形状的数组用于输出）
    result = similar(counts, Float64)
    for idx in CartesianIndices(counts)
        result[idx] = Float64(counts[idx]) / total
    end

    # 需要 N 的值
    println("输入是 $N 维数组")

    return result
end
```

## 要点

- `I[d]` 和 `I.I` 获取 `CartesianIndex` 的维度坐标，零开销
- **默认用 `eachindex`**（线性），只在需要多维坐标时用 `CartesianIndices`
- 不需要转 `Vector`——`I.I` 直接就是 `Tuple`
