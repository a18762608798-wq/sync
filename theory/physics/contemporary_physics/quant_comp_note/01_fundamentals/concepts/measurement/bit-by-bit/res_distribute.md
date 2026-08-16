# res_distribute

## counts 转为 pauli bases 期望

### product mask

给**一个**pauli bases, 转化为一个对非平庸位置的 mask 对应的十进制.

> pauli.x 列表顺序是正常顺序，生成mask过程取反，

**这意味这mask只能用于反序输出**, quafu在 `compiler="qiskit"` 确实是反序counts, 但到底是哪一步实现的不清楚.

```python
def pauli_mask(pauli):
    # Lor: 
    # support[i] = False if pauli[i] == Pauli("I") 
    # else True.
    support = pauli.x | pauli.z 

    # Transform Boole list to binary mask(但是十进制形式).
    return sum(
        int(bit) << i # 1 << i == 2 ** i
        for i, bit in enumerate(support)
    ) 
```

### get pauli vals from hist

只能以一组为例子了

选择组2, 算符为第2组pauli ops.

```python
group = groups[2]
base = bases[2]
shots = 1024
counts = {"00": 500, "01": 524}
masks = [pauli_mask(pauli) for pauli in group]
sums = {
    group[i]: 0 
    for i in range(len(group))
}
for outcome, frequency in counts.items():
    outcome = int(outcome, 2)

    for pauli, mask in zip(group, masks):
        parity = (mask & outcome).bit_count() % 2
        value = -1 if parity else 1

        sums[pauli] += frequency * value

pauli_map = {
    pauli: value_sum / shots
    for pauli, value_sum in sums.items()
}
```

## pauli bases 分发给具体算符

```python
result = 0.0
for pauli, coefficient in zip(
    observables[1].paulis,
    observables[1].coeffs,
):
    label = pauli
    result += coefficient * pauli_map[label]
```
