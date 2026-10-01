"""Second-order finite differences for H/(hbar*omega) = -D2/2 + xi**2/2."""

import os
import time
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


def hamiltonian(n, half_width):
    dx = 2 * half_width / (n + 1)
    x = -half_width + dx * np.arange(1, n + 1, dtype=np.float64)
    h = diags((-np.ones(n - 1) / (2 * dx**2),
               np.ones(n) / dx**2 + 0.5 * x**2,
               -np.ones(n - 1) / (2 * dx**2)), (-1, 0, 1), format='csc')
    return x, dx, h


def analytic_wavefunctions(x, states):
    """Normalized Hermite functions via stable three-term recurrence."""
    psi = np.empty((len(x), states))
    psi[:, 0] = np.pi**(-0.25) * np.exp(-x**2 / 2)
    if states > 1:
        psi[:, 1] = np.sqrt(2) * x * psi[:, 0]
    for n in range(1, states - 1):
        psi[:, n + 1] = (np.sqrt(2 / (n + 1)) * x * psi[:, n]
                         - np.sqrt(n / (n + 1)) * psi[:, n - 1])
    return psi


def diagnostics(x, dx, h, energies, psi):
    analytic = analytic_wavefunctions(x, len(energies))
    dots = np.sum(psi * analytic, axis=0) * dx
    psi *= np.where(dots < 0, -1.0, 1.0)
    overlap = np.abs(dots) / np.sqrt(np.sum(analytic**2, axis=0) * dx)
    residuals = np.linalg.norm(h @ psi - psi * energies, axis=0) * np.sqrt(dx)
    residuals /= np.maximum(1.0, np.abs(energies))
    norms = np.sum(psi**2, axis=0) * dx
    orthogonality = np.max(np.abs(psi.T @ psi * dx - np.eye(len(energies))))
    exact = np.arange(len(energies)) + 0.5
    return {'energies_reduced': energies.tolist(), 'analytic_energies_reduced': exact.tolist(),
            'absolute_energy_errors': np.abs(energies - exact).tolist(),
            'relative_energy_errors': (np.abs(energies - exact) / exact).tolist(),
            'wavefunction_l2_errors': (np.sqrt(np.sum((psi - analytic)**2, axis=0) * dx)).tolist(),
            'analytic_overlaps': overlap.tolist(), 'normalizations': norms.tolist(),
            'scaled_residuals': residuals.tolist(), 'orthogonality_error': float(orthogonality)}


def solve(n, half_width, states):
    if n > 255 and os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('grids above 255 points may only be solved in GitHub Actions')
    started = time.perf_counter()
    x, dx, h = hamiltonian(n, half_width)
    # Shift-invert at zero: sparse tridiagonal factorization; no dense Hamiltonian.
    energies, vectors = eigsh(h, k=states, sigma=0.0, which='LM', tol=1e-11,
                             maxiter=4000, ncv=min(n, max(20, 2 * states + 1)),
                             v0=np.random.default_rng(1729).normal(size=n))
    order = np.argsort(energies)
    energies, psi = energies[order], vectors[:, order] / np.sqrt(dx)
    report = diagnostics(x, dx, h, energies, psi)
    report.update(grid_points=n, half_width=half_width, dx=dx,
                  seconds=time.perf_counter() - started)
    return x, energies, psi, report
