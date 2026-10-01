"""Referência TOV com densidade PREM prescrita e extensão geométrica declarada."""
from functools import lru_cache
import numpy as np
from scipy.integrate import solve_ivp, cumulative_simpson
from prem_adapter import prem, G, C, M, R
from geometry import isolated, invariants, STRESS

PSTAR = G*M*M/R**4
EPS = G*M/(R*C*C)
RHOSTAR = M/R**3
RHOC = float(prem.density(0))
SAMPLES = {"surface": R, "0_9R": .9*R, "0_75R": .75*R, "0_5R": .5*R,
           "0_25R": .25*R, "0_1R": .1*R, "100km": 1e5, "1000km": 1e6}


class EarthReference:
    def __init__(self, f, rtol=2e-11):
        self.f = f
        self.parts = []
        self.intervals = []
        state = [0., .5*np.log1p(-2*EPS*(1-f))/EPS]
        for lo, hi, coeff in reversed(prem.LAYERS):
            start = max(lo*1000, 1e-14)
            t_hi, t_lo = np.log(hi*1000/R), np.log(start/R)
            def rhs(t, v):
                r = R*np.exp(t)
                x = r/R
                rho = (1-f)*1000*prem.NORMALIZATION*np.polynomial.polynomial.polyval(x, coeff)
                m = (1-f)*float(prem.mass(r))/M
                F = 1-2*EPS*m/x
                q, psi = v
                dpsi = (m+4*np.pi*EPS*x**3*q)/(x*F)
                return [-(rho/RHOSTAR+EPS*q)*dpsi, dpsi]
            sol = solve_ivp(rhs, (t_hi, t_lo), state, method="DOP853", rtol=rtol,
                            atol=[2e-13, 2e-13], max_step=1., dense_output=True)
            if not sol.success:
                raise RuntimeError("TOV PREM: "+sol.message)
            self.parts.append(sol.sol)
            self.intervals.append((t_lo, t_hi))
            state = sol.y[:, -1]

    def evaluate(self, r):
        r = np.atleast_1d(np.asarray(r, dtype=float))
        p = np.zeros_like(r)
        phi = np.zeros_like(r)
        inside = r <= R
        t = np.log(np.maximum(r, 1e-14)/R)
        for func, (lo, hi) in zip(self.parts, self.intervals):
            mask = inside & (t >= lo) & (t <= hi)
            if np.any(mask):
                q, psi = func(t[mask])
                p[mask] = q*PSTAR
                phi[mask] = psi*EPS
        if np.any(~inside):
            phi[~inside] = .5*np.log1p(-2*G*(1-self.f)*M/(C*C*r[~inside]))
        rho = (1-self.f)*prem.density(r)
        rho = np.where(inside, rho, 0.)
        m = (1-self.f)*prem.mass(r)
        b = 2*G*m/C**2
        F = 1-b/r
        mp = 4*np.pi*r*r*rho
        Fp = -2*G/C**2*(mp/r-m/r**2)
        numerator = G/C**2*(m+4*np.pi*r**3*p/C**2)
        phip = numerator/(r*r*F)
        pp = -(rho*C*C+p)*phip
        numerator_p = G/C**2*(mp+12*np.pi*r*r*p/C**2+4*np.pi*r**3*pp/C**2)
        phipp = numerator_p/(r*r*F)-phip*(2/r+Fp/F)
        return {"p": p, "phi": phi, "phip": phip, "phipp": phipp,
                "rho": rho, "m": m, "b": b, "F": F, "Fp": Fp}


@lru_cache(maxsize=20)
def reference(f):
    return EarthReference(f)


