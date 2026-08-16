# Quarto 与 Markdown 代码块发送 REPL

**日期**: 2026-08-15 17:28
**分类**: 编程/Julia
**标签**: #julia #quarto #markdown #otter #iron

## 背景

需要在更适合阅读的普通 Markdown 文档中运行 Julia 或 Python 代码块，同时保留 Quarto 文档的代码运行能力。

## 内容

`quarto-nvim` 的 runner 可以通过 `otter.nvim` 提取文档中的代码块，再使用 `iron.nvim` 将代码发送到对应 REPL：

```lua
require("quarto.runner").run_cell()
```

Quarto 的 `ftplugin/quarto.lua` 会自动激活 Otter，但普通 Markdown 不会自动执行该 ftplugin。因此 Markdown 需要单独调用 Otter，并使用标准 Markdown fenced-code 注入规则：

````markdown
```julia
println("hello")
```
````

配置中的 `lspFeatures.chunks = "curly"` 适合 Quarto 的：

````markdown
```{julia}
println("hello")
```
````

不应直接用这套 curly 查询解析普通 Markdown，否则普通 ```` ```julia ```` 代码块可能无法被识别。

## 要点

- Quarto 与普通 Markdown 可以共用 `quarto.runner` 和 `iron.nvim`。
- Markdown 应使用普通 fenced code，例如 ```` ```julia ````。
- Quarto 仍使用 ```` ```{julia} ```` 形式，原有行为不需要改变。
- Python 与 Julia 的 runner 选择由代码块语言决定。
