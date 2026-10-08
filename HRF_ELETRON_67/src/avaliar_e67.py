"""HRF — ELETRON-67 — aplica as regras pré-registradas (protocolo §5). Uso: python3 avaliar_e67.py [teste]"""
import os, sys, json
import numpy as np

TESTE = len(sys.argv) > 1 and sys.argv[1] == "teste"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # pasta do pacote (acima de src/)
BASE = os.path.join(RAIZ, "teste_saida") if TESTE else RAIZ          # modo teste grava à parte
D = os.path.join(BASE, "dados"); RES = os.path.join(BASE, "resultados")
WS = (2.0, 3.0) if TESTE else (4.0, 5.0, 6.0, 7.0)
PADROES = (2.0, 3.0) if TESTE else (4.0, 5.0)
J = lambda n: json.load(open(os.path.join(D, n + ".json")))


def expoente(rp, v):
    v = np.abs(np.array(v)); rp = np.array(rp); m = v > 1e-12
    if m.sum() < 3:
        return float("nan")
    return float(np.polyfit(np.log(rp[m]), np.log(v[m]), 1)[0])


def p_min(son, rp):
    ps = {fr: expoente(rp, v) for fr, v in son.items()}
    return float(np.nanmin(list(ps.values()))), ps


def classe_N(p):
    return "NORMALIZÁVEL" if p >= 2.0 else ("GRUDADA" if p <= 1.0 else "INTERMEDIÁRIA")


