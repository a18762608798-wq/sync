# grouping

## 准备：import and obs

```python
from qiskit.quantum_info import PauliList, Pauli, SparsePauliOp

observable = SparsePauliOp.from_list([
    ("XI", 1.0),
    ("YY", 1.0),
])

observables = [
    observable,
    SparsePauliOp("XY"),
    SparsePauliOp("ZZ"),
]
```

## 分组

```python
# 用集合特性找到bases交集, 转为string(be used to sort)
all_labels = {
    label
    for obs in observables
    for label in obs.paulis.to_labels() # Transform from PauliList to string。
}

all_paulis = PauliList(sorted(all_labels)) # 重新转换成 Qiskit 的 PauliList 对象
# PauliList(['XI', 'XY', 'YY', 'ZZ']), I < X,
groups = all_paulis.group_commuting(
    qubit_wise=True # NOTE: True表示逐位对易.
) # [PauliList(['YY']), PauliList(['ZZ']), PauliList(['XI', 'XY'])]
```
