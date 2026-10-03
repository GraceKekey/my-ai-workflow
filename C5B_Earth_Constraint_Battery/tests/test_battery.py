import sys,unittest,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core import *
from stages import slichter_benchmark,travel_removed

class ScientificControls(unittest.TestCase):
    def test_prem_provenance(self):self.assertEqual(verify_prem(),PARAMS['expected_PREM_sha256'])
    def test_report_regression(self):
        r=json.loads((ROOT/'results/regression_QW02.json').read_text());self.assertTrue(r['passed']);self.assertEqual(len(r['cases']),18)
    def test_mass_numeric_cavity(self):
        f,rc=1e-4,137567.;n=norm(f,rc)
        val=sum(quad(lambda r:4*np.pi*n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(r/R,co)*r*r,max(lo*1000,rc),hi*1000,epsrel=1e-11)[0] for lo,hi,co in prem.LAYERS if hi*1000>rc)
        self.assertLess(abs((val+f*M)/M-1),2e-14)
    def test_inertia_numeric(self):
        f,rc=1e-3,1153685.;n=norm(f,rc)
        val=sum(quad(lambda r:8*np.pi/3*n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(r/R,co)*r**4,max(lo*1000,rc),hi*1000,epsrel=1e-11)[0] for lo,hi,co in prem.LAYERS if hi*1000>rc)
        self.assertLess(abs(val/(n*(I0-inertia_below(rc)))-1),2e-14)
    def test_control_zero(self):
        rr=np.geomspace(1.,R,70);a=geometry(rr,0.,0.,'open');b=geometry(rr,0.,0.,'closed')
        self.assertTrue(np.array_equal(a['g'],b['g']));self.assertTrue(np.array_equal(a['m'],prem.mass(rr)))
        self.assertLess(np.max(abs(a['g']/prem.gravity(rr)-1)),2e-8)
    def test_control_small(self):
        ds=[]
        for f in [1e-10,1e-11,1e-12]:
            rc=cavity_threshold(f,.01)['rc_m'];ds.append(abs(geometry([1e5],f,rc)['g'][0]/geometry([1e5],0.,0.)['g'][0]-1))
        self.assertGreater(ds[0],ds[1]);self.assertGreater(ds[1],ds[2]);self.assertLess(ds[2],2e-7)
    def test_asymptotic_gravity(self):
        for state in ['open','closed']:
            f=1e-8;mu=G*f*M/C**2;rr=mu*1e7
            p=mu/(rr*(rr+(2*mu if state=='open' else -2*mu)))
            g=C*C*np.sqrt(1-2*mu/rr)*p
            self.assertLess(abs(g/(G*f*M/rr**2)-1),4e-7)
    def test_horizon_guard(self):
        f=1e-8;r0=2*G*f*M/C**2
        with self.assertRaises(ValueError):pressure(f,r0,'closed')
        with self.assertRaises(ValueError):geometry([r0/2],f,r0,'open')
    def test_pressure_quadrature_independent(self):
        f=1e-6;rc=cavity_threshold(f,.01)['rc_m'];p,d=pressure_newton(f,rc)
        n=norm(f,rc);hole=float(prem.mass(rc));v=0.
        for lo,hi,co in prem.LAYERS:
            a,b=max(rc,lo*1000),hi*1000
            if a>=b:continue
            v+=quad(lambda t:n*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(np.exp(t)/R,co)*G*(f*M+n*(float(prem.mass(np.exp(t)))-hole))/np.exp(t),np.log(a),np.log(b),epsrel=2e-10)[0]
        self.assertLess(abs((p+d)/v-1),2e-11)
    def test_pressure_weak_GR(self):
        f=1e-6;rc=cavity_threshold(f,.01)['rc_m'];p,d=pressure(f,rc);pn,dn=pressure_newton(f,rc)
        self.assertLess(abs(p/(pn+dn)-1),2e-8)
    def test_numerical_step_convergence(self):
        f=1e-8;r0=2*G*f*M/C**2
        p1,_=pressure(f,2*r0,'closed',rtol=2e-9);p2,_=pressure(f,2*r0,'closed',rtol=2e-11)
        self.assertLess(abs(p1/p2-1),1e-8)
    def test_finite_micro_open(self):
        f=1e-8;r0=2*G*f*M/C**2;p,_=pressure(f,r0,'open');x=geometry([r0],f,r0,'open')
        self.assertTrue(np.isfinite(p));self.assertEqual(float(x['g'][0]),0.);self.assertGreater(float(x['A'][0]),0.)
    def test_cavity_pressure_floor(self):
        f=.001;self.assertIsNone(cavity_threshold(f,.001)['rc_m'])
        for rc in [1e3,1e5,1e6,R*.95]:
            p,d=pressure_newton(f,rc);self.assertGreater(d/p,2*f/(1-f))
    def test_slichter_benchmark(self):
        T=slichter_benchmark(13000.,12000.);self.assertTrue(2*3600<T<12*3600)
        self.assertIsNone(slichter_benchmark(11000.,12000.))
    def test_PKIKP_units(self):
        self.assertAlmostEqual(travel_removed(5.6311),.001,places=11)
    def test_isolated_open_radial_NEC(self):
        mu=1.;r=4.;F=1-2*mu/r;phip=mu/(r*(r+2*mu))
        einstein_radial=ST*((F-1)/r**2+2*F*phip/r)
        analytic=-8*ST*mu**2/(r**3*(r+2*mu))
        self.assertLess(abs(einstein_radial/analytic-1),1e-14)
        self.assertLess(analytic,0.)
    def test_closed_composed_extra_stress_required(self):
        f=1e-6;rc=cavity_threshold(f,.01)['rc_m'];p,d=pressure(f,rc,'closed');x=geometry([rc],f,rc,'closed')
        mu=G*f*M/C**2;bw=2*mu;be=2*G*x['m'][0]/C**2
        extra=-2*ST*(be*x['phiWp'][0]+bw*x['phiEp'][0])/rc**2-d
        self.assertLess(extra,0.);self.assertGreater(p,0.)

if __name__=='__main__':unittest.main()
