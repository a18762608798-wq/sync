# the environment configuration of julia

## the package manager

### instantiation

* julia

Run the order at terminal in your folder as follow:

```julia
using Pkg
Pkg.activate(".")
Pkg.add("LanguageServer") # which provides the language server for julia, and it is the dependency of the vscode extension of julia.
```

If you clone a project of orders, run:

```julia
using Pkg
Pkg.activate(".")
Pkg.instantiate()
Pkg.add("LanguageServer")
```

* python

We recommend to use the pyjulia package **with the activate environment** in the mixed project with python and julia.

```julia
using CondaPkg
CondaPkg.add("numpy")
```

You could get the info of package in CondaPkg.toml and Project.toml.

### usage

* use `Pkg.activate(".")` in repl, then

```julia
include("test.jl")
```

* use `julia --project=@. main.jl` (which means search the toml file forward).
