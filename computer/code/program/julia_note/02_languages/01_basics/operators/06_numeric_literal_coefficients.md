# numeric literal coefficients

## format

```{julia}
# The symbol for one element does not require a space, while the symbol for two elements does.
var1 = 1
var2 = 2 * (var1^2 + 1)
var2 = 2(var1^2 + 1) # we could omit the multiplication between the numbers and the variables.
```

## omit limit

```{julia}
#=
any expression that is not a numeric literal,
when immediately followed by a parenthetical, is interpreted as a function.
so only the multiplication between the numbers and the variables can be omitted.
=#
expr1(var) = (var + 1)var
expr2(var) = var(var + 1)
expr3(var) = (var + 1)(var + 1)

try
    expr1(x);
catch
    println("expr1(x) is wrong")
end

try
    expr2(x)
catch
    println("expr2(x) is wrong")
end

try
    expr3(x)
catch
    println("expr3(x) is wrong")
end
```
