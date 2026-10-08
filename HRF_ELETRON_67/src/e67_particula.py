"""
HRF — ELETRON-67 — partícula na leitura (b): uma excitação quântica localizada da fronteira e sua imagem no bulk.
Excitação: aperto (squeeze) de um modo suave e localizado do campo Z (perfil "chapéu mexicano", média zero,
invariante de gauge), aplicado ao vácuo do tapete intacto. Mede: δS de discos (leitura de Ryu–Takayanagi) e a
"sombra" de energia na fronteira. Autoria: Mario José do Canto Filho, MD · código: Claude (-clau)
"""
import numpy as np
from e65_holo import minimg


def modo_chapeu(X, L, c, w):
    """perfil f ∝ (1 − r²/2w²) e^{−r²/2w²}, média exatamente zero (gauge) e norma 1."""
    r2 = (minimg(X - c, L) ** 2).sum(1)
    f = (1 - r2 / (2 * w * w)) * np.exp(-r2 / (2 * w * w))
    f = f - f.mean()
    return f / np.linalg.norm(f)


def aperta(Xt, Pt, f, r):
    """X_f → e^r X_f, P_f → e^{-r} P_f (unitário gaussiano que só age no modo f). Atualização de posto 2."""
    def upd(M, a):
        Mf = M @ f; fMf = f @ Mf
        return M + a * (np.outer(f, Mf) + np.outer(Mf, f)) + a * a * fMf * np.outer(f, f)
    return upd(Xt, np.exp(r) - 1.0), upd(Pt, np.exp(-r) - 1.0)


def energia_local(Kt, dX, dP):
    """energia acrescentada em cada GMF: ½ δ<p̃_i²> + ½ (K̃ δX̃)_ii."""
    return 0.5 * np.diag(dP) + 0.5 * np.einsum("ij,ji->i", Kt, dX)


def ktil(N, pr, kap, mu=0.0):
    """K̃ = M^{-1/2} K M^{-1/2} (mesma energia usada em e65_holo.vacuo)."""
    from e65_holo import W_E, M_N
    K = np.zeros((N, N)); a, b = pr[:, 0], pr[:, 1]; w = kap * W_E
    np.add.at(K, (a, a), w); np.add.at(K, (b, b), w); np.add.at(K, (a, b), -w); np.add.at(K, (b, a), -w)
    K += mu ** 2 * M_N * np.eye(N)
    return K / M_N


def raio_metade(X, L, c, e):
    """raio que contém metade de Σ|e| (largura da 'sombra' de energia)."""
    r = np.sqrt((minimg(X - c, L) ** 2).sum(1)); o = np.argsort(r); a = np.abs(e[o]); cum = np.cumsum(a) / a.sum()
    return float(r[o][np.searchsorted(cum, 0.5)])


def delta_K(X, L, x0, rho, e):
    """primeira lei (exploratório): δ<K_A> = 2π Σ_{i∈A} β_i δε_i, β = (ρ² − r²)/(2ρ)."""
    r2 = (minimg(X - x0, L) ** 2).sum(1); m = r2 <= rho * rho + 1e-9
    return float(2 * np.pi * ((rho * rho - r2[m]) / (2 * rho) * e[m]).sum())
