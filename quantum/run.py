"""Cloud CLI with estimates, validated checkpoints and downloadable scientific output."""

import argparse
from dataclasses import asdict
import hashlib
import json
import logging
import os
from pathlib import Path
import platform
import sys
import time

from .resources import Config, available_memory_mb, estimate_memory_mb, plan


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def fingerprint(config):
    values = asdict(config)
    for key in ('max_seconds', 'memory_mb'):
        values.pop(key)
    digest = hashlib.sha256(json.dumps(values, sort_keys=True).encode())
    for name in ('run.py', 'resources.py', 'oscillator.py'):
        digest.update(Path(__file__).with_name(name).read_bytes())
    import numpy, scipy
    digest.update(f'{numpy.__version__}/{scipy.__version__}'.encode())
    return digest.hexdigest()


def checkpoint(path, identity, n, width, states):
    """Treat restored data as untrusted: no pickle; recompute residuals and norms."""
    import numpy as np
    from .oscillator import diagnostics, hamiltonian, solve
    if path.exists():
        with np.load(path, allow_pickle=False) as data:
            metadata = json.loads(str(data['metadata'].item()))
            if metadata != {'fingerprint': identity, 'n': n, 'width': width, 'states': states}:
                raise ValueError(f'checkpoint parameters/code differ: {path.name}')
            x, energies, psi = data['x'], data['energies'], data['psi']
        expected_x, dx, h = hamiltonian(n, width)
        if (x.shape != (n,) or energies.shape != (states,) or psi.shape != (n, states)
                or not all(np.all(np.isfinite(a)) for a in (x, energies, psi))
                or not np.array_equal(x, expected_x) or np.any(np.diff(energies) <= 0)):
            raise ValueError(f'invalid checkpoint arrays: {path.name}')
        report = diagnostics(x, dx, h, energies, psi)
        if (max(report['scaled_residuals']) > 1e-7
                or report['orthogonality_error'] > 1e-9
                or max(abs(v - 1) for v in report['normalizations']) > 1e-9):
            raise ValueError(f'checkpoint failed numerical validation: {path.name}')
        report.update(grid_points=n, half_width=width, dx=dx, seconds=0.0, resumed=True)
        logging.info('Validated and resumed checkpoint %s', path.name)
        return x, energies, psi, report
    x, energies, psi, report = solve(n, width, states)
    metadata = {'fingerprint': identity, 'n': n, 'width': width, 'states': states}
    temporary = path.with_suffix('.tmp')
    with temporary.open('wb') as stream:
        np.savez_compressed(stream, x=x, energies=energies, psi=psi,
                            metadata=json.dumps(metadata, sort_keys=True))
    temporary.replace(path)
    report['resumed'] = False
    logging.info('Saved checkpoint %s (%.3fs)', path.name, report['seconds'])
    return x, energies, psi, report


def validate_results(reports, domain_report):
    import numpy as np
    finest = reports[-1]
    errors = np.array([r['absolute_energy_errors'] for r in reports])
    spacings = np.array([r['dx'] for r in reports])
    orders = []
    for i in range(1, len(reports)):
        row = []
        for previous, current in zip(errors[i - 1], errors[i]):
            # Avoid claiming an order when errors are at floating-point resolution.
            row.append(float(np.log(previous / current) / np.log(spacings[i - 1] / spacings[i]))
                       if min(previous, current) > 1e-9 else None)
        orders.append(row)
    finite_orders = [v for row in orders for v in row if v is not None]
    convergence = all(1.7 <= v <= 2.3 for v in finite_orders)
    convergence &= bool(finite_orders) or float(np.max(errors)) < 1e-8
    convergence &= bool(np.all(errors[1:] <= errors[:-1] + 1e-9))
    domain_shift = np.abs(np.array(finest['energies_reduced'])
                          - domain_report['energies_reduced'])
    checks = {
        'relative_energy_error_below_1e-4': max(finest['relative_energy_errors']) < 1e-4,
        'wavefunction_l2_error_below_1e-3': max(finest['wavefunction_l2_errors']) < 1e-3,
        'analytic_overlap_above_0_9999': min(finest['analytic_overlaps']) > 0.9999,
        'normalized_and_orthogonal': all(
            max(abs(v - 1) for v in r['normalizations']) < 1e-9
            and r['orthogonality_error'] < 1e-9 for r in reports + [domain_report]),
        'scaled_eigenpair_residual_below_1e-7': all(
            max(r['scaled_residuals']) < 1e-7 for r in reports + [domain_report]),
        'second_order_convergence': bool(convergence),
        'domain_energy_shift_below_1e-7': float(np.max(domain_shift)) < 1e-7,
        'domain_spacing_matches': bool(np.isclose(finest['dx'], domain_report['dx'], rtol=0, atol=1e-14)),
    }
    return {'passed': all(checks.values()), 'checks': checks,
            'energy_convergence_orders': orders,
            'roundoff_floor_for_order': 1e-9,
            'domain_energy_shifts': domain_shift.tolist()}


