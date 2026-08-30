# installization

## the installization of julia

### the installization in linux mint

```bash
rm -rf ~/.juliaup ~/.julia 2>/dev/null
curl -fsSL https://install.julialang.org | sh
source ~/.profile  # 使配置生效
```

the further renew

```bash
juliaup update
```

uninstallization as follow

```bash
# 卸载juliaup（官方推荐方式）
juliaup self uninstall

# 手动清理残留
rm -rf ~/.juliaup
rm -rf ~/.julia
rm -rf ~/.cache/julia
rm -rf ~/.local/share/julia
```

### the installization in windows

Simply download the exe file.

## other config

### multithreading

add `export JULIA_NUM_THREADS=8` in `~/.profile`
