# Release a package locally and install from github

## create format

python 只需要设计好项目格式就行, 本地直接安装不需要generate(或者说julia的generate也是创造格式?)

最简单参考:

```text
[project]
name = "qmeas"
version = "0.1.0"
dependencies = []
```

## locally

### Release

Install(Release) locally:

```julia
using CondaPkg

CondaPkg.rm_pip("qmeas")
path = expanduser(
    "~/sync/theory/physics/contemporary_physics/quant_comp_note/03_tools_practice/qmeas"
)

CondaPkg.add_pip(
    "qmeas";
    version="@file://$path",
    editable=true,
)
```

Update:

```julia
using CondaPkg

url = "git+https://github.com/a18762608798-wq/sync.git@master#subdirectory=theory/physics/contemporary_physics/quant_comp_note/03_tools_practice/qmeas"

CondaPkg.withenv() do
    python3 = CondaPkg.which("python3")
    run(`$python3 -m pip install --upgrade --force-reinstall --no-cache-dir $url`)
end
```

## Github

```julia
using CondaPkg

CondaPkg.add("pip")

url = "git+https://github.com/a18762608798-wq/python_note.git@main#subdirectory=06_project/demo_pkg"

CondaPkg.withenv() do
    python3 = CondaPkg.which("python3")
    run(`$python3 -m pip install --upgrade --force-reinstall $url`)
end
```
