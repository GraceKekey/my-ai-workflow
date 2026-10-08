import sys, time
import numpy as np
from scipy.linalg import eigh
sys.path.insert(0, "/home/claude/E67/src")
from e65_holo import *
from e67_particula import *
X, L, pr = rede(40, 46); N = len(X); c = L / 2 + np.array([0.25, 0.1])
X0, P0, _ = vacuo(N, pr, np.ones(len(pr)), 0.0)
K = np.zeros((N, N)); a, b = pr[:, 0], pr[:, 1]; w_ = W_E * np.ones(len(pr))
np.add.at(K, (a, a), w_); np.add.at(K, (b, b), w_); np.add.at(K, (a, b), -w_); np.add.at(K, (b, a), -w_); Kt = K / M_N
rhos = np.arange(0.5, 16.01, 0.5)
S0 = np.array([entropia_gauge(X0, P0, disco(X, L, c, r))[0] for r in rhos])
rn = np.sqrt((minimg(X - c, L) ** 2).sum(1))
for w in (1.5, 2.0, 3.0, 4.0):
    for rs in (0.5, 1.0):
        f = modo_chapeu(X, L, c, w); Xs, Ps = aperta(X0, P0, f, rs)
        dS = np.array([entropia_gauge(Xs, Ps, disco(X, L, c, r))[0] for r in rhos]) - S0
        e = energia_local(Kt, Xs - X0, Ps - P0); o = np.argsort(rn); cum = np.cumsum(e[o]) / e.sum()
        r50 = rn[o][np.searchsorted(cum, 0.5)]
        k = np.argmax(np.abs(dS))
        print(f"w={w} r={rs} E={e.sum():.3f} r50={r50:.2f} pico rho={rhos[k]} dSmax={dS[k]:.4f}")
        print("   dS:", np.round(dS, 4).tolist(), flush=True)
