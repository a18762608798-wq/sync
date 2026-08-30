from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

Ensemble = Literal["haar", "pauli"]


@dataclass(frozen=True)
class SettingRun:
    setting_num: int
    shot_num: int


@dataclass(frozen=True)
class AerOptions:
    method: str = "matrix_product_state"
    device: str = "CPU"
    precision: str = "single"
    correction: bool = False


@dataclass
class QuarkOptions:
    chip: str = "Baihua"
    token: str | None = None
    target_qubits: list[int] = field(default_factory=list)
    correction: bool = False
    coupling_map: list | None = None
    optimization_level: int = 3
    basis_gates: list[str] = field(default_factory=lambda: ["rz", "rx", "ry", "cz"])
    correct: bool = False


@dataclass
class RandomMeasConfig:
    qc: QuantumCircuit
    setting_runs: list[SettingRun]
    meas_indices: list[tuple[int, ...]]
    runner_opts: AerOptions | QuarkOptions = field(default_factory=AerOptions)
    ensemble: Ensemble = "haar"
    seed: int | None = None
    output_dir: Path = field(default_factory=lambda: Path("./data"))
    name: str = "experiment"

    def __post_init__(self) -> None:
        self.output_dir = Path(self.output_dir)

        # 初始化 ParameterVector
        group_num = len(self.meas_indices)
        self.params = [
            ParameterVector("theta", group_num),
            ParameterVector("phi", group_num),
        ]

        # 检查输入格式
        if not self.setting_runs:
            raise ValueError("setting_runs cannot be empty")

        if not self.meas_indices:
            raise ValueError("meas_indices cannot be empty")

        if any(len(group) == 0 for group in self.meas_indices):
            raise ValueError("meas_indices groups cannot be empty")
