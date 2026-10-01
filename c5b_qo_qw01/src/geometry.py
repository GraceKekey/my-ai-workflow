"""Morris–Thorne fornecido: convenção (-,+,+,+), r areal, unidades SI."""
import math
from functools import lru_cache
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from prem_adapter import G, C, M

STRESS = C**4/(8*np.pi*G)
F_VALUES = [0., 1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
ALPHA_BASE = [1.01, 1.1, 1.5, 2., 5., 10., 100.]
ALPHA_MIN_SWITCH = brentq(lambda a: 4*a**3+13*a**2-2*a-24, 1., 1.5)
ALPHA_REFINED = sorted(set(ALPHA_BASE+[1.001, 1.005, 1.99, 2.01] +
                            [ALPHA_MIN_SWITCH*v for v in [.99, 1., 1.01]]))


def parameters(f, alpha):
    if not (f > 0 and alpha > 1):
        raise ValueError("Família atravessável requer f>0 e alpha>1.")
    mu = G*f*M/C**2
    return mu, alpha*mu


def isolated(y, alpha):
    """Forma adimensional estável, inclusive y=1; curvatura escalada por r0."""
    y = np.asarray(y, dtype=float)
    if alpha <= 1 or np.any(y < 1):
        raise ValueError("Não atravessar r<r0; alpha>1 para flare-out estrito.")
    s = 1-2/alpha
    A = alpha*y/(alpha*y+2)
    F = (y-1)*(y+s)/y**2
    Fy = 2/(alpha*y**2)+2*s/y**3
    phi_y = 1/(y*(alpha*y+2))
    phi_yy = -2*(alpha*y+1)/(y**2*(alpha*y+2)**2)
    k1 = F*(phi_yy+phi_y**2)+.5*Fy*phi_y
    k2 = F*phi_y/y
    k3 = -.5*Fy/y
    k4 = 2/(alpha*y**3)+s/y**4
    # Expressões reduzidas: não subtrair termos O(1/y³) para obter O(1/y⁴).
    energy = -s/y**4
    pr = -((8/alpha**2+s)*y+4*s/alpha)/(y**4*(y+2/alpha))
    nec = -2*((4/alpha**2+s)*y+3*s/alpha)/(y**4*(y+2/alpha))
    pt = k1+k2-k3
    curvature = invariants(k1, k2, k3, k4)
    return {"A": A, "F": F, "Fy": Fy, "b_r": 2/(alpha*y)+s/y**2,
            "phi_y": phi_y, "phi_yy": phi_yy,
            "g_r0_c2": np.sqrt(F)*phi_y,
            "energy_scaled": energy, "pr_scaled": pr, "pt_scaled": pt,
            "nec_scaled": nec, **curvature}


def invariants(k1, k2, k3, k4):
    r00 = k1+2*k2
    r11 = -k1+2*k3
    r22 = -k2+k3+k4
    return {"ricci_scaled": -r00+r11+2*r22,
            "ricci2_scaled": r00*r00+r11*r11+2*r22*r22,
            "kretsch_scaled": 4*(k1*k1+2*k2*k2+2*k3*k3+k4*k4)}


@lru_cache(maxsize=40)
def nec_minimum(alpha):
    # NEC<0 em toda a boca. Para alpha pequeno o mínimo fica fora da garganta.
    opt = minimize_scalar(lambda z: float(isolated(np.exp(z), alpha)["nec_scaled"]),
                          bounds=(0., math.log(100.)), method="bounded")
    candidates = [(float(isolated(1., alpha)["nec_scaled"]), 1.),
                  (opt.fun, float(np.exp(opt.x)))]
    return min(candidates)


@lru_cache(maxsize=80)
def negative_nec_budget(alpha, epsrel=1e-10):
    """-∫ NEC dV/(4 pi STRESS r0), uma boca até infinito; NÃO é ANEC."""
    s = 1-2/alpha
    def integrand(z):
        y = 1+z*z
        # y=1+z² remove a singularidade integrável do volume próprio na garganta.
        return -2*float(isolated(y, alpha)["nec_scaled"])*y**3/math.sqrt(y+s)
    value, error = quad(integrand, 0., np.inf, epsabs=1e-10, epsrel=epsrel, limit=200)
    return value, error


@lru_cache(maxsize=40)
def negative_energy_budget(alpha):
    """Energia negativa de E_W; zero para 1<alpha<=2, distinta da NEC."""
    s = 1-2/alpha
    if s <= 0:
        return 0.
    value = quad(lambda z: 2*s/((1+z*z)*math.sqrt(1+z*z+s)),
                 0., np.inf, epsabs=1e-11, epsrel=1e-10)[0]
    return value
