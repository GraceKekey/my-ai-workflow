"""HRF — ELETRON-67 — rodada (só executar depois do 'pode rodar'). Uso: python3 e67_rodar.py [teste]"""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e65_holo import rede, kappa_padrao, vacuo, entropia_gauge, disco, unitario_gauge
from e67_particula import modo_chapeu, aperta, ktil, energia_local, raio_metade, delta_K

TESTE = len(sys.argv) > 1 and sys.argv[1] == "teste"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pasta do pacote (acima de src/)
BASE = os.path.join(RAIZ, "teste_saida") if TESTE else RAIZ          # modo teste grava à parte
D = os.path.join(BASE, "dados"); RES = os.path.join(BASE, "resultados")
os.makedirs(D, exist_ok=True); os.makedirs(RES, exist_ok=True)
TAM = (24, 28) if TESTE else (64, 74)
WS = (2.0, 3.0) if TESTE else (4.0, 5.0, 6.0, 7.0)
RS = (0.1, 0.25)
RHOS = np.arange(0.5, (8.0 if TESTE else 24.0) + 1e-9, 0.25)
RP = np.array([1.0, 1.5, 2.0, 2.5, 3.0])            # discos pequenos
FR = (0.5, 1.0, 1.5)                                 # posições d = FR × w (ou × R); centro excluído (fumaça)
OFF_D = np.arange(0, (6 if TESTE else 16) + 1e-9, 1.0); OFF_R = np.arange(1, (6 if TESTE else 16) + 1e-9, 1.0)


def log(*a):
    with open(os.path.join(RES, "log_execucao.txt"), "a") as fh:
        fh.write(time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a) + "\n")


def geo():
    X, L, pr = rede(*TAM); c = L / 2 + np.array([0.25, 0.1]); return X, L, pr, c


def S_(Xt, Pt, X, L, x0, r):
    return entropia_gauge(Xt, Pt, disco(X, L, x0, r))


def sondas(Xs, Ps, X0, P0, X, L, c, escala):
    out = {}; nmin = 1.0
    for fr in FR:
        x0 = c + np.array([fr * escala, 0.0]); v = []
        for r in RP:
            a, n1 = S_(Xs, Ps, X, L, x0, r); b, n2 = S_(X0, P0, X, L, x0, r); v.append(a - b); nmin = min(nmin, n1, n2)
        out[str(fr)] = v
    return out, nmin


def job(spec):
    tipo, par = spec; t0 = time.time()
    X, L, pr, c = geo(); N = len(X)
    X0, P0, _ = vacuo(N, pr, np.ones(len(pr)), 0.0)
    out = dict(tipo=tipo, par=par, rhos=RHOS.tolist(), rp=RP.tolist(), fr=list(FR)); nmin = 1.0
    if tipo == "aperto":
        w = par; Kt = ktil(N, pr, np.ones(len(pr))); f = modo_chapeu(X, L, c, w)
        S0 = []
        for r in RHOS:
            s, n = S_(X0, P0, X, L, c, r); S0.append(s); nmin = min(nmin, n)
        out["S0"] = S0
        for rs in RS:
            Xs, Ps = aperta(X0, P0, f, rs); o = {}
            S = []
            for r in RHOS:
                s, n = S_(Xs, Ps, X, L, c, r); S.append(s); nmin = min(nmin, n)
            o["S"] = S
            o["sondas"], n = sondas(Xs, Ps, X0, P0, X, L, c, w); nmin = min(nmin, n)
            e = energia_local(Kt, Xs - X0, Ps - P0); o["E_total"] = float(e.sum()); o["r50_sombra"] = raio_metade(X, L, c, e)
            o["dK_centrado"] = [delta_K(X, L, c, r, e) for r in RHOS]
            if w == WS[1] and rs == 0.25:
                M = np.zeros((len(OFF_D), len(OFF_R)))
                for i, d in enumerate(OFF_D):
                    for j, r in enumerate(OFF_R):
                        x0 = c + np.array([d, 0.0]); M[i, j] = S_(Xs, Ps, X, L, x0, r)[0] - S_(X0, P0, X, L, x0, r)[0]
                o["mapa"] = M.tolist(); o["mapa_d"] = OFF_D.tolist(); o["mapa_r"] = OFF_R.tolist()
            out[f"r{rs}"] = o
        if w == WS[0]:
            idx = disco(X, L, c, 6.0); out["k0"] = [entropia_gauge(X0, P0, idx, j)[0] for j in (0, len(idx) // 2, len(idx) - 1)]
    elif tipo == "padrao":
        R = par; Xp, Pp, _ = vacuo(N, pr, kappa_padrao(X, L, pr, c, R, 0.25), 0.0)
        out["sondas"], nmin = sondas(Xp, Pp, X0, P0, X, L, c, R)
    elif tipo == "vmais":
        Xu, Pu, npar = unitario_gauge(X0, P0, X, L, pr, c, 5.0, r_sq=0.25)
        out["sondas"], nmin = sondas(Xu, Pu, X0, P0, X, L, c, 5.0); out["pares"] = npar
        S = []; S0 = []
        for r in RHOS:
            S.append(S_(Xu, Pu, X, L, c, r)[0]); S0.append(S_(X0, P0, X, L, c, r)[0])
        out["S"] = S; out["S0"] = S0
    out["nu_min"] = nmin
    nome = f"{tipo}_{par:g}"
    json.dump(out, open(os.path.join(D, nome + ".json"), "w"))
    log("ok", nome, f"{time.time() - t0:.0f}s nu_min={nmin:.12f}")
    return nome


def main():
    log("== início", "TESTE" if TESTE else "")
    specs = [("aperto", w) for w in WS] + [("padrao", R) for R in ((2.0, 3.0) if TESTE else (4.0, 5.0))] + [("vmais", 5.0)]
    with Pool(int(os.environ.get("E67_PROCESSOS", "2"))) as pool:   # nº de processos não muda o resultado
        for _ in pool.imap_unordered(job, specs):
            pass
    log("== fim")


if __name__ == "__main__":
    main()
