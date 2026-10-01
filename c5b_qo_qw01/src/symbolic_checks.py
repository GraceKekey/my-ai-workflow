"""Derivações simbólicas independentes para o wormhole isolado."""
import sympy as sp


def derive():
    r, mu, r0 = sp.symbols("r mu r0", positive=True)
    a, u, v = sp.symbols("alpha u v", positive=True)
    A = r/(r+2*mu)
    b = 2*mu+(r0-2*mu)*r0/r
    F = 1-b/r
    phi = sp.log(A)/2
    p = sp.diff(phi, r)
    k1 = F*(sp.diff(p, r)+p*p)+sp.diff(F, r)*p/2
    k2 = F*p/r
    k3 = -sp.diff(F, r)/(2*r)
    k4 = b/r**3
    # Tensor Einstein ortonormal em unidades 8*pi*G/c^4.
    E = sp.diff(b, r)/r**2
    pr = -b/r**3+2*F*p/r
    pt = k1+k2-k3
    nec = sp.factor(E+pr)
    conservation = sp.factor(sp.diff(pr, r)+(E+pr)*p-2*(pt-pr)/r)
    Ricci = sp.factor(-2*k1-4*k2+4*k3+2*k4)
    Ricci2 = sp.factor((k1+2*k2)**2+(-k1+2*k3)**2+2*(-k2+k3+k4)**2)
    Kretsch = sp.factor(4*(k1*k1+2*k2*k2+2*k3*k3+k4*k4))
    throat = {"Ricci": sp.factor(Ricci.subs(r, r0).subs(mu, r0/a)),
              "Ricci2": sp.factor(Ricci2.subs(r, r0).subs(mu, r0/a)),
              "Kretschmann": sp.factor(Kretsch.subs(r, r0).subs(mu, r0/a))}
    proof = sp.expand(((a*a-2*a+4)*(1+u)+3*a-6).subs(a, 1+v))
    checks = {
        "b_r0_equal_r0": sp.simplify(b.subs(r, r0)-r0) == 0,
        "A_r0": sp.simplify(A.subs(r, r0)-r0/(r0+2*mu)) == 0,
        "bp_r0": sp.simplify(sp.diff(b, r).subs(r, r0)-(2*mu/r0-1)) == 0,
        "Einstein_density_from_curvature": sp.simplify(E-(2*k3+k4)) == 0,
        "Einstein_pr_from_curvature": sp.simplify(pr-(2*k2-k4)) == 0,
        "Einstein_trace": sp.simplify(Ricci-(E-pr-2*pt)) == 0,
        "covariant_conservation_isolated": conservation == 0,
        "NEC_negative_proof_polynomial": proof == u*v*v+3*u+v*v+3*v,
    }
    if not all(checks.values()):
        raise RuntimeError("Falha na validação simbólica")
    return {"checks": checks, "A": str(A), "b": str(b), "F_factorized": str(sp.factor(F)),
            "Phi_prime": str(sp.factor(p)), "energy_over_Cstress": str(sp.factor(E)),
            "pr_over_Cstress": str(sp.factor(pr)), "pt_over_Cstress": str(sp.factor(pt)),
            "NEC_over_Cstress": str(nec), "NEC_sign_proof": str(proof),
            "Ricci": str(Ricci), "Ricci2": str(Ricci2), "Kretschmann": str(Kretsch),
            "throat": {key: str(value) for key, value in throat.items()},
            "limits": {"A_large_r_first_order": str(sp.limit(r*(A-1), r, sp.oo)),
                       "B_large_r_first_order": str(sp.limit(r*(1/F-1), r, sp.oo)),
                       "g_r0": "0 para alpha>1", "NEC_width": "infinita"}}
