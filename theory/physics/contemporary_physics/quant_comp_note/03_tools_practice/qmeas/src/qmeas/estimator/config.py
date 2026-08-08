from dataclasses import dataclass, field

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp


@dataclass
class AerEstimatorOptions:
    method: str = "matrix_product_state"


@dataclass
class QuarkEstimatorOptions:
    token: str | None = None
    quark_options: dict = field(default_factory=lambda: {
        "chip": "Baihua",
        "shots": 1024,
        "name": "estimator",
        "compiler": "qiskit",
        "correct": True,
        "target_qubits": [],
    })


@dataclass
class EstimatorConfig:
    qc: QuantumCircuit
    observables: list[SparsePauliOp]
    runner_opts: AerEstimatorOptions | QuarkEstimatorOptions = field(
        default_factory=AerEstimatorOptions
    )
