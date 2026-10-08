import sys
import numpy as np
sys.path.insert(0, "/home/claude/E67/src")
from e65_holo import *
from e67_particula import *
X, L, pr = rede(64, 74); N = len(X); c = L / 2 + np.array([0.25, 0.1])
X0, P0, _ = vacuo(N, pr, np.ones(len(pr)), 0.0)
rp = np.array([1.0, 1.5, 2.0, 2.5, 3.0]); rhos = np.arange(0.5, 24.01, 0.5)
S0 = np.array([entropia_gauge(X0, P0, disco(X, L, c, r))[0] for r in rhos])
for w in (4.0, 5.0, 6.0, 7.0):
    f = modo_chapeu(X, L, c, w); Xs, Ps = aperta(X0, P0, f, 0.25); ps = []
    for fr in (0.5, 1.0, 1.5):
        x0 = c + np.array([fr * w, 0.0])
        d = np.array([entropia_gauge(Xs, Ps, disco(X, L, x0, r))[0] - entropia_gauge(X0, P0, disco(X, L, x0, r))[0] for r in rp])
        m = np.abs(d) > 1e-12; ps.append(np.polyfit(np.log(rp[m]), np.log(np.abs(d[m])), 1)[0])
    dS = np.array([entropia_gauge(Xs, Ps, disco(X, L, c, r))[0] for r in rhos]) - S0
    mw = rhos <= 3 * w; zc = (rhos[mw] * np.abs(dS[mw])).sum() / np.abs(dS[mw]).sum()
    e = energia_local(ktil(N, pr, np.ones(len(pr))), Xs - X0, Ps - P0)
    print(f"w={w}: p {np.round(ps, 2).tolist()} min {min(ps):.2f} | z(≤3w) {zc:.2f} z/w {zc/w:.3f} | r50 {raio_metade(X, L, c, e):.2f} | E {e.sum():.4f}", flush=True)
