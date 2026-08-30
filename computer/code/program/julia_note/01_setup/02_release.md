# release

## locally

### Release(Install) locally

```julia
# 进入Package目录
]
generate RandomMeasAdd # NOTE: 创造的是空包, 如果已经有代码, 需要手动合并.
```

这样将创建 `Project.toml`.

### Install locally

```julia
pkg> activate .
# 如果是在RadnomMeasAdd内部无需dev.
pkg> dev ~/sync/theory/physics/contemporary_physics/quant_comp_note/03_tools_practice/RandomMeasAdd
```

```text
dev  = 跟踪本地源码目录
add  = 安装一个“版本/提交状态”
```
