from dataclasses import dataclass, field

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp


@dataclass
class AerEstimatorOptions:
    method: str = "matrix_product_state"


@dataclass
class QuarkEstimatorOptions:
    token: str | None = None
    chip: str = "Baihua"
    shots: int = 1024
    name: str = "estimator"
    compiler: str = "qiskit"
    correct: bool = True
    target_qubits: list[int] = field(default_factory=list)


@dataclass
class EstimatorConfig:
    qc: QuantumCircuit
    observables: list[SparsePauliOp]
    runner_opts: AerEstimatorOptions | QuarkEstimatorOptions = field(
        default_factory=AerEstimatorOptions
    )
