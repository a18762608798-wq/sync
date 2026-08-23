# json

## save

```julia
using JSON

path = "./04_package/files_interation/basic.json"
data = Dict(
    "vec" => [1, 2]
)

open(path, "w") do io
    JSON.print(io, data)
end
```

## read

```julia
result = JSON.parsefile(path)
```
