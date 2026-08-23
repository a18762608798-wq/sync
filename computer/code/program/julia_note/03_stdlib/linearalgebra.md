# tmp

## 张量积（Kronecker 积）

```julia
using LinearAlgebra
A = ones((2, 2))
B = ones((2, 2))
kron(A, B)  # 计算矩阵 A 和 B 的张量积
```

## 对角化 / 特征分解

```julia
using LinearAlgebra

eigen(A)      # 返回特征值-特征向量结构体（包含 values 和 vectors 字段）
eigvals(A)    # 仅返回特征值向量
eigvecs(A)    # 仅返回特征向量矩阵
svd(A)        # 奇异值分解
```
