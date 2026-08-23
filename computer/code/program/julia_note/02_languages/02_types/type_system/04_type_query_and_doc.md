# type query and doc

## reflection

```julia
x = 1
typeof(x) # which return the specific type of x, in this case, it is Int64, which is a subtype of Integer,
x isa Int64 # judge whether x is an instance of Int64.
Int64 <: Signed # judge whether Int64 is a subtype of Signed.
```

## the doc of types

```julia
# 不同 constructor methods 接收不同 arguments，但最终都会构造出同一类对象，并且这个对象有同样的 fields。
# the arguments of different methods must be writen by youself.
# default documentation will only display the fundamental info.
@doc Cat
subtypes(Animal)
supertype(Cat)
fieldnames(typeof(c))
using InteractiveUtils
@which Cat('c')
```
