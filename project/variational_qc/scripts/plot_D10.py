"""Plot the formal D10 pair from validated Exp07 products, without new numerics."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

from exp07_common import line_dir, read_json, validate_batch
from figure_style import (apply_figure_style, finalize_figure, uniform_text,
                          font_pt_for, PRINT_TEXT_PT, effective_min_text_pt)
from optimization_source import file_sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=None)
    parser.add_argument('--output-dir', default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    directory = Path(args.root) if args.root else line_dir()
    output = Path(args.output_dir) if args.output_dir else root / 'figs/exp07'
    info = read_json(directory / 'groups.json')
    identity = validate_batch(info)
    manifest = read_json(directory / 'exp07_manifest_joint.json')
    if manifest['provenance'] != identity:
        raise ValueError('D10 source identity differs from current batch')
    data_path = directory / 'exp07_D10_joint.npz'
    data = np.load(data_path)
    apply_figure_style()
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.3), sharey=True)
    colors = {1: '#D62728', 2: '#0072B2', 3: '#000000'}
    markers = {1: 'o', 2: 's', 3: '^'}
    labels = {1: 'triv', 2: 'topo', 3: 'Néel'}
    pairs = np.asarray(data['pairs'])
    for axis, delta, di, letter in zip(axes, [-2.0, 0.85], [1, 2], ['(a)', '(b)']):
        mask = pairs[:, 0] == di
        axis.plot(pairs[mask, 1] / 100, np.asarray(data['q_sim30'])[mask],
                  color='#7f7f7f', linestyle='-', label=r'sim $p=2$')
        for branch in [1, 2, 3]:
            selected = np.isclose(data['deltas'], delta) & (data['branch'] == branch)
            assert int(selected.sum()) == 15
            axis.errorbar(data['s_idx'][selected] / 100, data['win_mean'][selected],
                          yerr=data['win_se'][selected], fmt=markers[branch],
                          color=colors[branch], capsize=2.5,
                          markeredgecolor='black', markeredgewidth=0.6,
                          label=f'exp $p=2$ ({labels[branch]})')
        axis.set_title(rf'$\delta={delta}$')
        axis.set_xlabel(r'$s$')
        axis.text(0.5, -0.32, letter, transform=axis.transAxes,
                  ha='center', va='top', clip_on=False)
    axes[0].set_ylabel(r'$Q$')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=4, frameon=False)
    fig.subplots_adjust(bottom=0.35, top=0.88, wspace=0.12)
    uniform_text(fig, font_pt_for(fig, PRINT_TEXT_PT))
    output.mkdir(parents=True, exist_ok=True)
    finalize_figure(fig, output / 'exp07_D10.pdf')
    finalize_figure(fig, output / 'exp07_D10.png')
    report = {'source_sha256': file_sha256(data_path), 'provenance': identity,
              'effective_minimum_text_pt': effective_min_text_pt(fig, PRINT_TEXT_PT * 25.4 / 72),
              'font_path': font_manager.findfont('Times New Roman', fallback_to_default=False),
              'palette': colors, 'markers': markers,
              'panel_tags': 'below each axis, centered', 'exports': ['exp07_D10.pdf', 'exp07_D10.png']}
    (output / 'exp07_D10-style.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    plt.close(fig)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
