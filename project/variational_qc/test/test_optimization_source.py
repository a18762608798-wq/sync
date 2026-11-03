"""Source/continuation checks; no hardware calls and no actual retired parameters."""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from optimization_source import (OPTIMIZATION_PROTOCOL, protocol_of,
                                  require_same_provenance, validate_s06)


def test_legacy_protocol_refused():
    with pytest.raises(ValueError, match='retired data refused'):
        protocol_of({})
    assert protocol_of({'optimization_protocol': np.frombuffer(OPTIMIZATION_PROTOCOL.encode(), dtype=np.uint8)}) == OPTIMIZATION_PROTOCOL


def test_parameter_or_run_change_refuses_resume():
    identity = {'run_id': 'test-independent', 's06_sha256': 'abc'}
    require_same_provenance(dict(identity), identity, 'unit')
    for changed in [None, {}, {**identity, 'run_id': 'previous'}, {**identity, 's06_sha256': 'def'}]:
        with pytest.raises(ValueError, match='resume refused'):
            require_same_provenance(changed, identity, 'unit')


def test_circuit_change_refuses_existing_task(monkeypatch):
    import exp07_submit as submit
    from qiskit import QuantumCircuit
    directory = Path(tempfile.mkdtemp(prefix='source-resume-', dir=ROOT / 'data/validation'))
    state_path = directory / 'state.json'
    monkeypatch.setattr(submit, 'unit_state_path', lambda uid: state_path)
    phase = [0.2]
    def circuits(*args):
        circuit = QuantumCircuit(8)
        circuit.rx(phase[0], 0)
        return {'g0': circuit}
    monkeypatch.setattr(submit, 'build_unit_tasks', circuits)
    identity = {'run_id': 'test-independent', 's06_sha256': 'abc'}
    groups = [{'branch': 1}]
    mapping = {1: list(range(8))}
    submit.prepare_unit(0, groups, {}, mapping, identity)
    state = json.loads(state_path.read_text())
    state['tids']['g0'] = 1  # synthetic identifier; never sent to the backend
    state_path.write_text(json.dumps(state))
    submit.prepare_unit(0, groups, {}, mapping, identity)
    phase[0] = 0.4
    with pytest.raises(ValueError, match='circuit changed'):
        submit.prepare_unit(0, groups, {}, mapping, identity)


def test_formal_source_is_independent():
    with validate_s06(ROOT / 'data/exp04/exp04_S06.npz') as archive:
        for tag in ['dm2', 'd085']:
            assert np.asarray(archive[tag + '_conv']).all()
            assert not np.asarray(archive[tag + '_stagn']).any()
