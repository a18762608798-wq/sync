# integer

## the foundational types of integers

```julia
α = Int8(1)
β = UInt8(1)
γ = 1
```

## operation

```julia
isodd(1)
iseven(1)
```

## special number system

### binaray system

#### assignment

```julia
# bin octal and hex literals
α = 0b1010 # bin
```

#### operation

##### bit operation

> Julia 中位运算结果默认以 `UInt8` 类型显示，`UInt8` 的 `show` 方法选择用 `0x` 十六进制格式展示。可以用 `bitstring` 展示二进制(8 位固定长度).

```julia
α = 0b0001
β = 0b1000

# 按位逻辑
bitstring(α ⊻ β) # xor
bitstring(α & β) # or
bitstring(α | β) # not
bitstring(~α)        # NOT（按位取反）
bitstring(bswap(α))  # 字节翻转(四个字节顺序翻转，但是内部不变.)
```

```julia
# 移位
bitstring(β)
n = 1
bitstring(β << n)    # 整体左移，右边补0; 1 << n ⇔ 2^n
bitstring(β >>> n)   # 整体右移，左边补0
bitstring(β >> n)    # 整体右移，左边补符号位(最高位为1则补一，反之补0)
```

##### others

```julia
count_ones(α)
count_zeros(β)
leading_zeros(α)          # 前导零
trailing_zeros(β)         # 末尾零
```

### other systems

```julia
β = 0o010777 # octal
γ = 0x1abcdef # hex
# Even if there are leading zero digits which don’t contribute to the value.
γ1 = 0x1abcdef 
γ2 = 0x0001abcdef 
println("the decimalism of γ1 and γ2 is $(γ1) and $(γ2)")
```

```julia
# Julia 的十六进制字面量强制为无符号类型，负号仅触发补码运算而不改变类型属性
a = -0x001
b = -0x00000001
println("the type of a and b is ", typeof(a), typeof(b))
```

## the range of any types of integer

```julia
# the min and max value of any type.
for T in [Int8,Int16,Int32,Int64,Int128,UInt8,UInt16,UInt32,UInt64,UInt128]
    println("$(lpad(T, 7, " ")): [$(typemin(T)),$(typemax(T))]") # lpad为字符小于7则左填充
end
```

```julia
# use big() to extend the range of integers, but it is not a type, it is a function that returns a BigInt object.
bignum1 = typemax(Int128) + 1
bignum2 = big(typemax(Int128)) + 1
println("bignum1, bignum2 are $bignum1, $bignum2")
```
