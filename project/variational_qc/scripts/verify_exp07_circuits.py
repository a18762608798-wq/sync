"""Compare all Exp07 logical circuits with Julia state references, zero QPU calls."""
import argparse
import json
from pathlib import Path

import numpy as np
from qiskit.quantum_info import Statevector

from exp07_circuits import branch_circuit
from exp07_common import S06_REF, line_dir, read_json, validate_batch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    info = read_json(line_dir() / 'groups.json')
    identity = validate_batch(info)
    reference = np.load(args.reference)
    assert len(info['groups']) == len(reference['psi']) == 90
    max_infidelity = 0.0
    for index, group in enumerate(info['groups']):
        key = [group['delta_idx'], group['s_idx'], group['branch']]
        assert np.array_equal(reference['indices'][index], key)
        circuit = branch_circuit(root / S06_REF, *key, group['delta'])
        circuit.remove_final_measurements()
        actual = np.asarray(Statevector.from_instruction(circuit).data)
        expected = reference['psi'][index]
        fidelity = float(abs(np.vdot(expected, actual)) ** 2)
        assert abs(np.vdot(actual, actual) - 1.0) < 1e-10
        assert abs(1.0 - fidelity) < 1e-10, (key, fidelity)
        max_infidelity = max(max_infidelity, abs(1.0 - fidelity))
    report = {'circuits_checked': 90, 'max_state_infidelity': max_infidelity,
              'reference_energies_checked_in_julia': True, 'provenance': identity}
    output = Path(args.reference).with_name('exp07-circuit-verification.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
