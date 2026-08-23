# tuple

## defined

```julia
tuple(1, 2, 3) # 直接定义               
qubit_dims = ntuple(_ -> 2, 2) # 全同元素
```

## transform

```julia
Tuple(1:5) # from UnitRange
Tuple(fill(2, 3)) # from vector
```
