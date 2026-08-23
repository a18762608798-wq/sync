# basic concepts

## definition

* abstract type: could <: to other abstract types but not <: structs.
* specific type(structs)
  * Fields: the params in structs.
* examples: the invocation method of structs.

## tree

```text
Any
├─ Built-in types
│   ├─ abstract type
│   │  ├─ Number
│   │   ├─ Complex
│   │   └─ Real
│   │       ├─ AbstractFloat
│   │       │  ├─ Float16
│   │       │  ├─ Float32
│   │       │  ├─ Float64
│   │       │  └─ BigFloat
│   │       ├─ Integer
│   │       │  ├─ Bool
│   │       │  ├─ Signed
│   │       │  │  ├─ Int8 / Int16 / Int32 / Int64 / Int128 / BigInt
│   │       │  └─ Unsigned
│   │       │     ├─ UInt8 / UInt16 / UInt32 / UInt64 / UInt128
│   │       ├─ Rational
│   │       └─ AbstractIrrational
│   │  ├─ AbstractString
│   │  ├─ AbstractArray{T,N}
│   │  └─ ...
├─ Custom type
```
