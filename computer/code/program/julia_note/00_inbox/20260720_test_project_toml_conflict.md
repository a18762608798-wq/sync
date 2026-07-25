# Julia test/Project.toml 包名冲突导致 Pkg.develop 失败

**日期**: 2026-07-20
**分类**: 编程/Julia
**标签**: #julia #测试 #pkg #环境配置

## 背景

运行 `julia --project=test test/runtests.jl` 时报错 `Package QMeasPost is required but does not seem to be installed`。尝试用 `Pkg.develop(path=".")` 注册主包时报 `has the same name or UUID as the active project`。

## 内容

**问题原因**：`test/Project.toml` 中定义了与主包相同的 `name` 和 `uuid`：

```toml
name = "QMeasPost"
uuid = "0eb3f2fb-1a00-44d2-b32f-d01c869429f6"

[deps]
QMeasPost = "0eb3f2fb-1a00-44d2-b32f-d01c869429f6"
```

当激活测试环境后尝试 `Pkg.develop` 主包时，Julia 检测到名称/UUID 冲突，拒绝操作。

**解决方法**：移除测试 Project.toml 中的顶层 `name` 和 `uuid`，只保留依赖声明：

```toml
[deps]
QMeasPost = "0eb3f2fb-1a00-44d2-b32f-d01c869429f6"
Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
```

然后重新执行：

```bash
julia --project=test -e 'using Pkg; Pkg.develop(path="."); Pkg.instantiate()'
```

## 要点

- 测试环境是独立的 Julia 项目，不应与主包共享 name/uuid
- `test/Project.toml` 可以不设顶层 name 字段（或使用不同的名称如 `"QMeasPostTests"`）
- 部署后 `Pkg.develop(path=".")` 会将主包注册为开发依赖
