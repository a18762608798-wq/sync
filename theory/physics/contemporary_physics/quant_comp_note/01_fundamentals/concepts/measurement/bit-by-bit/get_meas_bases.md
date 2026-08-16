# get meas bases

## 编码方式

Qiskit 不是用一个标记表示 I、X、Y、Z，而是用两个布尔值 z 和 x 共同表示. 可以**粗浅理解为pauli op是否含有 Z, X 分量**。

| Pauli |     `z` |     `x` |
| ----- | ------: | ------: |
| `I`   | `False` | `False` |
| `X`   | `False` |  `True` |
| `Y`   |  `True` |  `True` |
| `Z`   |  `True` | `False` |

反过来把每个位置的 z、x 信息合起来，即可判断测量基(**只对逐比特对易有效**)

| `basis_z` | `basis_x` | 测量基 |
| --------: | --------: | --- |
|     False |     False | I   |
|     False |      True | X   |
|      True |     False | Z   |
|      True |      True | Y   |

例如 X, I → X, 对应 [(False, True), (False, False)] → (False, True)

## 代码

```python
import numpy as np
from qiskit.quantum_info import PauliList, Pauli, SparsePauliOp

bases = []
for group in groups:
    basis_x = np.logical_or.reduce(
        group.x,
        axis=0,
    ) # 每一个比特是否含x布尔分量
    basis_z = np.logical_or.reduce(
        group.z,
        axis=0,
    ) # 是否含z分量. 

    measurement_basis = Pauli(
        (basis_z, basis_x)
    ) # 对z, x编码分别求 lor 操作，结合得测量基
    bases.append(measurement_basis)

bases = PauliList(bases) # transform list to PauliList.
print(bases)
```
