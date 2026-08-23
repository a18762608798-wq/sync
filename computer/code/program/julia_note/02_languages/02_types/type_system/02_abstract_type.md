# abstract type

```julia
# abstract type is to difine a abstract classification, containing some structs or other abstract types.
# it can not be instantiated to store specific data.
abstract type Biology end
abstract type Animal <: Biology end

struct Dog <: Animal
    name::String
end

println(Dog <: Biology)
d = Dog("Bob")
```
