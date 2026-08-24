# QuantumCircuit

## bases

### defined

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(1, 1)
qc.measure([0], [0]) # 0 classical register records 0 qubits.
qc.draw()
```

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.measure([0], [0])
qc.draw()
qc.draw(cregbundle=True) # 强制clbits合成一条线
```

### Operation of qc

```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate
qc = QuantumCircuit(2, 2)
qc.num_qubits # get the qubits num.
qc.num_clbits # git the classical bits num.
qc.x([0]) # append gates
qc.inverse().draw() # dagger
qc.barrier()              # 对全部量子比特加 barrier
print(qc.depth())      # 电路深度
print(qc.data)         # 电路中每条指令的列表
qc.append(evo_odd, range(qubit_num)) # 示例代码, 没有经典比特直接append
qc.append(single_qc.inverse(), range(qubit_num), cargs) # 有经典比特需要写上映射range
```

### decompose and transpile

对于复杂门需要transpile, 但是如果decompose()到底(默认reps=1)，确实不需要transpile.

* transpile 可以直接转换带参数电路.
* transpile 会尽量减少电路深度，很建议开.

```python
from qiskit import QuantumCircuit, transpile
from qiskit import qasm2
qc = QuantumCircuit(2, 2)
qc.cx([0], [1])
qc.decompose().draw() 
qc_basis = transpile(
    qc,
    basis_gates=["rx", "ry", "rz", "cz"],
    optimization_level=3, # 优化等级
) 
qc_basis.draw()
```

| level | 大致力度 | 关键特点                                               |
| ----- | ---- | -------------------------------------------------- |
| `0`   | 只求能跑 | basis translation / routing 等必要转换，不主动优化            |
| `1`   | 轻度   | 合并单比特门、消掉紧挨着的逆门                                    |
| `2`   | 中/重度 | level 1 + **commutation 分析** + 做一次 **1Q/2Q block**(只涉及一个或两个 qubit 的连续小块, 暴力等效) 重综合 |
| `3`   | 最重   | level 2 + **把 2Q block 重综合放进优化循环里反复做**             |
