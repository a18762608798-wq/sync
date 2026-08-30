# the environment configuration of julia

## the julia project

Run the order at terminal in your folder as follow:

```bash
using Pkg
Pkg.activate(".")
# nvim is not needed to install it.
#Pkg.add("LanguageServer") # which provides the language server for julia, and it is the dependency of the vscode extension of julia.
```

If you clone a project of orders, run:

```bash
using Pkg
Pkg.activate(".")
Pkg.instantiate()
```

> 不同 Julia project/environment 可以隔离依赖版本，但共享下载缓存；同版本包一般不重复下载，不同版本、artifact、预编译缓存或不同 depot 才会额外占空间

```bash
# 启动 Julia，并把当前目录 . 作为 active project。
julia --project=.
```

## python in julia

### install package

We recommend to use the pyjulia package **with the activate environment** in the mixed project with python and julia.

```julia
using CondaPkg
CondaPkg.add("numpy")
CondaPkg.add_pip("quarkstudio") # NOTE: quarkstudio does not included in conda, use PYPI.
CondaPkg.add_pip("mineru"; extras=["all"]) # When you have extra pip params.
```

If you clone a project of orders, run:

```{julia}
using CondaPkg
CondaPkg.resolve()
```

### CIL in current environment

```{bash}
"${SHELL}" <(curl -L micro.mamba.pm) # install micromamba to run CIL
```

Then activate the environment via micromamba.

```{bash}
micromamba activate -p .CondaPkg/.pixi/envs/default
```

## usage

* use `Pkg.activate(".")` in repl, then

```julia
include("test.jl")
```

* use `julia --project=@. main.jl`(which means search the toml file forward).
