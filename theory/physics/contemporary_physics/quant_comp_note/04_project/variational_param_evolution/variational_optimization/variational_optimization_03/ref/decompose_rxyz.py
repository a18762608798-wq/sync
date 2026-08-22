from qiskit import transpile
from qiskit.circuit import QuantumCircuit, Parameter

theta_x = Parameter("θx")
theta_y = Parameter("θy")
theta_z = Parameter("θz")

qc = QuantumCircuit(2)
qc.rxx(theta_x, 0, 1)
qc.ryy(theta_y, 0, 1)
qc.rzz(theta_z, 0, 1)

qc_num = qc.assign_parameters(
    {
        theta_x: 0.31,
        theta_y: 0.57,
        theta_z: 0.83,
    }
)

qc_optimization = transpile(
    qc_num,
    basis_gates=["rz", "rx", "ry", "cz"],
    optimization_level=3,
)
print(qc_optimization.draw())
