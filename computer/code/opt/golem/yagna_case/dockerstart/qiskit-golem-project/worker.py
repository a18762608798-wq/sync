import sys
import json
import numpy as np  # 新增
import rustworkx as rx
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorSampler, StatevectorEstimator

def cost_func_vqe(params, circuit, hamiltonian, estimator):
    """Return estimate of energy from estimator

    Parameters:
        params (ndarray): Array of ansatz parameters
        ansatz (QuantumCircuit): Parameterized ansatz circuit
        hamiltonian (SparsePauliOp): Operator representation of Hamiltonian
        estimator (Estimator): Estimator primitive instance

    Returns:
        float: Energy estimate
    """
    pub = (circuit, hamiltonian, params)
    cost = estimator.run([pub]).result()[0].data.evs
    return cost
    
        
def main():
    # 获取输入参数（采样点数 N）
    try:
        qaoa_layer = int(sys.argv[1])
        if qaoa_layer <= 0:
            raise ValueError
    except:
        qaoa_layer = 5  # 默认值，防止出错
    # ----------
    n = 4
    G = rx.PyGraph()
    G.add_nodes_from(range(n))
    # The edge syntax is (start, end, weight)
    edges = [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    G.add_edges_from(edges)
    hamiltonian = SparsePauliOp.from_list(
    [("IIZZ", 1), ("IZIZ", 1), ("IZZI", 1), ("ZIIZ", 1), ("ZZII", 1)]
    )
    ansatz = QAOAAnsatz(hamiltonian, reps=qaoa_layer) # Designing parametric variational circuits based on the Hamiltonian.
    # Draw
    # display(ansatz.decompose(reps=1).draw()) # decompose the circ to a more fundational form. t is a placeholder.
    # Sum the weights, and divide by 2
    offset = -sum(edge[2] for edge in edges) / 2
    h_m = 10
    for i in range(200 * qaoa_layer):
        x0 = 1/np.sqrt(qaoa_layer) * 2 * np.pi * np.random.rand(ansatz.num_parameters) # iteration of the params of cost layer and mixer layer
        estimator = StatevectorEstimator()
        new_h_m = cost_func_vqe(x0, ansatz, hamiltonian, estimator)
        if h_m > new_h_m:
            h_m = new_h_m
    max_cut_cost = -(1/2 * h_m + offset)
    
    # ----------
    # 输出结果
    result = {
        "status": "success",
        "max_cut_cost": max_cut_cost,
        "qaoa_layer": qaoa_layer,
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()