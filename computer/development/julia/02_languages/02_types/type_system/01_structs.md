# structs

structs are a kind of specific types.

## immutable struct

```julia
# structs are a kind of specific types.
# immutable struct.
struct Person
    name::String # fields
    age::Int
end

p = Person("Tom", 20)
p.age = 21   # which is error, you can not change the value of age, because it is immutable.
println(p)
```

## mutable struct

```julia
# mutable struct.
mutable struct Person
    name::String
    age::Int
end

p = Person("Tom", 20)
p.age = 21   # 可以
println(p.age)   # 21
```
