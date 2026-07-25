# Julia `Project.toml` 依赖分类规则

**日期**: 2026-07-20 23:10
**分类**: 编程/Julia
**标签**: #Julia #包管理 #Project.toml

## 背景

写 `Project.toml` 时，不清楚哪些包需要写进 `[deps]`，哪些不需要。涉及第三方包、独立标准库、Base 子模块三类的区分。

## 内容

### `[deps]` 三分类

| 类别 | 例子 | 写 `[deps]`？ | 写法 |
|------|------|-------------|------|
| **第三方包** | ITensors, JSON, StatsBase | ✅ **必须写** | `] add` 自动填入 UUID |
| **独立标准库** | LinearAlgebra, Statistics, Random, Test | ✅ **必须写** | 手动写入 UUID，不需要 `] add` |
| **Base 子模块** | Base.Threads, Core | ❌ **不写** | 语言内置，永远可用 |

### 标准库 UUID 的获取

不需要记，几种方式：

```julia
# 方式一：代码查
using LinearAlgebra
Base.PkgId(LinearAlgebra).uuid   # "37e2e46d-..."

# 方式二：Julia 安装目录
# ~/.julia/juliaup/julia-1.12.6/share/julia/stdlib/v1.12/LinearAlgebra/Project.toml

# 方式三：从已有项目复制（UUID 固定不变）
```

### `[compat]` 是可选的

```toml
# 完全省略 [compat] 段 — 合法
[deps]
ITensors = "9136182c-..."

# 只写需要的约束 — 推荐
[compat]
ITensors = "0.7"
julia = "1.10"
```

`[compat]` 不写表示不限制版本。空着整个段或只写部分依赖的约束都可以。

### `Base.Threads` 特殊处理

`Base.Threads` 是 `Base` 的子模块，不是独立的包：

```toml
# ❌ 错误 — Threads 不是独立的包
[deps]
Threads = "..."

# 代码中直接用
using Base.Threads   # 或 Threads.@threads for ...
```

`[compat]` 中也无需涉及 `Threads`。线程功能依赖的 Julia 版本通过 `julia = "1.x"` 控制。

### 判断规则

不确定某个模块是否要写 `[deps]` 时：

1. 能否 `] add <包名>`？ → 能则写
2. 是标准库（LinearAlgebra, Statistics）？ → 写
3. 是 `Base.XXX` 或 `Core.XXX`？ → **不写**

## 要点

- 第三方包：`] add` 自动处理
- 独立标准库：手动写 `[deps]`，不需 `add`
- Base 子模块（Threads, Core）：从不写 `[deps]`
- `[compat]` 可选，省略即不限制版本
