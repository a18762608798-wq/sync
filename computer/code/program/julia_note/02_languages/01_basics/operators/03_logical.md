# logical operators

```{julia}
var1 = 2.3;
var2 = 1.1;
boolvar1 = !(var1 == 2.3)
boolvar2 = (var1 == 2.3) && (var2 == 1.1)
boolvar3 = (var1 == 2.3) || (var2 == 1.1)
println(boolvar1, boolvar2, boolvar3)
println(typeof(boolvar1), typeof(boolvar2), typeof(boolvar3))
```

```{julia}
# bool values can be used in arithmetic operations as integer.
var3 = boolvar1 + 1
println(boolvar1)
println(var3) # Note that Bool is an integer type.
```
