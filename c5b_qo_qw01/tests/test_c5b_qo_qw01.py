import hashlib
import io
import json
from pathlib import Path
import sys
import unittest

import numpy as np
from scipy.integrate import quad
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from prem_adapter import prem, verify_source, source_hash, G, C, M, R
from geometry import isolated, parameters, negative_nec_budget, negative_energy_budget, invariants, ALPHA_BASE
from earth import profile, composed, reference, pressure_ode
from symbolic_checks import derive


def code_hashes():
    files = list((ROOT/"src").glob("*.py"))+list((ROOT/"tests").glob("*.py"))+[ROOT/"requirements.txt"]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}


class WormholeTests(unittest.TestCase):
    def test_01_mass_conservation(self):
        verify_source()
        # Quadratura independente do perfil anterior, com limites de camada.
        total = sum(quad(lambda r: 4*np.pi*r*r*1000*prem.NORMALIZATION*
                    np.polynomial.polynomial.polyval(r/R, a), lo*1000, hi*1000)[0]
                    for lo, hi, a in prem.LAYERS)
        self.assertAlmostEqual(total/M, 1., places=13)
        for f in [1e-10, 1e-6, 1e-3]:
            for alpha in ALPHA_BASE:
                _, r0 = parameters(f, alpha)
                mm = composed([R], f, alpha, r0)["m_matter"][0]
                self.assertAlmostEqual((mm+f*M)/M, 1., places=13)

    def test_02_throat(self):
        for a in ALPHA_BASE:
            w = isolated(1., a)
            self.assertAlmostEqual(float(w["b_r"]), 1., places=14)
            self.assertEqual(float(w["F"]), 0.)

    def test_03_flare_out(self):
        for a in ALPHA_BASE:
            self.assertLess(2/a-1, 1.)
        with self.assertRaises(ValueError):
            parameters(1e-8, 1.)

    def test_04_no_horizon(self):
        for a in ALPHA_BASE:
            self.assertGreater(float(isolated(1., a)["A"]), 0.)
            self.assertTrue(np.all(isolated(np.geomspace(1.000001, 1e8, 100), a)["F"] > 0))

    def test_05_asymptotic(self):
        for a in ALPHA_BASE:
            y = 1e8
            w = isolated(y, a)
            ratio = a*y*y*float(w["g_r0_c2"])
            self.assertLess(abs(ratio-1), 4e-8)
            self.assertLess(abs(float(w["A"])-(1-2/(a*y))), 1e-14)

    def test_06_f_zero_PREM(self):
        p = profile(0., resolution=400)
        self.assertTrue(np.all(p["deltaP_Pa"] == 0))
        for r in [1e5, 1e6, R/2, R]:
            g = composed([r], 0., None, 0.)["g"][0]
            self.assertLess(abs(g/float(prem.gravity(r))-1), 1e-8)
        baseline = reference(0.).evaluate([1e-6])["p"][0]
        self.assertLess(abs(baseline/prem.pressure_integral(0, 0)-1), 1e-8)

    def test_07_convergence(self):
        for f, a in [(1e-10, 1.01), (1e-8, 2.), (1e-3, 100.)]:
            p = profile(f, a, 650)
            fine = profile(f, a, 1300)
            self.assertLess(abs(p["P_Pa"][0]/fine["P_Pa"][0]-1), 2e-6)
            ode = pressure_ode(f, a)
            self.assertLess(abs(ode/fine["P_Pa"][0]-1), 2e-6)

    def test_08_finite_domain(self):
        p = profile(1e-8, 1.01, 400)
        for name, values in p.items():
            self.assertTrue(np.isfinite(values).all(), name)
        with self.assertRaises(ValueError):
            isolated(.999, 2.)

    def test_09_curvature_throat_finite(self):
        for a in ALPHA_BASE:
            w = isolated(np.array([1., 1+1e-9, 2.]), a)
            for key in ["ricci_scaled", "ricci2_scaled", "kretsch_scaled"]:
                self.assertTrue(np.isfinite(w[key]).all())
                self.assertLess(abs(w[key][1]-w[key][0]), 1e-6)
            self.assertEqual(float(w["g_r0_c2"][0]), 0.)

    def test_10_symbolic_and_conservation(self):
        d = derive()
        self.assertTrue(all(d["checks"].values()))
        (ROOT/"report").mkdir(exist_ok=True)
        (ROOT/"report/symbolic_derivations.json").write_text(json.dumps(d, indent=2), encoding="utf-8")

    def test_11_NEC_and_volume(self):
        for a in ALPHA_BASE:
            self.assertTrue(np.all(isolated(np.geomspace(1, 1e10, 150), a)["nec_scaled"] < 0))
            value, error = negative_nec_budget(a)
            self.assertGreater(value, 0.)
            self.assertLess(error/value, 1e-7)

    def test_12_negative_energy_not_same_as_NEC(self):
        self.assertEqual(negative_energy_budget(1.5), 0.)
        self.assertEqual(negative_energy_budget(2.), 0.)
        self.assertGreater(negative_energy_budget(5.), 0.)

    def test_13_invariants_Schwarzschild_known_result(self):
        mu, r = 3., 20.
        t = mu/r**3
        values = invariants(-2*t, t, -t, 2*t)
        self.assertAlmostEqual(values["ricci_scaled"], 0., places=14)
        self.assertAlmostEqual(values["ricci2_scaled"], 0., places=14)
        self.assertAlmostEqual(values["kretsch_scaled"], 48*mu*mu/r**6, places=14)


if __name__ == "__main__":
    capture = io.StringIO()
    result = unittest.TextTestRunner(stream=capture, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(WormholeTests))
    print(capture.getvalue())
    (ROOT/"results").mkdir(exist_ok=True)
    (ROOT/"results/test_log.txt").write_text(capture.getvalue(), encoding="utf-8")
    (ROOT/"results/test_results.json").write_text(json.dumps({"passed": result.wasSuccessful(),
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "code_hashes": code_hashes(), "prem_sha256": source_hash()}, indent=2), encoding="utf-8")
    sys.exit(0 if result.wasSuccessful() else 1)