def main():
    out = {"aperto": {}, "controles": {}, "validacoes": {}}
    for w in WS:
        a = J(f"aperto_{w:g}"); r = np.array(a["rhos"]); S0 = np.array(a["S0"]); o = {}
        for rs in ("0.1", "0.25"):
            b = a[f"r{rs}"]; dS = np.array(b["S"]) - S0
            pm, ps = p_min(b["sondas"], a["rp"])
            mw = r <= 3 * w; zc = float((r[mw] * np.abs(dS[mw])).sum() / np.abs(dS[mw]).sum())   # janela ρ ≤ 3w
            dK = np.array(b["dK_centrado"]); mk = (r >= 2) & (r <= 3 * w) & (np.abs(dK) > 1e-9)
            o[rs] = dict(p_min=pm, p_por_posicao=ps, classe_N=classe_N(pm), z_centroide=zc, z_sobre_w=zc / w,
                         r50_sombra=b["r50_sombra"], z_sobre_r50=zc / b["r50_sombra"], z_sobre_r50_ref_pontual=1.55, E_total=b["E_total"],
                         dS_max=float(np.abs(dS).max()), rho_pico=float(r[np.argmax(np.abs(dS))]),
                         primeira_lei_mediana=float(np.median(dS[mk] / dK[mk])) if mk.any() else float("nan"),
                         fecho=float(np.abs(dS[r >= 4 * w]).max() / np.abs(dS).max()) if (r >= 4 * w).any() else float("nan"))
        rL = np.array(a["rhos"]); d1 = np.array(a["r0.1"]["S"]) - S0; d2 = np.array(a["r0.25"]["S"]) - S0
        mb = np.abs(d2) >= 0.5 * np.abs(d2).max(); o["linearidade"] = float(np.median(d2[mb] / d1[mb]))
        out["aperto"][f"w{w:g}"] = o
    cls = [out["aperto"][f"w{w:g}"]["0.25"]["classe_N"] for w in WS]
    N = max(set(cls), key=cls.count) if max(cls.count(x) for x in set(cls)) >= len(WS) - 1 else "MISTA"
    zw = np.array([out["aperto"][f"w{w:g}"]["0.25"]["z_sobre_w"] for w in WS]); cv = float(np.std(zw) / np.mean(zw))
    zz = np.array([out["aperto"][f"w{w:g}"]["0.25"]["z_centroide"] for w in WS]); b, a0_ = np.polyfit(np.array(WS), zz, 1)
    out["ajuste_z"] = dict(inclinacao=float(b), intercepto=float(a0_), CV_z_sobre_w=cv)
    Z = "PROPORCIONAL" if (cv <= 0.1 and 0.7 <= b <= 1.5) else ("NÃO PROPORCIONAL" if (cv >= 0.3 or b < 0.4) else "PARCIAL")
    for R in PADROES:
        p = J(f"padrao_{R:g}"); pm, ps = p_min(p["sondas"], p["rp"])
        out["controles"][f"padrao_R{R:g}"] = dict(p_min=pm, p_por_posicao=ps, classe_N=classe_N(pm))
    v = J("vmais_5"); pm, ps = p_min(v["sondas"], v["rp"])
    out["controles"]["vmais"] = dict(p_min=pm, p_por_posicao=ps, classe_N=classe_N(pm))
    r = np.array(v["rhos"]); dv = np.array(v["S"]) - np.array(v["S0"])
    val = out["validacoes"]
    a0 = J(f"aperto_{WS[0]:g}"); S0 = np.array(a0["S0"]); m = (r >= 3) & (r <= (6 if TESTE else 20))
    pf = np.polyfit(r[m], S0[m], 1); res = S0[m] - np.polyval(pf, r[m]); R2 = 1 - (res ** 2).sum() / ((S0[m] - S0[m].mean()) ** 2).sum()
    val["V0_lei_de_area"] = dict(R2=float(R2), ok=bool(R2 >= 0.99))
    nus = [J(f"aperto_{w:g}")["nu_min"] for w in WS] + [J(f"padrao_{R:g}")["nu_min"] for R in PADROES] + [v["nu_min"]]
    val["Vnu"] = dict(min=float(min(nus)), ok=bool(min(nus) >= 0.5 - 1e-9))
    k0 = a0["k0"]; val["VK"] = dict(espalhamento=float(max(k0) - min(k0)), ok=bool(max(k0) - min(k0) <= 1e-8))
    val["Vmais_fecho"] = dict(max_contem=float(np.abs(dv[r >= 5.5]).max()), ok=bool(np.abs(dv[r >= 5.5]).max() <= 1e-8))
    lin = [out["aperto"][f"w{w:g}"]["linearidade"] for w in WS]
    val["VL_linearidade"] = dict(razoes=lin, ok=bool(all(2.0 <= x <= 4.5 for x in lin)))   # linear 2,5 · quadrático 6,25
    dp = [abs(out["aperto"][f"w{w:g}"]["0.1"]["p_min"] - out["aperto"][f"w{w:g}"]["0.25"]["p_min"]) for w in WS]
    val["VP_expoente_estavel"] = dict(diferencas=dp, ok=bool(all(x <= 0.3 for x in dp)))
    ctrl = [out["controles"][k]["classe_N"] for k in out["controles"]]
    val["VC_controles_grudados"] = dict(classes=ctrl, ok=bool(all(x == "GRUDADA" for x in ctrl)))
    fe = [out["aperto"][f"w{w:g}"]["0.25"]["fecho"] for w in WS]
    val["VF_fecho_aperto"] = dict(valores=fe, ok=bool(all((x <= 0.01) or np.isnan(x) for x in fe)))
    base_ok = all(val[k]["ok"] for k in ("V0_lei_de_area", "Vnu", "VK", "Vmais_fecho", "VC_controles_grudados"))
    if not base_ok:
        geral = "INCONCLUSIVO"
    elif N == "NORMALIZÁVEL" and Z == "PROPORCIONAL":
        geral = "SIM — a excitação aparece como objeto do bulk (só o campo dela chega à fronteira), com profundidade proporcional ao tamanho"
    elif N == "GRUDADA":
        geral = "NÃO — a excitação fica grudada na fronteira (como um padrão)"
    else:
        geral = "PARCIAL"
    dec = {"H67 (partícula no bulk)": geral, "H67-N (objeto do bulk × grudado)": N if base_ok else "INCONCLUSIVO",
           "H67-Z (profundidade ∝ tamanho)": Z if base_ok else "INCONCLUSIVO"}
    out["decisoes"] = dec; out["CV_z_sobre_w"] = cv
    json.dump(out, open(os.path.join(RES, "E67_resumo.json"), "w"), indent=1, ensure_ascii=False, default=float)
    print(json.dumps(dec, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
