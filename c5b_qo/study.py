"""PREM diagnóstico e politropo carregado n=1; nenhuma modificação da gravitação."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.integrate import cumulative_simpson, quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

M = 5.9722e24
R = 6.371e6
G = 6.67430e-11
C = 299792458.0
BASE_F = [0., 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, .05, .10, .25, .50]
RADII = {"100km": 1e5, "1221_5km": 1.2215e6, "3480km": 3.480e6, "R_2": R/2}
# (limite inferior km, superior km, coeficientes crescentes em x=r/R).
LAYERS = [
    (0., 1221.5, [13.0885, 0., -8.8381]),
    (1221.5, 3480., [12.5815, -1.2638, -3.6426, -5.5281]),
    (3480., 5701., [7.9565, -6.4761, 5.5283, -3.0807]),
    (5701., 5771., [5.3197, -1.4836]),
    (5771., 5971., [11.2494, -8.0298]),
    (5971., 6151., [7.1089, -3.8045]),
    (6151., 6346.6, [2.6910, .6924]),
    (6346.6, 6356., [2.9]),
    (6356., 6368., [2.6]),
    (6368., 6371., [1.02]),
]
K = 2*G*R**2/np.pi


def primitive(coeff, r, power=2):
    r = np.asarray(r)
    return sum(a*r**(j+power+1)/(R**j*(j+power+1)) for j, a in enumerate(coeff))


RAW_MASS = sum(4*np.pi*1000*(primitive(a, hi*1000)-primitive(a, lo*1000))
               for lo, hi, a in LAYERS)
NORMALIZATION = M/RAW_MASS


def density(r):
    values = np.asarray(r, dtype=float)
    out = np.zeros_like(values)
    for lo, hi, a in LAYERS:
        mask = (values >= lo*1000) & (values < hi*1000)
        out = np.where(mask, 1000*NORMALIZATION*np.polynomial.polynomial.polyval(values/R, a), out)
    out = np.where(values == R, 1000*NORMALIZATION*LAYERS[-1][2][0], out)
    return out


def mass(r):
    values = np.asarray(r, dtype=float)
    out = np.zeros_like(values)
    for lo, hi, a in LAYERS:
        stop = np.clip(values, lo*1000, hi*1000)
        out += 4*np.pi*1000*NORMALIZATION*(primitive(a, stop)-primitive(a, lo*1000))
    return out


def gravity(r, f=0.):
    values = np.asarray(r, dtype=float)
    if np.any(values <= 0):
        raise ValueError("g avaliada apenas em r>0; centro singular para f>0.")
    return G*(f*M+(1-f)*mass(values))/values**2


def relative_gravity(r, f):
    return f*(M/mass(r)-1)


def schwarzschild_radius(f):
    return 2*G*M*f/C**2


def cutoff(f):
    return max(1., 100*schwarzschild_radius(f))


def pressure_integral(r, f=0.):
    """Referência independente por quadratura em cada camada; não atravessa horizonte."""
    if r < 0 or (f > 0 and r <= schwarzschild_radius(f)):
        raise ValueError("P não é integrada através do horizonte.")
    result = 0.
    for lo, hi, a in LAYERS:
        start = max(r, lo*1000)
        end = hi*1000
        if start >= end:
            continue
        def integrand(s):
            rho = 1000*NORMALIZATION*np.polynomial.polynomial.polyval(s/R, a)
            return (1-f)*rho*float(gravity(s, f))
        if start == 0:
            result += quad(integrand, 0, end, epsabs=1e-2, epsrel=2e-11)[0]
        else:
            result += quad(lambda t: math.exp(t)*integrand(math.exp(t)),
                           math.log(start), math.log(end), epsabs=1e-2, epsrel=2e-11)[0]
    return result


def diagnostic_profile(f, resolution=1200):
    """Integra pressão separando saltos do PREM e usando log r no centro."""
    rmin = cutoff(f)
    chunks = []
    p_top = 0.
    for lo, hi, a in reversed(LAYERS):
        start, end = max(rmin, lo*1000), hi*1000
        if start >= end:
            continue
        # Malha composta: resolução por comprimento físico e por décadas.
        n = max(20, int(resolution*(end-start)/R)+int(30*math.log(end/start)))
        radii = np.unique(np.r_[np.linspace(start, end, n), np.geomspace(start, end, n),
                                [v for v in RADII.values() if start < v < end]])
        rho = (1-f)*1000*NORMALIZATION*np.polynomial.polynomial.polyval(radii/R, a)
        accel = gravity(radii, f)
        t = np.log(radii)
        integ = cumulative_simpson(rho*accel*radii, x=t, initial=0.)
        pressures = p_top + integ[-1]-integ
        p_top = float(pressures[0])
        chunks.append((radii, rho, accel, pressures))
    chunks.reverse()
    arrays = [np.concatenate([ch[j] if i == 0 else ch[j][1:]
                              for i, ch in enumerate(chunks)]) for j in range(4)]
    return dict(zip(["r", "rho", "g", "p"], arrays))


def maximum_gravity(f):
    candidates = [cutoff(f), R]
    for lo, hi, _ in LAYERS:
        a, b = max(cutoff(f), 1000*lo), 1000*hi
        candidates.extend([a, b])
        opt = minimize_scalar(lambda s: -float(gravity(s, f)), bounds=(a, b), method="bounded")
        if opt.success:
            candidates.append(opt.x)
    return max(((float(gravity(s, f)), s) for s in candidates), key=lambda p: p[0])


def influence_radius(f):
    if f == 0:
        return 0.
    target = f*M/(1-f)
    if target >= M:
        return R
    return brentq(lambda s: float(mass(s))-target, 0., R, xtol=1e-7)


def base_inertia():
    return sum(8*np.pi/3*1000*NORMALIZATION*(primitive(a, hi*1000, 4)-primitive(a, lo*1000, 4))
               for lo, hi, a in LAYERS)/(M*R**2)


def refined_f():
    """Adiciona pontos nas transições de sensibilidade, sem alegar limites empíricos."""
    vals = set(BASE_F)
    transitions = []
    for label, radius in RADII.items():
        gain = M/float(mass(radius))-1
        for tolerance in [.01, .05, .10]:
            f = tolerance/gain
            transitions.append({"raio": label, "tolerancia_ilustrativa": tolerance, "f": f})
            if 1e-8 < f < .5:
                vals.update(v for v in [.9*f, f, 1.1*f] if v <= .5)
    return sorted(vals), transitions


def polytrope_analytic(f, x):
    x = np.asarray(x)
    if f == 0:
        z = np.pi
        w = np.sin(np.pi*x)/np.pi
        q = (np.sin(np.pi*x)-np.pi*x*np.cos(np.pi*x))/np.pi
    else:
        z = brentq(lambda z: np.sin(z)/z-f, 1e-9, np.pi, xtol=5e-15)
        # Usa 1/z em vez de f/sin(z), evitando cancelamento para f muito pequeno.
        w = np.sin(z-np.pi*x)/z
        q = (np.sin(z-np.pi*x)+np.pi*x*np.cos(z-np.pi*x))/z
    return z/np.pi, w, q


def polytrope(f, rtol=2e-10, max_step=.06):
    """Shooting: w=x*h/(GM/R), q=(Mc+m)/M. K nunca muda."""
    xmin = cutoff(f)/R
    def rhs(t, y):
        x = np.exp(t)
        w, q = y
        return [w-q, np.pi**2*x*x*w]
    def integrate(xs, dense=False):
        sol = solve_ivp(rhs, (math.log(xs), math.log(xmin)), [0., 1.],
                        method="DOP853", rtol=rtol, atol=rtol*1e-8,
                        max_step=max_step, dense_output=dense)
        if not sol.success:
            raise RuntimeError(sol.message)
        return sol
    if f == 0:
        xs = 1.
        # O centro regular fornece uma série; integrar para fora evita amplificar
        # contaminação pela solução singular ao integrar para dentro.
        w0 = xmin*(1-np.pi**2*xmin**2/6+np.pi**4*xmin**4/120)
        q0 = np.pi**2*xmin**3/3-np.pi**4*xmin**5/30
        sol = solve_ivp(rhs, (math.log(xmin), 0.), [w0, q0], method="DOP853",
                        rtol=rtol, atol=rtol*1e-8, max_step=max_step, dense_output=True)
        if not sol.success:
            raise RuntimeError(sol.message)
    else:
        xs = brentq(lambda s: integrate(s).y[1, -1]-f, .1, 1., xtol=5e-15)
        sol = integrate(xs, True)
    x = np.unique(np.r_[np.geomspace(xmin, xs, 1200), np.linspace(xmin, xs, 1200)])
    w, q = sol.sol(np.log(x))
    if f == 0:
        # Normaliza a amplitude pelo único alvo de massa do caso base.
        scale = q[-1]
        w, q = w/scale, q/scale
        w[-1] = 0.
    h = G*M/R*w/x
    rho = h/(2*K)
    p = K*rho**2
    xa, wa, qa = polytrope_analytic(f, x)
    return {"x": x, "w": w, "q": q, "rho": rho, "p": p, "xs": xs,
            "radius_error": abs(xs-xa), "w_error": float(np.max(abs(w-wa))),
            "q_error": float(np.max(abs(q-qa))), "inner_residual": float(q[0]-f),
            "min_density": float(rho.min())}


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def save_plot(path, xlabel, ylabel, xscale="linear", yscale="linear"):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.grid(alpha=.25)
    plt.legend(fontsize=8)
    plt.tight_layout()
    for extension in ["png", "pdf"]:
        plt.savefig(path.with_suffix("."+extension), dpi=180)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    fs, transitions = refined_f()
    p0 = pressure_integral(0, 0)
    inertia0 = base_inertia()
    rows, validations, cuts = [], [], []
    selected = [0., 1e-8, 1e-6, 1e-4, .01, .1, .5]
    profiles = {}
    for f in fs:
        prof = diagnostic_profile(f)
        gm, rgm = maximum_gravity(f)
        rmin = cutoff(f)
        pm = float(prof["p"][0])
        baseline_cut = pressure_integral(rmin, 0)
        row = {"f": f, "Mc_kg": f*M, "Mmat_kg": (1-f)*M,
               "rs_m": schwarzschild_radius(f), "rs_R": schwarzschild_radius(f)/R,
               "rmin_m": rmin, "g_superficie_m_s2": float(gravity(R, f)),
               "gmax_dominio_m_s2": gm, "raio_gmax_m": rgm,
               "Pmax_dominio_Pa": pm, "raio_Pmax_m": rmin,
               "delta_Pmax_rel_mesmo_corte": pm/baseline_cut-1,
               "raio_Mc_igual_mmat_m": influence_radius(f),
               "I_MR2": (1-f)*inertia0,
               "delta_I_rel": -f,
               "divergencia_formal_P": "1/r" if f else "nenhuma",
               "Pcentral_global_Pa": "divergente" if f else p0,
               "campo_forte_r_ate_m": 10*schwarzschild_radius(f),
               "horizonte_excluido": bool(f),
               "massa_formal_dentro_rs_kg": (1-f)*float(mass(schwarzschild_radius(f))),
               "massa_material_excluida_no_corte_kg": (1-f)*float(mass(rmin)),
               "estabilidade": "não calculada",
               "validade": "perfil prescrito truncado; singular" if f else "diagnóstico PREM regular"}
        for label, radius in RADII.items():
            row["g_"+label+"_m_s2"] = float(gravity(radius, f))
            row["delta_g_rel_"+label] = float(relative_gravity(radius, f))
            row["P_"+label+"_Pa"] = pressure_integral(radius, f)
        rows.append(row)
        if f in BASE_F:
            hi = diagnostic_profile(f, 2400)
            ref = pressure_integral(rmin, f)
            relerr = abs(pm-ref)/ref
            errhi = abs(float(hi["p"][0])-ref)/ref
            # Compara também em raios macroscópicos; falha gera erro visível.
            point_errors = []
            for radius in RADII.values():
                i = int(np.argmin(abs(prof["r"]-radius)))
                exact = pressure_integral(radius, f)
                point_errors.append(abs(float(prof["p"][i])-exact)/exact)
            validations.append({"f": f, "P_quadratura_Pa": ref,
                                "erro_P_1200_rel": relerr, "erro_P_2400_rel": errhi,
                                "mudanca_resolucao_rel": abs(float(hi["p"][0])-pm)/ref,
                                "erro_P_raios_referencia_rel": max(point_errors),
                                "erro_massa_rel": abs(f*M+(1-f)*float(mass(R))-M)/M,
                                "epsilon_rs_rmin": schwarzschild_radius(f)/rmin})
            if max(relerr, errhi, *point_errors) > 2e-5:
                raise RuntimeError(f"Falha de convergência da pressão para f={f}")
            for multiplier in [1., 10., 100., 1000.]:
                rc = rmin*multiplier
                pc = pressure_integral(rc, f)
                cuts.append({"f": f, "rmin_m": rc, "Pmax_dominio_Pa": pc,
                             "g_no_corte_m_s2": float(gravity(rc, f)),
                             "rs_rmin": schwarzschild_radius(f)/rc})
            write_csv(out/f"perfil_prem_f_{f:g}.csv", [
                {"r_m": r, "x": r/R, "rho_kg_m3": rho, "g_m_s2": g,
                 "P_Pa": p, "delta_g_rel": float(relative_gravity(r, f))}
                for r, rho, g, p in zip(prof["r"], prof["rho"], prof["g"], prof["p"])])
        if f in selected:
            profiles[f] = prof
    write_csv(out/"tabela_prem.csv", rows)
    write_csv(out/"sensibilidade_corte.csv", cuts)
    write_csv(out/"transicoes_ilustrativas.csv", transitions)

    for column, ylabel, name in [("g", "g (m/s²)", "gravidade_prem"),
                                 ("p", "P (Pa)", "pressao_prem")]:
        plt.figure(figsize=(8, 5))
        for f, prof in profiles.items():
            plt.plot(prof["r"]/R, prof[column], label=f"f={f:g}")
        save_plot(out/name, "x = r/R da Terra", ylabel, "log", "log")
    plt.figure(figsize=(8, 5))
    for f, prof in profiles.items():
        if f:
            # Exclui superfície, onde a diferença é exatamente zero.
            plt.plot(prof["r"][:-1]/R, relative_gravity(prof["r"][:-1], f), label=f"f={f:g}")
    save_plot(out/"diferenca_gravidade", "x = r/R da Terra", "(g_f-g_0)/g_0", "log", "log")
    plt.figure(figsize=(8, 5))
    for f, prof in profiles.items():
        mask = prof["r"]/R >= .01
        plt.plot(prof["r"][mask]/R, prof["g"][mask], label=f"f={f:g}")
    save_plot(out/"gravidade_macroscopica", "x = r/R da Terra", "g (m/s²)", "linear", "log")

    prows, pchecks, pprofiles = [], [], {}
    for f in BASE_F:
        solution = polytrope(f)
        coarse = polytrope(f, rtol=1e-8, max_step=.12)
        xs = solution["xs"]
        row = {"f": f, "K_SI": K, "R_solucao_m": xs*R, "R_solucao_Rterra": xs,
               "delta_R_rel": xs-1, "g_superficie_m_s2": G*M/(xs*R)**2,
               "Pmax_dominio_Pa": float(solution["p"].max()),
               "rho_no_corte_kg_m3": float(solution["rho"][0]),
               "massa_no_corte_sobre_M": float(solution["q"][0]),
               "dominio_rmin_m": cutoff(f),
               "divergencia_rho": "1/r" if f else "nenhuma",
               "divergencia_P": "1/r²" if f else "nenhuma",
               "equilibrio_regular_central": not bool(f),
               "estabilidade_dinamica": "não calculada",
               "classe": "[M] politropo n=1 truncado, não terrestre"}
        prows.append(row)
        check = {"f": f, "erro_raio_analitico_Rterra": solution["radius_error"],
                 "erro_max_w_analitico": solution["w_error"],
                 "erro_max_massa_analitica_M": solution["q_error"],
                 "residuo_shooting_M": solution["inner_residual"],
                 "mudanca_raio_passo_tolerancia_Rterra": abs(xs-coarse["xs"]),
                 "mudanca_Pmax_passo_tolerancia_rel": abs(float(solution["p"].max())-
                                                          float(coarse["p"].max()))/float(solution["p"].max()),
                 "rho_min_kg_m3": solution["min_density"]}
        pchecks.append(check)
        if max(solution["radius_error"], solution["w_error"], solution["q_error"]) > 2e-7:
            raise RuntimeError(f"Politropo não concorda com solução analítica: {f}")
        if check["mudanca_Pmax_passo_tolerancia_rel"] > 2e-5:
            raise RuntimeError(f"Politropo sem convergência de pressão: {f}")
        write_csv(out/f"perfil_politropo_f_{f:g}.csv", [
            {"r_m": x*R, "x_Rterra": x, "rho_kg_m3": rho, "P_Pa": p,
             "massa_total_interior_sobre_M": q}
            for x, rho, p, q in zip(solution["x"], solution["rho"], solution["p"], solution["q"])])
        if f in selected:
            pprofiles[f] = solution
    write_csv(out/"tabela_politropo.csv", prows)
    for column, ylabel, name in [("rho", "rho (kg/m³)", "densidade_politropo"),
                                 ("p", "P (Pa)", "pressao_politropo")]:
        plt.figure(figsize=(8, 5))
        for f, prof in pprofiles.items():
            mask = prof[column] > 0
            plt.plot(prof["x"][mask], prof[column][mask], label=f"f={f:g}")
        save_plot(out/name, "x = r/R da Terra (K fixo; superfície livre)", ylabel, "log", "log")

    grrows = []
    for f in BASE_F[1:]:
        rs = schwarzschild_radius(f)
        for ratio in [1., 1.01, 1.1, 2., 10., 50.7512437810945, 100., 500.75012493758, 1000.]:
            grrows.append({"f": f, "r_rs": ratio, "r_m": ratio*rs,
                           "epsilon_rs_r": 1/ratio,
                           "a_propria_sobre_a_Newton": 1/math.sqrt(1-1/ratio) if ratio > 1 else "indefinida",
                           "dominio": "horizonte excluído" if ratio <= 1 else "Schwarzschild vácuo: referência central"})
    write_csv(out/"referencia_schwarzschild.csv", grrows)
    for check in validations:
        if check["erro_massa_rel"] > 1e-13:
            raise RuntimeError("Massa total não conservada")
    sanity = {"rs_f1_m": schwarzschild_radius(1.), "g_superficie_m_s2": G*M/R**2,
              "M_prem_original_kg": RAW_MASS, "normalizacao_prem": NORMALIZATION,
              "P0_central_Pa": p0, "I0_MR2": inertia0,
              "limite_f_observacional": None,
              "motivo_limite_indefinido": "Faltam dados sísmicos, covariâncias, EOS e dinâmica de acreção.",
              "todas_validacoes_aprovadas": True,
              "prem_convergencia": validations, "politropo_convergencia": pchecks}
    write_json(out/"validacao.json", sanity)
    write_json(out/"parametros.json", {"M_kg": M, "R_m": R, "G_SI": G, "c_m_s": C,
                "f_base": BASE_F, "f_refinada": fs, "K_politropo_SI": K,
                "camadas_PREM_km_coef_g_cm3": LAYERS, "normalizacao_PREM": NORMALIZATION,
                "raios_referencia_m": RADII, "corte": "max(1 m,100 rs)",
                "pressao_resolucoes_base": [1200, 2400],
                "pressao_quadratura_epsrel": 2e-11,
                "ODE_metodo": "DOP853", "ODE_rtol": [2e-10, 1e-8],
                "ODE_max_step_logr": [.06, .12], "ODE_atol_sobre_rtol": 1e-8,
                "shooting_xtol_Rterra": 5e-15,
                "python": platform.python_version(), "numpy": np.__version__,
                "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
                "fonte_PREM": "doi:10.1016/0031-9201(81)90046-7"})

    base_rows = {r["f"]: r for r in rows if r["f"] in BASE_F}
    lines = ["# Ensaio C5B-QO — resultados e limites", "",
        "[M] O ensaio **não determina um maior f permitido para a Terra real**. "
        "Ele mede sensibilidade de dois modelos e identifica singularidades. "
        "As tolerâncias ilustrativas não são limites observacionais.", "",
        f"[F/M] g superficial = {G*M/R**2:.8f} m/s² em todos os casos PREM prescritos; "
        "isso decorre da massa total e do raio fixos, e não valida a estrutura interna.", "",
        f"[M] PREM original: M={RAW_MASS:.9e} kg; multiplicador={NORMALIZATION:.9f}; "
        f"P central sem fonte={p0/1e9:.3f} GPa; I/(MR²)={inertia0:.7f}.", "",
        "| f | Mc (kg) | rs (m) | Δg/g0 a 100 km | influência (km) |", 
        "|---:|---:|---:|---:|---:|"]
    for f in BASE_F:
        r = base_rows[f]
        lines.append(f"| {f:g} | {r['Mc_kg']:.4e} | {r['rs_m']:.4e} | "
                     f"{r['delta_g_rel_100km']:.4e} | {r['raio_Mc_igual_mmat_m']/1000:.3f} |")
    lines += ["", "[M] Identidade exata do perfil escalado: Δg/g0=f[M/m0(r)−1]. "
        "No centro, g0~r, o excesso~f/r² e a diferença relativa~f/r³. "
        "Para rho central finita, P~G*Mc*(1−f)*rho0(0)/r para qualquer f>0.", "",
        "[M] Os máximos das tabelas referem-se apenas ao domínio "
        "r>=max(1 m,100 rs). São dependentes do corte; a pressão não tem máximo "
        "global finito na extensão pontual. A tabela de cortes verifica essa dependência. "
        "O limite formal r→0 não é uma trajetória física através do horizonte. "
        "m0 é a integral matemática do perfil prescrito desde zero; a pequena "
        "massa formal dentro de rs e a massa excluída pelo corte estão nas tabelas, "
        "não são uma atmosfera física dentro do horizonte.", "",
        "[F] r<=rs fica fora do domínio. Schwarzschild descreve vácuo, não o "
        "interior completo com matéria. A aceleração própria de um observador estático "
        "é a_N/sqrt(1−rs/r), diferente da aceleração de coordenada e do movimento em "
        "queda livre. Seu excesso sobre a_N é <=1% para r/rs>=50.7513 e <=0.1% "
        "para r/rs>=500.7502. epsilon=rs/r>=0.1 (r<=10rs) marca campo forte nesta "
        "convenção explícita. O observador estático não existe no horizonte. "
        "Essa comparação central não resolve a estrutura relativística com matéria.", "",
        "[M] O politropo mantém K fixo e massa total fixa. Sua solução livre obedece "
        "f=sin(z)/z, R_solucao/R_terra=z/pi; a integração por shooting reproduz isso. "
        "A família f>0 possui rho~1/r, P~1/r²: existe solução formal truncada, "
        "mas não um centro regular. As variações são relativas ao politropo f=0, "
        "cujo perfil de densidade não é PREM.", "",
        "| f | R_solucao/R_terra | variação de raio |", "|---:|---:|---:|"]
    for r in prows:
        lines.append(f"| {r['f']:g} | {r['R_solucao_Rterra']:.9f} | {100*r['delta_R_rel']:.6f}% |")
    lines += ["", "[?] Estabilidade dinâmica não foi calculada. Hidrostática estática "
        "e convergência não provam estabilidade nem longevidade. Para um BH são "
        "necessários acreção, condições de contorno absorventes, energia/temperatura, "
        "transporte, composição e relatividade com matéria; uma atmosfera mantida "
        "estática sobre o horizonte não é demonstrada por este ensaio.", "",
        "[F/?] Sismologia poderia testar as faixas de f por tempos de viagem, "
        "modos normais, estrutura/raio do núcleo e velocidades elásticas recalculadas "
        "com EOS, além de momento de inércia. A família PREM escalada dá "
        "I_f=(1−f)I0: mesmo com g superficial idêntica, muda uma restrição global. "
        "PREM é um modelo de referência; seus coeficientes não trazem aqui uma "
        "covariância que permita excluir quantitativamente cada faixa. "
        "Não se infere f_max de percentuais arbitrários. As singularidades impedem "
        "uma extensão regular do toy model, mas não constituem, sozinhas, "
        "um limite observacional universal para um BH com fluxo de acreção.", "",
        "[H] C5B-QO não foi incorporada às equações. Uma proposta de regularização "
        "precisaria demonstrar em equações como remove a singularidade, preserva "
        "conservação, recupera GR em domínios testados e prevê observáveis novos. "
        "Ajustar uma solução não é evidência experimental. Não há conclusão de "
        "que exista um BH na Terra.", "",
        f"Validação: rs(f=1)={1000*schwarzschild_radius(1):.6f} mm; conservação de massa, "
        "quadratura independente da pressão, duplicação da resolução, mudança de "
        "passo/tolerância ODE e solução analítica politrópica verificadas. "
        "Os erros efetivos estão em validacao.json. Os testes executáveis incluem "
        "esfera uniforme, identidade de perturbação e horizonte excluído.", ""]
    (out/"relatorio.md").write_text("\n".join(lines), encoding="utf-8")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir())
              if p.is_file() and p.name != "manifesto_sha256.json"}
    write_json(out/"manifesto_sha256.json", hashes)
    print(json.dumps({"output": str(out), "casos_PREM": len(fs), "validacao": True,
                      "rs_f1_mm": 1000*schwarzschild_radius(1), "f_max_observacional": None}, ensure_ascii=False))


if __name__ == "__main__":
    main()
