import sys
import numpy as np
sys.path.insert(0, "/home/claude/E67/src")
from e65_holo import *
from e67_particula import *
X, L, pr = rede(40, 46); N = len(X); c = L / 2 + np.array([0.25, 0.1])
X0, P0, _ = vacuo(N, pr, np.ones(len(pr)), 0.0)
ds = np.arange(0, 12.01, 0.5)
def mapa_peq(Xs, Ps, rhos):
    out = []
    for d in ds:
        x0 = c + np.array([d, 0.0])
        out.append([entropia_gauge(Xs, Ps, disco(X, L, x0, r))[0] - entropia_gauge(X0, P0, disco(X, L, x0, r))[0] for r in rhos])
    return np.array(out)
for w in (3.0, 4.0):
    f = modo_chapeu(X, L, c, w); Xs, Ps = aperta(X0, P0, f, 0.5)
    M = mapa_peq(Xs, Ps, (1.0, 1.5))
    print(f"apertado w={w}: max |dS| discos pequenos (rho 1 e 1,5) por d:", np.round(np.abs(M).max(1), 4).tolist())
R = 4 * np.sqrt(2)
Xp, Pp, _ = vacuo(N, pr, kappa_padrao(X, L, pr, c, R, 0.25), 0.0)
M = mapa_peq(Xp, Pp, (1.0, 1.5))
print(f"padrão de relações R={R:.2f}: max |dS| discos pequenos por d:", np.round(np.abs(M).max(1), 4).tolist())
rhos = np.arange(0.5, 16.01, 0.5)
dSc = [entropia_gauge(Xp, Pp, disco(X, L, c, r))[0] - entropia_gauge(X0, P0, disco(X, L, c, r))[0] for r in rhos]
print("padrão centrado max |dS|:", round(max(abs(np.array(dSc))), 4))
for rs in (0.25, 0.5):
    f = modo_chapeu(X, L, c, 4.0); Xs, Ps = aperta(X0, P0, f, rs)
    dS = np.array([entropia_gauge(Xs, Ps, disco(X, L, c, r))[0] - entropia_gauge(X0, P0, disco(X, L, c, r))[0] for r in rhos])
    print(f"w=4 r={rs}: centroide {np.sum(rhos*np.abs(dS))/np.sum(np.abs(dS)):.2f}  max {np.abs(dS).max():.4f}")
