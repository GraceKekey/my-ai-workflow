import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from scipy.sparse import issparse

from quantum.oscillator import analytic_wavefunctions, hamiltonian, solve
from quantum.resources import Config
from quantum.run import checkpoint, fingerprint


class TestQuantumNumerics(unittest.TestCase):
    def test_sparse_structure_matches_independent_stencil(self):
        x, dx, h = hamiltonian(15, 4)
        self.assertTrue(issparse(h))
        self.assertEqual(h.nnz, 3 * 15 - 2)
        np.testing.assert_allclose(h.toarray(), h.toarray().T)
        function = x**2 - 16  # zero at both boundaries
        np.testing.assert_allclose(h @ function, -np.ones(15) + 0.5 * x**2 * function)

    def test_analytic_recurrence(self):
        x = np.linspace(-2, 2, 11)
        psi = analytic_wavefunctions(x, 3)
        ground = np.pi**(-0.25) * np.exp(-x*x/2)
        np.testing.assert_allclose(psi[:, 0], ground)
        np.testing.assert_allclose(psi[:, 1], np.sqrt(2)*x*ground)
        np.testing.assert_allclose(psi[:, 2], (2*x*x-1)/np.sqrt(2)*ground, atol=1e-15)

    def test_spectrum_normalization_residual_and_convergence(self):
        reports = [solve(n, 6, 4)[3] for n in (63, 127, 255)]
        for report in reports:
            self.assertLess(max(report['scaled_residuals']), 1e-9)
            self.assertLess(report['orthogonality_error'], 1e-12)
            np.testing.assert_allclose(report['normalizations'], np.ones(4), atol=1e-12)
        self.assertLess(max(reports[-1]['relative_energy_errors']), 0.001)
        for coarse, fine in zip(reports, reports[1:]):
            ratio = np.array(coarse['absolute_energy_errors']) / fine['absolute_energy_errors']
            self.assertTrue(np.all((ratio > 3.9) & (ratio < 4.2)))

    def test_checkpoints_resume_reject_wrong_code_and_corrupt_arrays(self):
        config = Config(grid_points=127, states=2, half_width=6)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'grid-127.npz'
            identity = fingerprint(config)
            first = checkpoint(path, identity, 127, 6, 2)
            second = checkpoint(path, identity, 127, 6, 2)
            self.assertTrue(second[3]['resumed'])
            np.testing.assert_allclose(first[1], second[1])
            with self.assertRaisesRegex(ValueError, 'differ'):
                checkpoint(path, 'different-code', 127, 6, 2)
            np.savez(path, metadata=json.dumps({'fingerprint': identity, 'n': 127, 'width': 6, 'states': 2}),
                     x=first[0], energies=first[1], psi=np.zeros((127, 2)))
            with self.assertRaisesRegex(ValueError, 'numerical validation'):
                checkpoint(path, identity, 127, 6, 2)

    @unittest.skipUnless(os.environ.get('GITHUB_ACTIONS') == 'true', 'integration calculation runs in cloud only')
    def test_cloud_cli_results_and_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, '-m', 'quantum.run', '--grid-points', '511',
                       '--half-width', '6', '--states', '2', '--output', directory]
            for attempt in range(2):
                environment = os.environ.copy()
                environment.pop('GITHUB_STEP_SUMMARY', None)
                result = subprocess.run(command, capture_output=True, text=True, timeout=60, env=environment)
                self.assertEqual(result.returncode, 0, result.stderr)
                folder = Path(directory)
                summary = json.loads((folder / 'summary.json').read_text())
                self.assertTrue(summary['validation']['passed'])
                self.assertEqual(summary['finest']['resumed'], attempt == 1)
                self.assertEqual(json.loads((folder / 'status.json').read_text())['status'], 'completed')
                for name in ('spectrum.png', 'convergence.png', 'energies.csv', 'wavefunctions.npz',
                             'manifest.json', 'parameters.json', 'resource_plan.json'):
                    self.assertGreater((folder / name).stat().st_size, 0)


if __name__ == '__main__':
    unittest.main()
