# NPZ

## save

```julia
using NPZ

path = "./04_package/files_interation/basic.npz"
data = Dict(
    "vec" => [1, 2]
)

npzwrite(
    path,
    data,
)
```

## read

```julia
data = npzread(path)
```
