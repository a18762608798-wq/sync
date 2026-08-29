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
    correct: bool = False
    target_qubits: list[int] = field(default_factory=list)
    coupling_map: list | None = None
    optimization_level: int = 3
    basis_gates: list[str] = field(default_factory=lambda: ["rz", "rx", "ry", "cz"])


@dataclass
class EstimatorConfig:
    qc: QuantumCircuit
    observables: list[SparsePauliOp]
    runner_opts: AerEstimatorOptions | QuarkEstimatorOptions = field(
        default_factory=AerEstimatorOptions
    )
