"""Formal D10 assertions against every raw acquisition unit, zero QPU calls."""
import argparse
import json
import math
from pathlib import Path

import numpy as np

from exp06_assemble import (group_Ms, mitigate_counts, obs_basis_arrays,
                            q_hat_basis, unit_q_se_qb)
from exp07_assemble import (SCHEMA, pair_sim_q, search_best_branch_window,
                            branch_point_index, MANIFEST_KEYS)
from exp07_common import (N_POINTS, ROUND_UNITS, SHOTS, line_dir, read_json,
                          validate_batch)
from exp07_submit import (build_theta_map, build_unit_tasks, unit_task_meta,
                          cached_transpile, allowed_edges)
from optimization_source import require_same_provenance, file_sha256
from qiskit import qasm2
import hashlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=None)
    parser.add_argument('--figures-only', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    directory = Path(args.root) if args.root else line_dir()
    product_path = directory / 'exp07_D10_joint.npz'
    if args.figures_only:
        figure_dir = root / 'figs/exp07'
        report = read_json(figure_dir / 'exp07_D10-style.json')
        assert report['source_sha256'] == file_sha256(product_path)
        assert report['effective_minimum_text_pt'] >= 8
        for extension in ['pdf', 'png']:
            assert (figure_dir / f'exp07_D10.{extension}').stat().st_size > 0
        print('VERIFY-EXP07-FIGURES-OK')
        return
    info = read_json(directory / 'groups.json')
    bill = read_json(directory / 'rounds/r001/bill.json')
    identity = validate_batch(info, bill)
    manifest = read_json(directory / 'exp07_manifest_joint.json')
    assert MANIFEST_KEYS <= set(manifest) and manifest['schema'] == SCHEMA
    require_same_provenance(manifest['provenance'], identity, 'D10 manifest')
    data = np.load(product_path)
    groups = info['groups']
    assert len(groups) == N_POINTS == 90 and bill['n_units'] == ROUND_UNITS == 500
    unit_ids = np.arange(bill['unit_start'], bill['unit_start'] + bill['n_units'])
    assert np.array_equal(data['unit_ids'], unit_ids)
    assert manifest['n_units'] == manifest['window']['N'] == 500
    assert data['s_post'].shape == data['o_post'].shape == (500, 90)
    theta_map = build_theta_map(groups)
    expected_theta = np.array([theta_map[(g['delta_idx'], g['s_idx'], g['branch'])] for g in groups])
    np.testing.assert_array_equal(data['theta'], expected_theta)
    for key, field in [('s_idx', 's_idx'), ('deltas', 'delta'), ('branch', 'branch')]:
        np.testing.assert_array_equal(data[key], [g[field] for g in groups])
    physical = {1: info['chain_top1'], 2: info['subchain_top1'], 3: info['chain_top1']}
    circuits = build_unit_tasks(groups, theta_map, physical)
    task_physical, task_branch = unit_task_meta(groups, physical)
    expected_hashes = {key: hashlib.sha256(qasm2.dumps(cached_transpile(circuit, task_branch[key])).encode()).hexdigest()
                       for key, circuit in circuits.items()}
    expected_keys = set(circuits)
    assert len(expected_keys) == 92
    spi_basis, string_basis = obs_basis_arrays()
    endpoints = manifest['endpoints']
    qb = q_hat_basis(endpoints['S_max'], endpoints['O_max'])
    tids = []
    for row, uid in enumerate(unit_ids):
        state = read_json(directory / 'units' / f'{uid:05d}' / 'state.json')
        require_same_provenance(state.get('provenance'), identity, f'unit {uid}')
        assert set(state['tids']) == set(state['counts']) == expected_keys
        assert state['qasm_sha256'] == expected_hashes
        tids.extend(state['tids'].values())
        for key in expected_keys:
            audit = state['transpile'][key]
            assert audit['in_allowed']
            assert all(tuple(edge) in allowed_edges(task_branch[key]) for edge in audit['cz_edges'])
            options = state['submit_params'][key]
            assert options['shots'] == SHOTS and options['correct'] is False
            assert options['target_qubits'] == task_physical[key]
        matrices = group_Ms({key: state['counts'][key] for key in ['cal_zero', 'cal_one']},
                           physical[groups[0]['branch']])
        np.testing.assert_allclose(data['s05'][row], matrices, rtol=0, atol=1e-12)
        for gi in range(90):
            counts = state['counts'][f'g{gi}']
            assert all(np.isfinite(value) and value >= 0 for value in counts.values())
            probabilities = mitigate_counts(counts, matrices)
            raw = np.zeros(256)
            for bitstring, count in counts.items():
                raw[int(bitstring, 2)] += count
            assert raw.sum() > 0
            raw /= raw.sum()
            for field, value in [('s_post', probabilities @ spi_basis),
                                  ('o_post', probabilities @ string_basis),
                                  ('s_pre', raw @ spi_basis), ('o_pre', raw @ string_basis),
                                  ('q_post', probabilities @ qb),
                                  ('q_se_unit', unit_q_se_qb(probabilities, qb, SHOTS))]:
                np.testing.assert_allclose(data[field][row, gi], value, rtol=0, atol=1e-10)
    assert len(tids) == len(set(tids)) == bill['total_tasks'] == 46000
    source_manifest = read_json(root / 'data/exp04/exp04_manifest.json')
    retirement = root / source_manifest.get('migration', {}).get('retirement_record', '') / 'retired-task-ids.json'
    if retirement.is_file():
        assert not set(tids).intersection(read_json(retirement)['task_ids'])
    simulated, pairs = pair_sim_q()
    np.testing.assert_allclose(data['q_sim30'], simulated, rtol=0, atol=1e-12)
    branches, pair_indices = branch_point_index(groups)
    window = search_best_branch_window(data['s_post'], data['o_post'], simulated, branches, pair_indices)
    assert window['start'] == manifest['window']['start']
    assert window['length'] == manifest['window']['length']
    for key in ['S_max', 'O_max']:
        np.testing.assert_allclose(window[key], endpoints[key], rtol=0, atol=1e-12)
    for key in ['r_a', 'd_raw_a']:
        actual = {str(k): v for k, v in window[key].items()}
        for branch in ['1', '2', '3']:
            np.testing.assert_allclose(actual[branch], manifest['branch_stats'][key][branch], rtol=0, atol=1e-12)
    start, length = window['start'], window['length']
    selected = data['q_post'][start:start + length]
    np.testing.assert_allclose(data['win_mean'], selected.mean(axis=0), rtol=0, atol=1e-12)
    np.testing.assert_allclose(data['win_se'], selected.std(axis=0, ddof=1) / math.sqrt(length), rtol=0, atol=1e-12)
    validate_batch(info, bill)
    report = {'units_verified': 500, 'points_verified': 45000, 'unique_tasks': 46000,
              'all_raw_observables_recomputed': True, 'window_recomputed': True,
              'source_sha256': file_sha256(product_path), 'provenance': identity}
    (directory / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('VERIFY-EXP07-OK ' + json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
