# demo-pkg

A minimal demo Python package to install from github.

## Install

### python venv

```{bash}
# create the venv
python3 -m venv .venv 
source .venv/bin/activate
```

```bash
# download
python3 -m pip install --upgrade --force-reinstall --no-cache-dir "git+https://github.com/a18762608798-wq/python_note.git@main#subdirectory=06_project/demo_pkg"
```

Or clone and install locally:

```bash
python3 -m pip install -e ./06_project/demo_pkg
```

Update:

```bash
# upgrade from github
pip install --upgrade git+https://github.com/a18762608798-wq/python_note.git#subdirectory=06_project/demo_pkg

# upgrade from local
pip install --upgrade -e .
```

### Julia (via CondaPkg.jl)

Since `demo_pkg` is not on PyPI/Conda, install from GitHub via pip:

```julia
using CondaPkg

CondaPkg.add("pip")

url = "git+https://github.com/a18762608798-wq/python_note.git@main#subdirectory=06_project/demo_pkg"

CondaPkg.withenv() do
    python3 = CondaPkg.which("python3")
    run(`$python3 -m pip install --upgrade --force-reinstall $url`)
end
```

或者安装本地：

```{julia}
CondaPkg.add_pip(
    "demo-pkg";
    version="@ ./06_project/demo_pkg",
    editable=true
)
```

更新的命令

```{julia}
using CondaPkg

url = "git+https://github.com/a18762608798-wq/python_note.git@main#subdirectory=06_project/demo_pkg"

CondaPkg.withenv() do
    python3 = CondaPkg.which("python3")
    run(`$python3 -m pip install --upgrade --force-reinstall --no-cache-dir $url`)
end
```

## uninstall

### python

```bash
python3 -m pip uninstall demo-pkg
```

### julia

```{julia}
using CondaPkg

CondaPkg.withenv() do
    python3 = CondaPkg.which("python3")
    run(`$python3 -m pip uninstall -y demo-pkg`)
end
```

## Usage

### Python

```python
from demo_pkg import hello

print(hello())        # Hello, world!
print(hello("Alice")) # Hello, Alice!
```