def outputs(folder, config, finest, reports, domain_report, resource_plan, started):
    import numpy as np
    import scipy
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from .oscillator import analytic_wavefunctions
    x, energies, psi, report = finest
    analytic = analytic_wavefunctions(x, config.states)
    length, energy_unit = config.scales()
    exact = np.arange(config.states) + 0.5
    validation = validate_results(reports, domain_report)
    np.savez_compressed(folder / 'wavefunctions.npz', xi=x, x=x * length,
                        psi_reduced=psi, psi=psi / np.sqrt(length),
                        analytic_psi_reduced=analytic, energies_reduced=energies,
                        energies=energies * energy_unit)
    np.savetxt(folder / 'energies.csv', np.column_stack((np.arange(config.states), energies,
        exact, energies * energy_unit, np.abs(energies - exact), np.abs(energies - exact) / exact)),
        delimiter=',', header='n,E_over_hbar_omega,analytic_E_over_hbar_omega,E_physical,absolute_error_reduced,relative_error', comments='')
    rows = [[r['grid_points'], r['dx'], n, e, r['absolute_energy_errors'][n], r['seconds']]
            for r in reports for n, e in enumerate(r['energies_reduced'])]
    np.savetxt(folder / 'convergence.csv', rows, delimiter=',',
               header='grid_points,dx,n,E_reduced,absolute_error,solve_seconds', comments='')
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout='constrained')
    axes[0].plot(x, 0.5 * x**2, color='gray', label='V/(hbar omega)')
    for n, value in enumerate(energies):
        axes[0].axhline(value, linewidth=0.6)
        axes[0].plot(x, value + 0.5 * psi[:, n], label=f'n={n}')
    axes[0].set(xlim=(-5, 5), ylim=(0, config.states + 1), xlabel='xi = x/a',
                ylabel='E/(hbar omega); wavefunctions offset for display', title='Sparse oscillator')
    axes[0].legend(fontsize=7)
    axes[1].plot(np.arange(config.states), energies, 'o', label='Numerical')
    axes[1].plot(np.arange(config.states), exact, '+', label='Analytical')
    axes[1].set(xlabel='n', ylabel='E/(hbar omega)', title='Energy spectrum')
    axes[1].legend()
    fig.savefig(folder / 'spectrum.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout='constrained')
    for n in range(config.states):
        axes[0].plot(x, psi[:, n], label=f'n={n}')
        axes[0].plot(x, analytic[:, n], '--', linewidth=0.8)
        axes[1].loglog([r['dx'] for r in reports],
                       [max(r['absolute_energy_errors'][n], 1e-16) for r in reports], 'o-', label=f'n={n}')
    spacings = np.array([r['dx'] for r in reports])
    axes[1].loglog(spacings, reports[0]['absolute_energy_errors'][0] * (spacings / spacings[0])**2,
                   'k--', label='O(dx^2)')
    axes[0].set(xlim=(-config.half_width, config.half_width), xlabel='xi', ylabel='psi(xi)',
                title='Numerical (solid) / analytical (dashed)')
    axes[1].set(xlabel='dx in oscillator lengths', ylabel='Absolute energy error (reduced)', title='Grid convergence')
    for axis in axes:
        axis.legend(fontsize=7)
    fig.savefig(folder / 'convergence.png', dpi=160)
    plt.close(fig)
    summary = {'schema_version': 1, 'parameters': asdict(config),
               'units': {'length_scale_a': length, 'energy_scale_hbar_omega': energy_unit,
                         'defaults': 'reduced units: hbar=m=omega=1',
                         'conversion': 'x=a*xi; E=hbar*omega*epsilon; psi(x)=phi(xi)/sqrt(a)'},
               'method': 'CSC tridiagonal centered finite differences; Dirichlet walls; eigsh shift-invert sigma=0',
               'grids': reports, 'domain_check': domain_report, 'finest': report,
               'validation': validation, 'resource_plan': resource_plan,
               'elapsed_seconds': time.perf_counter() - started,
               'provenance': {'git_sha': os.environ.get('GITHUB_SHA'),
                              'run_id': os.environ.get('GITHUB_RUN_ID'),
                              'resumed_from_run_id': os.environ.get('RESUME_RUN_ID') or None,
                              'python': platform.python_version(), 'numpy': np.__version__,
                              'scipy': scipy.__version__, 'matplotlib': matplotlib.__version__,
                              'fingerprint': fingerprint(config)}}
    write_json(folder / 'summary.json', summary)
    text = ['## Quantum harmonic oscillator', '', f"Validation passed: **{validation['passed']}**", '',
            '| n | Numerical E/(hbar omega) | Analytical | Relative error |', '|---|---:|---:|---:|']
    for n, value in enumerate(energies):
        text.append(f'| {n} | {value:.12f} | {exact[n]:.1f} | {report["relative_energy_errors"][n]:.3e} |')
    text += ['', f"Grid: {config.grid_points}; domain: +/- {config.half_width} a; levels: {config.levels}.",
             f"Convergence orders: {validation['energy_convergence_orders']}",
             f"Max residual: {max(report['scaled_residuals']):.3e}; domain shift: {max(validation['domain_energy_shifts']):.3e}.",
             f"Elapsed: {summary['elapsed_seconds']:.3f} s; estimated peak: {max(resource_plan['estimated_peak_mb_per_grid']):.1f} MiB.",
             '', 'Download quantum-results for arrays, CSV, figures, parameters, logs and checkpoints.']
    (folder / 'report.md').write_text('\n'.join(text) + '\n', encoding='utf-8')
    manifest = {str(path.relative_to(folder)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(folder.rglob('*')) if path.is_file() and path.suffix != '.log'
                and path.name not in ('manifest.json', 'status.json')}
    write_json(folder / 'manifest.json', manifest)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
            stream.write('\n'.join(text) + '\n')
    logging.info('VERIFIED_RESULTS %s', json.dumps(summary, allow_nan=False))
    return validation['passed']


def main(argv=None):
    parser = argparse.ArgumentParser(description='Cloud-only sparse oscillator demonstration')
    for name, value in asdict(Config()).items():
        parser.add_argument('--' + name.replace('_', '-'), type=type(value), default=value)
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--dry-run', action='store_true', help='validate and estimate memory without solving')
    args = parser.parse_args(argv)
    folder = args.output
    folder.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', force=True,
                        handlers=[logging.StreamHandler(), logging.FileHandler(folder / 'calculation.log')])
    started = time.perf_counter()
    write_json(folder / 'status.json', {'status': 'started'})
    # Final results from a restored artifact must never masquerade as new results.
    for name in ('summary.json', 'report.md', 'manifest.json', 'wavefunctions.npz',
                 'energies.csv', 'convergence.csv', 'spectrum.png', 'convergence.png'):
        (folder / name).unlink(missing_ok=True)
    try:
        config = Config(**{name: getattr(args, name) for name in asdict(Config())}).validate()
        write_json(folder / 'parameters.json', asdict(config))
        preflight = plan(config, available_mb=available_memory_mb())
        write_json(folder / 'resource_plan.json', preflight)
        if args.dry_run:
            print(json.dumps(preflight, indent=2))
            write_json(folder / 'status.json', {'status': 'planning_only', 'calculation_completed': False})
            return 0
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            raise RuntimeError('run calculations in GitHub Actions; use --dry-run locally')
        from .oscillator import solve
        _, _, _, pilot = solve(255, config.half_width, config.states)
        preflight = plan(config, pilot['seconds'], available_memory_mb())
        write_json(folder / 'resource_plan.json', preflight)
        logging.info('PREFLIGHT %s', json.dumps(preflight))
        identity = fingerprint(config)
        checkpoint_folder = folder / 'checkpoints'
        checkpoint_folder.mkdir(exist_ok=True)
        reports, finest = [], None
        jobs = [(n, config.half_width) for n in config.grids()]
        jobs.append((config.domain_grid(), config.half_width * 1.25))
        for index, (n, width) in enumerate(jobs):
            remaining = config.max_seconds - (time.perf_counter() - started)
            if remaining < preflight['estimated_seconds_per_grid'][index] + 30:
                raise TimeoutError('remaining budget too small; completed grids are checkpointed')
            current_available = available_memory_mb()
            budget = min(config.memory_mb, 0.6 * current_available) if current_available is not None else config.memory_mb
            if estimate_memory_mb(n, config.states) > budget:
                raise MemoryError('available memory decreased; refusing larger grid')
            path = checkpoint_folder / f'{"domain" if index == len(jobs) - 1 else "grid"}-{n}.npz'
            result = checkpoint(path, identity, n, width, config.states)
            if index < len(jobs) - 1:
                reports.append(result[3])
                finest = result
            else:
                domain_report = result[3]
            write_json(folder / 'progress.json', {'completed_grids': index + 1, 'total_grids': len(jobs),
                                                  'last_grid': result[3]})
        passed = outputs(folder, config, finest, reports, domain_report, preflight, started)
        write_json(folder / 'status.json', {'status': 'completed' if passed else 'validation_failed',
                                           'calculation_completed': True, 'validation_passed': passed})
        return 0 if passed else 2
    except (ValueError, RuntimeError, OSError, OverflowError, TimeoutError, MemoryError) as error:
        logging.exception('Calculation stopped: %s', error)
        write_json(folder / 'status.json', {'status': 'failed', 'calculation_completed': False, 'error': str(error)})
        return 2


if __name__ == '__main__':
    sys.exit(main())
