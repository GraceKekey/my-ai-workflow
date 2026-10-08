"""expoente de δS em discos pequenos: estado (aperto suave) × fonte (padrão de relações) × excitação de rede (V+)."""
import sys
import numpy as np
sys.path.insert(0, "/home/claude/E67/src")
from e65_holo import *
from e67_particula import *
X, L, pr = rede(48, 56); N = len(X); c = L / 2 + np.array([0.25, 0.1])
X0, P0, _ = vacuo(N, pr, np.ones(len(pr)), 0.0)
rp = np.array([1.0, 1.5, 2.0, 2.5, 3.0])
def perfil_peq(Xs, Ps, x0):
    return np.array([entropia_gauge(Xs, Ps, disco(X, L, x0, r))[0] - entropia_gauge(X0, P0, disco(X, L, x0, r))[0] for r in rp])
def expo(d):
    d = np.abs(d); m = d > 1e-12
    return np.polyfit(np.log(rp[m]), np.log(d[m]), 1)[0] if m.sum() >= 3 else np.nan
for w in (4.0, 6.0):
    for rs in (0.1, 0.25):
        f = modo_chapeu(X, L, c, w); Xs, Ps = aperta(X0, P0, f, rs)
        for frac in (0.0, 0.5, 1.0, 1.5):
            d = perfil_peq(Xs, Ps, c + np.array([frac * w, 0.0]))
            print(f"aperto w={w} r={rs} d={frac}w: dS={np.round(d, 5).tolist()} expoente={expo(d):.2f}", flush=True)
Xp, Pp, _ = vacuo(N, pr, kappa_padrao(X, L, pr, c, 5.0, 0.25), 0.0)
for d0 in (0.0, 2.5, 5.0, 7.5):
    d = perfil_peq(Xp, Pp, c + np.array([d0, 0.0]))
    print(f"padrão R=5 d={d0}: dS={np.round(d, 5).tolist()} expoente={expo(d):.2f}")
Xu, Pu, _ = unitario_gauge(X0, P0, X, L, pr, c, 5.0, r_sq=0.25)
for d0 in (0.0, 2.5):
    d = perfil_peq(Xu, Pu, c + np.array([d0, 0.0]))
    print(f"V+ d={d0}: dS={np.round(d, 5).tolist()} expoente={expo(d):.2f}")
