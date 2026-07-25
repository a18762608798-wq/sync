# Julia 空 Vector 与定长 Vector 创建方式

**日期**: 2026-07-20 22:50
**分类**: 编程/Julia
**标签**: #Julia #数组 #Vector

## 背景

在 Julia 中创建指定类型的空 vector 或预分配固定长度的 vector 有多种写法，性能和初始化行为不同。

## 内容

### 空 vector

```julia
v = Int[]          # ✅ 推荐，简洁
v = Float64[]      # []
v = String[]       # []
v = ComplexF32[]   # []

# 等价于
v = Vector{Int}()          # 同样返回空 vector
v = Vector{Float64}()
```

`Int[]` 是 Julia 社区的惯用风格。

### 定长 vector（预分配）

#### 1. `undef` — 不初始化（性能最快）

```julia
v = Vector{Int}(undef, 10)       # 长度 10，内容为垃圾值
v = Vector{Float64}(undef, 5)    # 用之前必须逐个赋值
```

`undef` 表示"未初始化内存"——不写入任何值，分配后内存中是随机的旧数据。

#### 2. `zeros` / `ones` — 全零/全一初始化

```julia
v = zeros(Int, 10)       # [0, 0, 0, ...]
v = ones(Float64, 5)     # [1.0, 1.0, 1.0, ...]
```

#### 3. `fill` — 指定填充值

```julia
v = fill(0, 10)                  # 全 0
v = fill(1.5, 5)                # 全 1.5
v = fill("hello", 3)            # ["hello", "hello", "hello"]
v = fill(ComplexF64(0, 0), 4)   # 全 0+0im
```

### 四种方式对比

| 方式 | 初始化内容 | 性能 | 适用场景 |
|------|-----------|------|---------|
| `Vector{Int}(undef, n)` | **垃圾值**（不初始化） | **最快**（不写内存） | 马上逐个元素覆盖赋值 |
| `zeros(Int, n)` | 全 0 | 略慢（CPU 全写一遍） | 需要默认零值 |
| `fill(x, n)` | 全 x | 同上 | 需要指定初始值 |
| `Int[]` | 空（长度 0） | 不分配大块内存 | 动态增长 |

### `similar` — 保持类型和形状

```julia
A = rand(3, 4)
v = similar(A, 10)         # 与 A 相同元素类型的 Vector，长度 10
m = similar(A, (5, 5))     # 与 A 相同元素类型的 Matrix，5×5
```

## 要点

- 空 vector：`Int[]`（推荐）或 `Vector{Int}()`
- 定长预分配：`undef` 最快但需要立即赋值；`zeros`/`fill` 适合需要已知初始值
- `similar` 用于保持元素类型创建新数组
