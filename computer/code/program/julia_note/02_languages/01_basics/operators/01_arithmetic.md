# arithmetic operators

## binary operator

```{julia}
var1 = 2.1;
var2 = 1.0;
var1 ÷ var2 # (\div + tab) 除法结果只取整数, 但是保留类型.
var1 \ var2 # var2 / var1
var1 % var2 # reminder of var1 / var2
div(var1, var2) # solve the division
mod(var1, var2) # solve the modulo
rem(7, 3)       # 1 — 取余，结果符号与 x 相同
rem(-7, 3)      # -1
mod(7, 3)       # 1 — 取模，结果符号与 y 相同
mod(-7, 3)      # 2
divrem(7, 3)    # (2, 1) — 同时返回商和余数
```

## unary operator: round off

```{julia}
var1 = -1.1;
round(var1)
floor(var1)
ceil(var1)
trunc(var1)  # 去尾
```

## unary operator: math operation

```{julia}
var = 2;
println("复数优先级高于其他运算符: ", 2var/5im)
abs(var)
abs2(var)  # 平方
sign(var)
cbrt(var) # 三次根
log(2, var)  # log2(x)
cos(var)
exp(var)
sqrt(var)
real(var)
imag(var)
angle(var)
binomial(10, 2) # C_10^2
```
