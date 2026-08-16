# basic

## defined

```python
from qiskit.quantum_info import SparsePauliOp

# basicc defined.
obs = SparsePauliOp.from_list([
    ("XX", 1.0),
    ("YY", 1.0),
])

# defined by the bit position.
xx = SparsePauliOp.from_sparse_list(
    [
        ("XX", [0, 1], 1.0)
    ],
    num_qubits=2,
)
```

## operation

### simplify

```python
obs.simplify()  # 合并同类项
```

### is_hermitian

```python
assert obs == obs.transpose().conjugate()  # H.is_hermitian() 也可以用
```

### pauli to label

```python
print(obs.paulis.to_labels())
```

### 提取pauli strings

```python
# 利用集合特性可以挑选出不同的pauli strings
all_labels = {
    label
    for obs in observables
    for label in obs.paulis.to_labels() # 它把Qiskit 内部的 PauliList 转成普通字符串列表, qiskit 顺序。
}
```

### get the pauli list form obs

```python
import numpy as np
def get_commute_group(obs):
    # get pauli list
    pauli_list = {
        label
        for ob in obs
        for label in ob.paulis.to_labels()  # 它把Qiskit 内部的 PauliList 转成普通字符串列表。
    }

    pauli_list = PauliList(sorted(pauli_list))  # 重新转换成 Qiskit 的 PauliList 对象
    # get commute group
    meas_basis_ls = []
    groups = pauli_list.group_commuting(qubit_wise=True)
    for group in groups:
        basis_x = np.logical_or.reduce(
            group.x,
            axis=0,
        )  # 每一个比特是否含x布尔分量
        basis_z = np.logical_or.reduce(
            group.z,
            axis=0,
        )

        measurement_basis = Pauli((basis_z, basis_x))
        meas_basis_ls.append(measurement_basis)

    return groups, meas_basis_ls

groups, meas_basis_ls = get_commute_group(observables)
```