def composed(r, f, alpha, r0):
    r = np.atleast_1d(np.asarray(r, dtype=float))
    if np.any(r < r0):
        raise ValueError("r<r0 excluído")
    earth = reference(f).evaluate(r)
    hole = float(prem.mass(r0))
    norm = (1-f)/(1-hole/M)
    mm = norm*(prem.mass(r)-hole)
    rho = norm*prem.density(r)
    rho = np.where(r <= R, rho, 0.)
    be = 2*G*mm/C**2
    bep = 8*np.pi*G*r*r*rho/C**2
    if f == 0:
        W = {key: np.zeros_like(r) for key in ["phi_y", "phi_yy", "b_r", "nec_scaled", "pr_scaled", "energy_scaled"]}
        phiW, phipW, phippW = np.zeros_like(r), np.zeros_like(r), np.zeros_like(r)
        bw, bwp = np.zeros_like(r), np.zeros_like(r)
        Fw = np.ones_like(r)
    else:
        y = r/r0
        W = isolated(y, alpha)
        phiW = -.5*np.log1p(2*G*f*M/(C*C*r))
        phipW, phippW = W["phi_y"]/r0, W["phi_yy"]/r0**2
        bw = r*W["b_r"]
        bwp = -(1-2/alpha)/y**2
        Fw = W["F"]
    F = Fw-be/r
    if np.any(F < 0):
        raise RuntimeError("Assinatura não lorentziana na boca composta")
    Fp = (bw+be)/r**2-(bwp+bep)/r
    phip = phipW+earth["phip"]
    phipp = phippW+earth["phipp"]
    phi = phiW+earth["phi"]
    k1 = F*(phipp+phip**2)+.5*Fp*phip
    k2 = F*phip/r
    k3 = -.5*Fp/r
    k4 = (bw+be)/r**3
    cv = invariants(k1, k2, k3, k4)
    # 'scaled' é nome comum do helper; aqui os argumentos já têm unidades m^-2.
    curvature = {"Ricci_m2": cv["ricci_scaled"], "Ricci2_m4": cv["ricci2_scaled"],
                 "Kretsch_m4": cv["kretsch_scaled"]}
    if f:
        ew = STRESS/r0**2*W["energy_scaled"]
        prw = STRESS/r0**2*W["pr_scaled"]
        necw = STRESS/r0**2*W["nec_scaled"]
    else:
        ew, prw, necw = np.zeros_like(r), np.zeros_like(r), np.zeros_like(r)
    db = earth["b"]-be
    cross = -2*STRESS*(be*phipW+bw*earth["phip"])/r**2
    cavity = STRESS*db*(1/r**3-2*earth["phip"]/r**2)
    prtotal = prw+earth["p"]+cross+cavity
    return {"r": r, "rho": rho, "m_matter": mm, "phi": phi, "F": F,
            "A": np.exp(2*phi), "b_r": 1-F, "g": C*C*np.sqrt(F)*phip,
            "gW_isolated": np.zeros_like(r) if not f else C*C/r0*W["g_r0_c2"],
            "phip": phip, "phipW": phipW, "phiE_p": earth["phip"],
            "P_E": earth["p"], "rho_E": earth["rho"],
            "energy_W_J_m3": ew, "pr_W_Pa": prw,
            "pt_total_Pa": STRESS*(k1+k2-k3), "pr_total_Pa": prtotal,
            "energy_total_J_m3": ew+rho*C*C,
            "NEC_W_Pa": necw, "NEC_total_Pa": necw+rho*C*C+earth["p"]+cross+cavity,
            "NEC_exotic_without_deltaP_Pa": necw+cross+cavity,
            **curvature}


def profile(f, alpha=None, resolution=650):
    r0 = 0. if not f else alpha*G*f*M/C**2
    minimum = 1e-6 if not f else r0
    chunks = []
    delta_top = 0.
    for lo, hi, coeff in reversed(prem.LAYERS):
        a, b = max(minimum, lo*1000), hi*1000
        if a >= b:
            continue
        n = max(30, int(resolution*(b-a)/R)+int(resolution/18*np.log(b/a)))
        extras = [v for v in SAMPLES.values() if a < v < b]
        if a == minimum and f:
            extras += list(r0*(1+np.geomspace(1e-12, 1, 70)))
            extras += list(r0*np.geomspace(1, 100, 140))
        rr = np.unique(np.r_[np.geomspace(a, b, n), np.linspace(a, b, n), extras])
        rr = rr[(rr >= a) & (rr <= b)]
        geo = composed(rr, f, alpha, r0)
        rho = (1-f)/(1-float(prem.mass(r0))/M)*1000*prem.NORMALIZATION*\
              np.polynomial.polynomial.polyval(rr/R, coeff)
        # Integra ΔP=P-P_E, evitando subtrair pressões quase iguais no campo fraco.
        rho_E_local = (1-f)*1000*prem.NORMALIZATION*\
                      np.polynomial.polynomial.polyval(rr/R, coeff)
        source = ((rho/RHOC+geo["P_E"]/(RHOC*C*C))*rr*geo["phipW"] +
                  (rho-rho_E_local)/RHOC*rr*geo["phiE_p"])*np.exp(geo["phi"])
        integ = cumulative_simpson(source[::-1], x=-np.log(rr)[::-1], initial=0.)[::-1]
        delta = np.exp(-geo["phi"])*(integ+delta_top*np.exp(geo["phi"][-1]))
        delta_top = float(delta[0])
        geo["deltaP_Pa"] = delta*RHOC*C*C
        geo["P_Pa"] = geo["P_E"]+geo["deltaP_Pa"]
        geo["NEC_exotic_Pa"] = geo["NEC_exotic_without_deltaP_Pa"]-geo["deltaP_Pa"]
        chunks.append(geo)
    chunks.reverse()
    return {key: np.concatenate([piece[key] if i == 0 else piece[key][1:]
                                 for i, piece in enumerate(chunks)]) for key in chunks[0]}


def pressure_ode(f, alpha):
    """Validação independente da hidrostática linear, sem quadratura de Simpson."""
    r0 = alpha*G*f*M/C**2
    state = [0.]
    for lo, hi, coeff in reversed(prem.LAYERS):
        a, b = max(r0, lo*1000), hi*1000
        def rhs(t, q):
            # exp(log(r0)) pode arredondar alguns ulps abaixo do limite exato.
            r = max(r0, np.exp(t))
            geo = composed([r], f, alpha, r0)
            rho = (1-f)/(1-float(prem.mass(r0))/M)*1000*prem.NORMALIZATION*\
                  np.polynomial.polynomial.polyval(r/R, coeff)
            return [-(rho/RHOC+q[0])*r*float(geo["phip"][0])]
        sol = solve_ivp(rhs, (np.log(b), np.log(a)), state, method="DOP853",
                        rtol=2e-11, atol=1e-22, max_step=.6)
        if not sol.success:
            raise RuntimeError(sol.message)
        state = sol.y[:, -1]
    return state[0]*RHOC*C*C
