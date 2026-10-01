import importlib.util
import math
from pathlib import Path
import sys
import unittest

import numpy as np
from scipy.integrate import quad

spec = importlib.util.spec_from_file_location("study", Path(__file__).parents[1]/"study.py")
s = importlib.util.module_from_spec(spec)
sys.modules["study"] = s
spec.loader.exec_module(s)


class PhysicalInvariants(unittest.TestCase):
    def test_mass_independent_quadrature(self):
        m = 0.
        for lo, hi, a in s.LAYERS:
            m += quad(lambda r: 4*np.pi*r*r*1000*s.NORMALIZATION*
                      np.polynomial.polynomial.polyval(r/s.R, a), lo*1000, hi*1000)[0]
        self.assertAlmostEqual(m/s.M, 1., places=13)
        for f in s.BASE_F:
            self.assertAlmostEqual((f*s.M+(1-f)*m)/s.M, 1., places=13)

    def test_surface_and_schwarzschild(self):
        for f in s.BASE_F:
            self.assertAlmostEqual(float(s.gravity(s.R, f)), s.G*s.M/s.R**2, places=12)
        self.assertAlmostEqual(s.schwarzschild_radius(1)*1000, 8.87010287, places=5)

    def test_perturbation_identity(self):
        for r in [1e5, 1.2215e6, 3.48e6, .9*s.R]:
            g0 = s.gravity(r, 0)
            for f in [1e-6, .1, .5]:
                self.assertAlmostEqual(float((s.gravity(r, f)-g0)/g0),
                                       float(s.relative_gravity(r, f)), places=9)

    def test_uniform_sphere_pressure(self):
        # Independente do PREM: solução exata em esfera homogênea com fonte pontual.
        rho = 3*s.M/(4*np.pi*s.R**3)
        r = 100.
        for f in [0., .01, .5]:
            numerical = quad(lambda t: (1-f)*rho*s.G*
                             (f*s.M+(1-f)*s.M*(math.exp(t)/s.R)**3)/math.exp(t),
                             math.log(r), math.log(s.R), epsrel=1e-11)[0]
            exact = (1-f)*rho*s.G*f*s.M*(1/r-1/s.R) + \
                    (1-f)**2*2*np.pi/3*s.G*rho*rho*(s.R*s.R-r*r)
            self.assertAlmostEqual(numerical/exact, 1., places=10)

    def test_pressure_boundary_and_horizon(self):
        self.assertEqual(s.pressure_integral(s.R, .1), 0.)
        with self.assertRaises(ValueError):
            s.pressure_integral(s.schwarzschild_radius(.1), .1)
        with self.assertRaises(ValueError):
            s.gravity(0, .1)

    def test_polytrope_against_closed_solution(self):
        for f in [0., 1e-8, .1, .5]:
            sol = s.polytrope(f)
            self.assertLess(sol["radius_error"], 2e-8)
            self.assertLess(sol["q_error"], 2e-8)
            self.assertLess(sol["w_error"], 2e-8)
            self.assertGreater(sol["min_density"], -1e-3)

    def test_central_asymptotes(self):
        f = .01
        # ΔP(1m)-ΔP(10m) deve reproduzir o termo central 1/r.
        dp = (s.pressure_integral(1, f)-s.pressure_integral(10, f) -
              (1-f)**2*(s.pressure_integral(1, 0)-s.pressure_integral(10, 0)))
        exact = (1-f)*float(s.density(0))*s.G*f*s.M*(1-1/10)
        self.assertAlmostEqual(dp/exact, 1., places=8)
        # Mais perto da assíntota; ambos os raios continuam fora de 100 rs.
        x = np.array([.01, .1])/s.R
        _, w, _ = s.polytrope_analytic(f, x)
        self.assertAlmostEqual(float(w[0]/w[1]), 1., places=4)


if __name__ == "__main__":
    unittest.main()
