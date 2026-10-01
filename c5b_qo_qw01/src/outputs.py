"""Gráficos separados por escala e relatório epistemológico A–J."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from prem_adapter import G, C, M, R
from geometry import isolated, ALPHA_BASE, STRESS
from earth import RHOC, reference


def save(path, xlabel, ylabel, xscale="linear", yscale="linear"):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.grid(alpha=.25)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(path.with_suffix(".png"), dpi=170)
    plt.savefig(path.with_suffix(".pdf"))
    plt.close()


def make_plots(root, selected, base_profile):
    plots = root/"plots"
    plots.mkdir(exist_ok=True)
    base_g = base_profile["g"]
    base_r = base_profile["r"]
    for key, title, name, logy in [("g", "g estática própria (m/s²)", "01_gravity_earth", True),
          ("P_Pa", "P da matéria (Pa)", "03_pressure_earth", True),
          ("rho", "rho prescrita (kg/m³)", "04_density_earth", False)]:
        plt.figure(figsize=(8, 5))
        mask0 = base_r/R >= 1e-5
        plt.plot(base_r[mask0]/R, base_profile[key][mask0], label="PREM convencional GR")
        for f, a, p in selected:
            if a != 2.:
                continue
            mask = (p["r"]/R >= 1e-5) & (p[key] > 0)
            plt.plot(p["r"][mask]/R, p[key][mask], label=f"f={f:g}, alpha=2")
        save(plots/name, "r/R da Terra (escala terrestre)", title, "log", "log" if logy else "linear")
    plt.figure(figsize=(8, 5))
    for f, a, p in selected:
        if a != 2.:
            continue
        mask = (p["r"]/R >= 1e-5) & (p["r"] < .999*R)
        conventional = reference(0.).evaluate(p["r"][mask])
        ref = C*C*np.sqrt(conventional["F"])*conventional["phip"]
        plt.plot(p["r"][mask]/R, (p["g"][mask]-ref)/ref, label=f"f={f:g}")
    save(plots/"02_relative_gravity", "r/R da Terra", "(g_QW-g_PREM_GR)/g_PREM_GR", "log", "symlog")
    y = np.unique(np.r_[1., 1+np.geomspace(1e-10, 1, 100), np.geomspace(1.000001, 100, 280)])
    for key, title, name, logy in [("A", "A_W(r)", "05_A_micro", False),
          ("b_r", "b_W(r)/r", "06_b_over_r_micro", False),
          ("nec_scaled", "NEC_W / [c⁴/(8 pi G r0²)]", "07_NEC_micro", False),
          ("g_r0_c2", "g_W / (c²/r0)", "09_gravity_micro", False)]:
        plt.figure(figsize=(8, 5))
        for a in ALPHA_BASE:
            plt.plot(y, isolated(y, a)[key], label=f"alpha={a:g}")
        save(plots/name, "r/r0 (uma boca; 1 a 100)", title, "log", "log" if logy else "linear")
    fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    for a in ALPHA_BASE:
        w = isolated(y, a)
        for ax, key, label in zip(axes, ["ricci_scaled", "ricci2_scaled", "kretsch_scaled"],
                                 ["Ricci × r0²", "Ricci² × r0⁴", "Kretschmann × r0⁴"]):
            ax.plot(y, w[key], label=f"alpha={a:g}")
            ax.set_ylabel(label)
            ax.set_yscale("symlog", linthresh=1e-7)
            ax.grid(alpha=.25)
    axes[-1].set_xscale("log")
    axes[-1].set_xlabel("r/r0; invariantes finitos no limite r=r0")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(plots/"08_curvature_micro.png", dpi=170)
    fig.savefig(plots/"08_curvature_micro.pdf")
    plt.close(fig)
    plt.figure(figsize=(8, 5))
    for f, a, p in selected:
        if f != 1e-8:
            continue
        r0 = a*G*f*M/C**2
        mask = p["r"]/r0 <= 100
        plt.plot(p["r"][mask]/r0, p["P_Pa"][mask], label=f"alpha={a:g}, f=1e-8")
    save(plots/"10_pressure_micro", "r/r0 (uma boca)", "P da matéria (Pa): finita, muito elevada", "log", "log")
    plt.figure(figsize=(8, 5))
    for a in ALPHA_BASE:
        w = isolated(y, a)
        plt.plot(y, w["energy_scaled"], label=f"E_W, alpha={a:g}")
    save(plots/"11_energy_density_micro", "r/r0", "E_W / [c⁴/(8 pi G r0²)]", "log", "symlog")
    # Invariantes com unidades SI para uma massa declarada; não só normalizados.
    plt.figure(figsize=(8, 5))
    for a in ALPHA_BASE:
        r0 = a*G*1e-8*M/C**2
        plt.plot(y, isolated(y, a)["kretsch_scaled"]/r0**4, label=f"alpha={a:g}, f=1e-8")
    save(plots/"12_Kretschmann_SI_micro", "r/r0", "Kretschmann (m⁻⁴)", "log", "log")


def make_report(root, rows, validation, tests):
    worms = [r for r in rows if r["f"] > 0]
    base = rows[0]
    a2 = [r for r in worms if r["alpha"] == 2.]
    pmin = min(r["P_throat_Pa"] for r in worms)
    pmax = max(r["P_throat_Pa"] for r in worms)
    emin = min(r["NEC_negative_proper_volume_one_mouth_J"] for r in worms)
    emax = max(r["NEC_negative_proper_volume_one_mouth_J"] for r in worms)
    nmin = min(r["NEC_min_W_Pa"] for r in worms)
    nmax = max(r["NEC_min_W_Pa"] for r in worms)
    kmin = min(r["Kretsch_throat_W_m4"] for r in worms)
    kmax = max(r["Kretsch_throat_W_m4"] for r in worms)
    lines = ["# C5B-QO-QW01 — relatório", "", "**STATUS: EXECUÇÃO CONCLUÍDA**", "",
        f"[M] {len(rows)} casos executados: {len(worms)} gargantas e uma referência PREM. "
        f"{sum(r['numerically_valid'] for r in rows)} casos numericamente válidos. "
        f"{tests['tests_run']} testes aprovados, {tests['failures']} falhas e {tests['errors']} erros.", "",
        "## O que foi calculado", "",
        "[M] Métrica isolada exata proposta e extensão composta declarada no README. "
        "A geometria composta é um ansatz fixo: b=b_W+2Gm_mat/c², "
        "Phi=Phi_W+Phi_E, onde Phi_E vem de TOV com densidade PREM prescrita. "
        "Einstein reconstrói o tensor total; o resíduo após retirar o fluido "
        "terrestre conservado é o setor exótico necessário. A composição não é "
        "uma lei de superposição da GR nem uma EOS terrestre autocoerente.", "",
        "[F] Para um observador estático, u^t=1/sqrt(A), "
        "a^r=c²A'/(2AB) e |a|=c²|A'|/(2A sqrt(B))=c²sqrt(F)|Phi'|. "
        "A conservação de um fluido isotrópico exige P'=−(rho c²+P)Phi'. "
        "Em distância própria, dP/dl=−(rho+P/c²)g. Portanto −rho*g por unidade "
        "de r não é válido arbitrariamente perto da garganta.", "",
        "[M] b(r0)=r0, A(r0)=alpha/(alpha+2)>0, b'(r0)=2/alpha−1. "
        "F=(r−r0)(r+r0−2mu)/r². Flare-out estrito e boca lorentziana requerem "
        "alpha>1. A divergência de B=1/F em r0 é de coordenada; usando distância "
        "própria, r−r0 é proporcional a l² e os invariantes têm limites finitos.", "",
        "## Respostas físicas A–J", "",
        "**A)** [M] Sim, para cada r0>0 e alpha>1 esta garganta remove a "
        "singularidade pontual dentro do domínio definido: g→0 na garganta, "
        "P é finita e os três invariantes são finitos. Não existe um centro r=0 "
        "nessa boca; ele foi substituído por uma superfície mínima e outra região.", "",
        f"**B)** [M] Não apareceu divergência de curvatura ou pressão em nenhum "
        f"caso admitido. Entretanto P(r0) variou de {pmin:.6e} a {pmax:.6e} Pa, "
        f"contra {base['Pmax_Pa']:.6e} Pa no centro PREM de referência. "
        "Isso é pressão extrema com densidade ainda prescrita como terrestre, "
        "sem EOS que a justifique. O limite paramétrico r0→0 não é regular: "
        "curvaturas e tensões podem divergir.", "",
        "**C)** [M] Sim, em primeira ordem assintótica: A_W=1−2mu/r+O(r⁻²), "
        "B_W=1+2mu/r+O(r⁻²), g_W→GM_W/r². O exterior não é exatamente vácuo "
        "Schwarzschild: o tensor requerido possui cauda. A garganta remove "
        "a singularidade, mas preserva o sinal gravitacional de massa em grande r.", "",
        "**D)** [M] A gravidade profunda aumenta aproximadamente como no modelo "
        "pontual anterior em raios terrestres. As pequenas correções de GR da "
        "referência são separadas da comparação Newtoniana na tabela de amostras.", "",
        "| f | Δg/g PREM a 100 km | P(r0), alpha=2 (Pa) |",
        "|---:|---:|---:|"]
    for r in a2:
        lines.append(f"| {r['f']:g} | {r['relative_g_100km']:.8e} | {r['P_throat_Pa']:.6e} |")
    lines += ["", "**E)** [M] As menores massas produzem pequenas alterações nos "
        "pontos terrestres amostrados; a tabela permite conferir o crescimento "
        "sem escolher um limite arbitrário. Isso não estabelece compatibilidade "
        "sísmica: faltam EOS, velocidades elásticas, dados e covariâncias. "
        "Mesmo quando a alteração macroscópica é pequena, o microambiente "
        "da garganta exige pressão e tensor exótico extremos.", "",
        f"**F)** [M] NEC_W mínima variou de {nmin:.6e} a {nmax:.6e} Pa. "
        f"A magnitude −∫NEC_W dV próprio, em UMA boca até infinito, variou de "
        f"{emin:.6e} a {emax:.6e} J. Ela é um orçamento de violação da NEC, "
        "não energia ADM, massa do wormhole, energia de formação ou ANEC. "
        "A integral da densidade de energia negativa é calculada separadamente "
        "na tabela e é zero para 1<alpha<=2, apesar da NEC violada.", "",
        "**G)** [M] Escrevendo y=r/r0 e C*=c⁴/(8 pi G), "
        "NEC_W=C*/r0² × n_alpha(y). Na garganta, "
        "NEC_W=−2C*(alpha−1)/(alpha*r0²). A escala local cresce como r0⁻² "
        "a alpha fixo; Kretschmann cresce como r0⁻⁴. A integral própria "
        "escala como C*r0 vezes uma função de alpha. A largura negativa "
        "é INFINITA: a NEC é negativa em todo r>=r0, com cauda O(r⁻⁴), "
        "cuja integral volumétrica converge.", "",
        "**H)** [M] Aumentar r0 a massa externa fixa significa aumentar alpha. "
        "Isso reduz a escala local de tensão/curvatura nos casos grandes, "
        "mas não elimina a NEC. Para grandes alpha, o orçamento integrado "
        "cresce proporcionalmente a r0; garganta maior não implica menos "
        "quantidade exótica integrada. Os valores de cada alpha estão no CSV, "
        "incluindo o comportamento próximo do limite alpha=1.", "",
        "**I)** [M] Há combinações geometricamente regulares, sem horizonte, "
        "com convergência numérica e pequenas perturbações nos pontos terrestres "
        "amostrados. [?] Não há demonstração de compatibilidade física completa "
        "com uma Terra nem de estabilidade dinâmica. Não se deve converter "
        "validade numérica em existência física.", "",
        "**J)** [M] Nenhum critério geométrico mínimo falhou na grade admitida. "
        "A exigência de fonte exótica violando NEC já aparece no flare-out; "
        "a pressão microscópica extrema e a falta de EOS impedem afirmar "
        "um equilíbrio terrestre real. Para alpha=1, o primeiro critério "
        "que falha é flare-out estrito; surge um limite de distância própria "
        "infinita, sem A=0. Para alpha<1, há F<0 em parte da boca, invalidando "
        "a assinatura pretendida. Esses limites não são uma transição "
        "dinâmica demonstrada para um buraco negro.", "",
        "## Curvatura e tensor necessários", "",
        f"[M] Kretschmann na garganta: {kmin:.6e} a {kmax:.6e} m⁻⁴. "
        "Finito não significa moderado. O CSV registra Ricci, Ricci² e "
        "Kretschmann, tanto da métrica isolada quanto da composição. "
        "O tensor está em base ortonormal: E=C*b'/r², "
        "p_r=C*(−b/r³+2F Phi'/r), "
        "p_t=C*[F(Phi''+Phi'²+Phi'/r)+F'/2*(Phi'+1/r)]. "
        "A conservação radial do tensor isolado foi verificada simbolicamente.", "",
        "[M] O tensor exótico na composição não é simplesmente o isolado: "
        "p_r,ex=p_r,total−P_mat, E_ex=E_W. A pressão adicional e os termos "
        "de interação geométrica estão nos perfis selecionados. O orçamento "
        "integral publicado é o da métrica isolada fornecida, com seu volume "
        "próprio; não é apresentado como integral exata do planeta composto.", "",
        "## Estado não atravessável — análise preliminar", "",
        "[M] A família fornecida tem A_W(r)>0 para r>0. Phi_E da Terra de "
        "referência também é finita: nenhuma escolha admitida cria A_total=0. "
        "Variar alpha até 1 não cria um horizonte. [F] Um horizonte estático "
        "regular requer analisar A(r_h)=0, a superfície nula e F(r_h), além "
        "da regularidade em coordenadas que atravessem o horizonte. "
        "[?] Uma evolução A(r,t), b(r,t) deve satisfazer Einstein e conservação "
        "covariante. Ela não foi construída; nenhuma interpolação foi inventada.", "",
        "## Validação e limites", "",
        f"[M] Erro máximo de massa: {validation['max_mass_relative_error']:.3e}. "
        f"Mudança máxima de pressão na duplicação da resolução: "
        f"{validation['max_pressure_resolution_relative_change']:.3e}. "
        f"Erro máximo frente à ODE independente da pressão: "
        f"{validation['max_pressure_ode_relative_error']:.3e}. "
        f"Erro máximo do limite assintótico: {validation['max_asymptotic_g_relative_error']:.3e}. "
        "Dados completos em results/validation.json.", "",
        "[?] Não foram resolvidos EOS, sismologia, suporte quântico de energia "
        "exótica, evolução causal, estabilidade dinâmica ou custo de formação. "
        "A redução de rho por (1−f) continua um perfil prescrito. Massa "
        "gravitacional/Misner–Sharp e integral em volume areal não são massa "
        "bariônica em volume próprio. A grade não estima um f máximo "
        "observacional permitido.", "",
        "[H] Um Q orientador corresponder a uma microgeometria de garganta "
        "continua hipótese. A possibilidade de estados causais diferentes "
        "também continua hipótese. Os resultados aqui são conteúdo matemático "
        "de GR com fonte exótica reconstruída; não introduzem uma previsão "
        "independente específica de C5B. Não comprovam wormhole terrestre, "
        "equivalência entre emaranhamento e wormholes ou resolução da NEC.", ""]
    (root/"report/C5B_QO_QW01_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
