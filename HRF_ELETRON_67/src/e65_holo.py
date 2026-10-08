"""
HRF — ELETRON-65 — Da fronteira ao bulk: o vácuo do campo no tapete (fronteira 2D) e a leitura de Ryu–Takayanagi.
Tapete intacto (rede triangular a = 1, periódica), parado. Campo: polarização fora do plano (escalar nos GMFs),
H = sum Q^2/(2M) + 1/2 sum_e kappa_e w_e (Z_i - Z_j)^2 + 1/2 mu^2 sum M Z^2, com w_e = 1/sqrt(3) (cotangentes) e
M = sqrt(3)/2 (área de Voronoi) — a mesma energia do campo fora do plano da espuma (E-61/E-63) no tapete intacto.
Estado: vácuo (gaussiano). Entropia de uma região A pelas correlações (método de Peschel/Srednicki).
Autoria: Mario José do Canto Filho, MD · código: Claude (-clau)
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.linalg import eigh, cholesky

S3 = np.sqrt(3.0)
W_E, M_N = 1.0 / S3, S3 / 2.0


def rede(NX, NY):
    j, i = np.meshgrid(np.arange(NY), np.arange(NX), indexing="ij")
    X = np.stack([(i + 0.5 * (j % 2)).ravel().astype(float), (j * S3 / 2).ravel()], 1)
    L = np.array([NX, NY * S3 / 2])
    t = cKDTree(np.mod(X, L), boxsize=L)
    pr = np.array(sorted(t.query_pairs(1.01)))
    return X, L, pr


def minimg(d, L):
    return d - L * np.round(d / L)


def kappa_padrao(X, L, pr, c, R, f):
    """kappa = f nas ligações cujo ponto médio está a menos de R de c; 1 fora."""
    d = minimg(X[pr[:, 1]] - X[pr[:, 0]], L)
    mid = X[pr[:, 0]] + 0.5 * d
    r = np.sqrt((minimg(mid - c, L) ** 2).sum(1))
    k = np.ones(len(pr))
    if R > 0:
        k[r <= R] = f
    return k


def vacuo(N, pr, kap, mu):
    """correlações do vácuo nas coordenadas com massa (x~ = sqrt(M) Z): Xt = <x x>, Pt = <p p>.
    mu = 0: o modo constante (A_z constante = gauge) é removido; só diferenças de Z são usadas depois."""
    K = np.zeros((N, N))
    a, b = pr[:, 0], pr[:, 1]; w = kap * W_E
    np.add.at(K, (a, a), w); np.add.at(K, (b, b), w); np.add.at(K, (a, b), -w); np.add.at(K, (b, a), -w)
    K += mu ** 2 * M_N * np.eye(N)
    Kt = K / M_N                                    # M^{-1/2} K M^{-1/2}, M uniforme
    lam, V = eigh(Kt)
    if mu == 0:
        lam, V = lam[1:], V[:, 1:]
    s = np.sqrt(np.clip(lam, 1e-300, None))
    Xt = 0.5 * (V / s) @ V.T
    Pt = 0.5 * (V * s) @ V.T
    return Xt, Pt, lam


def entropia(Xt, Pt, idx):
    if len(idx) == 0:
        return 0.0
    XA = Xt[np.ix_(idx, idx)]; PA = Pt[np.ix_(idx, idx)]
    Lc = cholesky(XA, lower=True)
    nu2 = eigh(Lc.T @ PA @ Lc, eigvals_only=True)
    nu = np.sqrt(np.clip(nu2, 0.25, None))
    a = nu + 0.5; b = nu - 0.5
    with np.errstate(divide="ignore", invalid="ignore"):
        tb = np.where(b > 1e-14, b * np.log(b), 0.0)
    return float((a * np.log(a) - tb).sum())


def disco(X, L, x0, rho):
    return np.flatnonzero((minimg(X - x0, L) ** 2).sum(1) <= rho * rho + 1e-9)


def unitario_local(Xt, Pt, X, L, pr, c, R, r_sq=0.5, seed=65):
    """controle positivo: estado mudado por uma transformação unitária (squeezing de dois modos em pares de vizinhos)
    que age só dentro do disco P(c, R). Regiões que contêm P inteiro ou não tocam P não podem mudar de entropia."""
    rng = np.random.default_rng(seed)
    dentro = (minimg(X - c, L) ** 2).sum(1) <= R * R
    cand = [(a, b) for a, b in pr if dentro[a] and dentro[b]]
    rng.shuffle(cand); usados = set(); pares = []
    for a, b in cand:
        if a not in usados and b not in usados:
            pares.append((a, b)); usados.update((a, b))
    N = len(X); Sx = np.eye(N)
    ch, sh = np.cosh(r_sq), np.sinh(r_sq)
    for a, b in pares:
        Sx[a, a] = ch; Sx[a, b] = sh; Sx[b, a] = sh; Sx[b, b] = ch
    Sp = np.linalg.inv(Sx).T
    return Sx @ Xt @ Sx.T, Sp @ Pt @ Sp.T, len(pares)


def entropia_gauge(Xt, Pt, idx, j0=0):
    """entropia da álgebra invariante de gauge da região: diferenças Z_k - Z_k0 e momentos Q_k, condicionada ao
    centro Q_tot da região (termo clássico do centro excluído — entropia 'destilável'). Devolve (S, nu_min)."""
    idx = np.asarray(idx)
    if len(idx) < 2:
        return 0.0, 0.5
    idx = np.r_[idx[j0], np.delete(idx, j0)]
    XA = Xt[np.ix_(idx, idx)]; PA = Pt[np.ix_(idx, idx)]
    XY = XA[1:, 1:] - XA[1:, :1] - XA[:1, 1:] + XA[0, 0]
    cc = PA[1:, :].sum(1); v = PA.sum(); PC = PA[1:, 1:] - np.outer(cc, cc) / v
    Lc = cholesky(XY, lower=True)
    nu = np.sqrt(np.clip(eigh(Lc.T @ PC @ Lc, eigvals_only=True), 0.0, None))
    nmin = float(nu.min()); nu = np.clip(nu, 0.5, None); a = nu + 0.5; b = nu - 0.5
    bl = np.where(b > 1e-14, b * np.log(np.where(b > 1e-14, b, 1.0)), 0.0)
    return float((a * np.log(a) - bl).sum()), nmin


def unitario_gauge(Xt, Pt, X, L, pr, c, R, r_sq=0.5, seed=65):
    """controle positivo invariante de gauge: aperta (squeeze) o modo-diferença (Z_a - Z_b) de pares disjuntos de
    vizinhos dentro de P(c, R), sem tocar o modo-soma. Preserva o modo constante e a soma dos Q."""
    rng = np.random.default_rng(seed)
    dentro = (minimg(X - c, L) ** 2).sum(1) <= R * R
    cand = [(a, b) for a, b in pr if dentro[a] and dentro[b]]
    rng.shuffle(cand); usados = set(); pares = []
    for a, b in cand:
        if a not in usados and b not in usados:
            pares.append((a, b)); usados.update((a, b))
    N = len(X); Sx = np.eye(N); Sp = np.eye(N)
    e, ei = np.exp(r_sq), np.exp(-r_sq)
    for a, b in pares:
        Sx[a, a] = Sx[b, b] = (1 + e) / 2; Sx[a, b] = Sx[b, a] = (1 - e) / 2
        Sp[a, a] = Sp[b, b] = (1 + ei) / 2; Sp[a, b] = Sp[b, a] = (1 - ei) / 2
    return Sx @ Xt @ Sx.T, Sp @ Pt @ Sp.T, len(pares)
