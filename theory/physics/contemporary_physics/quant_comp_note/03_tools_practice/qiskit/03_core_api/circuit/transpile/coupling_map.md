# coupling_map

Limit the topological structure.

* Greate the circuit

```python
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit import transpile
from qiskit.transpiler import CouplingMap

qc = QuantumCircuit(3, 3)
qc.swap(0, 1)
qc.swap(0, 2)
qc.measure([0, 1, 2], [0, 1, 2])
qc.draw()

```

## 线性门

```python
# 4 个量子比特呈线型：0--1--2--3
coupling_map = CouplingMap.from_line(3)

qc2 = transpile(
    qc,
    coupling_map=coupling_map,
    routing_method="sabre", # 根据硬件连接图寻找可行路径, 要求优化
    optimization_level=3, 
)

qc2.draw()
```

## 指定结构

```python
coupling_map = [
    [0, 1], [1, 0],
    [1, 2], [2, 1],
    [2, 3], [3, 2],
] # 有方向

qc2 = transpile(
    qc,
    coupling_map=coupling_map,
    routing_method="sabre",
)

qc2.draw()
```
