"""Executa a grade somente após testes válidos e entrega um ZIP verificado."""
from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import zipfile

import numpy as np
import scipy
from scipy.integrate import quad
from prem_adapter import ROOT, PREM_PATH, prem, verify_source, source_hash, G, C, M, R
from geometry import (F_VALUES, ALPHA_BASE, ALPHA_REFINED, ALPHA_MIN_SWITCH, STRESS,
                      parameters, isolated, nec_minimum, negative_nec_budget, negative_energy_budget)
from earth import profile, composed, reference, pressure_ode, SAMPLES, RHOC
from outputs import make_plots, make_report


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_gate():
    verify_source()
    spec = importlib.util.spec_from_file_location("qw_test_gate", ROOT/"tests/test_c5b_qo_qw01.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    path = ROOT/"results/test_results.json"
    if not path.exists():
        raise RuntimeError("Execute tests/test_c5b_qo_qw01.py antes da grade.")
    record = json.loads(path.read_text())
    if not record.get("passed") or record["code_hashes"] != module.code_hashes():
        raise RuntimeError("Testes falharam ou o código mudou; rode os testes atuais antes da grade.")
    return record


def row_for(f, alpha, p, fine, case_id):
    mu = G*f*M/C**2
    r0 = alpha*mu if f else 0.
    mm = float(composed([R], f, alpha, r0)["m_matter"][0])
    pref = p["P_Pa"][0]
    change = abs(pref/fine["P_Pa"][0]-1)
    maximum = float(np.max(p["P_Pa"]))
    gs = float(p["g"][-1])
    g0s = float(composed([R], 0., None, 0.)["g"][0])
    info = {"case_id": case_id, "f": f, "M_W_kg": f*M, "M_matter_kg": mm,
            "mass_relative_error": abs(mm+f*M-M)/M,
            "mu_m": mu, "alpha": alpha, "r0_m": r0,
            "A_throat_W": None, "A_throat_total": None, "bprime_throat_W": None,
            "flare_out_OK": None, "horizon": False,
            "g_surface_m_s2": gs, "relative_g_surface": (gs-g0s)/g0s,
            "g_100km_m_s2": None, "relative_g_100km": None,
            "g_0_1R_m_s2": None, "Pmax_Pa": maximum,
            "P_throat_Pa": None, "P_near_1_001r0_Pa": None,
            "P_throat_rho_c2_ratio": None, "P_throat_to_PREM_center": None,
            "Ricci_throat_W_m2": None, "Ricci2_throat_W_m4": None,
            "Kretsch_throat_W_m4": None, "Ricci_throat_total_m2": None,
            "Ricci2_throat_total_m4": None, "Kretsch_throat_total_m4": None,
            "NEC_min_W_Pa": None, "r_NEC_min_over_r0": None,
            "NEC_min_exotic_composed_near_isolated_min_Pa": None,
            "NEC_negative_radial_width_m": "não aplicável",
            "NEC_negative_proper_volume_one_mouth_J": 0.,
            "negative_energy_density_volume_one_mouth_J": 0.,
            "NEC_budget_over_MW_c2": None,
            "proper_distance_throat_to_2r0_m": None,
            "pressure_resolution_change_rel": change,
            "regular_throat": None, "numerically_valid": True,
            "physical_EOS_verified": False, "dynamic_stability": "não calculada",
            "mathematical_status": "referência PREM GR" if not f else "garganta regular; fonte exótica requerida"}
    for label, r in SAMPLES.items():
        idx = int(np.argmin(abs(p["r"]-r)))
        g = float(p["g"][idx])
        g0 = float(composed([r], 0., None, 0.)["g"][0])
        if label == "100km":
            info["g_100km_m_s2"], info["relative_g_100km"] = g, (g-g0)/g0
        if label == "0_1R":
            info["g_0_1R_m_s2"] = g
    if f:
        w = isolated(1., alpha)
        nmin, y_min = nec_minimum(alpha)
        budget, err = negative_nec_budget(alpha)
        eneg = negative_energy_budget(alpha)
        Pnear = float(np.interp(np.log(1.001*r0), np.log(p["r"]), p["P_Pa"]))
        i = int(np.argmin(abs(np.log(p["r"]/r0)-np.log(y_min))))
        length = r0*quad(lambda z: 2*(1+z*z)/np.sqrt(1+z*z+1-2/alpha), 0, 1,
                         epsrel=1e-10)[0]
        info.update({"A_throat_W": float(w["A"]), "A_throat_total": float(p["A"][0]),
            "bprime_throat_W": 2/alpha-1, "flare_out_OK": bool(2/alpha-1 < 1),
            "P_throat_Pa": float(pref), "P_near_1_001r0_Pa": Pnear,
            "P_throat_rho_c2_ratio": float(pref/(p["rho"][0]*C*C)),
            "P_throat_to_PREM_center": float(pref/reference(0.).evaluate([1e-6])["p"][0]),
            "Ricci_throat_W_m2": float(w["ricci_scaled"])/r0**2,
            "Ricci2_throat_W_m4": float(w["ricci2_scaled"])/r0**4,
            "Kretsch_throat_W_m4": float(w["kretsch_scaled"])/r0**4,
            "Ricci_throat_total_m2": float(p["Ricci_m2"][0]),
            "Ricci2_throat_total_m4": float(p["Ricci2_m4"][0]),
            "Kretsch_throat_total_m4": float(p["Kretsch_m4"][0]),
            "NEC_min_W_Pa": float(nmin)*STRESS/r0**2,
            "r_NEC_min_over_r0": y_min,
            "NEC_min_exotic_composed_near_isolated_min_Pa": float(p["NEC_exotic_Pa"][i]),
            "NEC_negative_radial_width_m": "infinita (analítico; cauda em todo r>=r0)",
            "NEC_negative_proper_volume_one_mouth_J": 4*np.pi*STRESS*r0*budget,
            "negative_energy_density_volume_one_mouth_J": 4*np.pi*STRESS*r0*eneg,
            "NEC_budget_over_MW_c2": alpha*budget/2,
            "proper_distance_throat_to_2r0_m": length,
            "regular_throat": True})
    if info["mass_relative_error"] > 1e-13 or change > 2e-6:
        raise RuntimeError(f"Caso {case_id}: massa ou convergência inválida")
    if np.any(p["P_Pa"] < -1e-6):
        raise RuntimeError(f"Caso {case_id}: pressão inesperadamente negativa")
    for field, values in p.items():
        if not np.isfinite(values).all():
            raise RuntimeError(f"Caso {case_id}: NaN/Inf em {field}")
    return info


def make_zip(root):
    target = root.parent/"C5B_QO_QW01.zip"
    files = [p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            z.write(p, "c5b_qo_qw01/"+str(p.relative_to(root)))
        z.write(PREM_PATH, "c5b_qo/study.py")
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise RuntimeError("Falha de integridade no ZIP")
    return target


def main():
    tests = test_gate()
    for name in ["data", "results", "plots", "report"]:
        (ROOT/name).mkdir(exist_ok=True)
    metadata = {"project": "C5B-QO-QW01", "G": G, "c": C, "M_earth": M, "R_earth": R,
        "f": F_VALUES, "alpha_initial": ALPHA_BASE, "alpha_refined": ALPHA_REFINED,
        "alpha_NEC_min_location_transition": ALPHA_MIN_SWITCH,
        "refinement_reason": "limite alpha=1; sinal E_W em alpha=2; mínimo NEC sai da garganta",
        "radial_resolutions": [650, 1300], "PREM_sha256": source_hash(),
        "PREM_source_commit": "313e3e7db01c64be08091172c5c6f4e6d5bdda86",
        "PREM_layers": prem.LAYERS, "PREM_normalization": prem.NORMALIZATION,
        "metric_composition": "b=bW+2Gm_mat/c²; Phi=PhiW+Phi_E(TOV prescrito)",
        "mass_convention": "massa gravitacional em volume areal; não massa bariônica própria",
        "TOV_rtol": 2e-11, "TOV_max_step_log_r": 1.,
        "NEC_volume": "uma boca isolada até infinito; volume próprio; não ANEC",
        "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__}
    write_json(ROOT/"data/parameters.json", metadata)
    write_json(ROOT/"data/PREM_SOURCE.json", {"path": "../c5b_qo/study.py",
        "sha256": source_hash(), "unchanged": True, "source": "doi:10.1016/0031-9201(81)90046-7"})
    rows, samples, checks, selected = [], [], [], []
    pairs = [(0., None)]+[(f, a) for f in F_VALUES[1:] for a in ALPHA_REFINED]
    baseline = None
    for number, (f, a) in enumerate(pairs):
        p = profile(f, a, 650)
        fine = profile(f, a, 1300)
        row = row_for(f, a, p, fine, number)
        rows.append(row)
        if not f:
            baseline = p
        if f and (a == 2. or (f == 1e-8 and a in ALPHA_BASE)):
            selected.append((f, a, p))
            export = ["r", "g", "gW_isolated", "rho", "P_Pa", "deltaP_Pa", "A", "F", "b_r",
                      "NEC_W_Pa", "NEC_exotic_Pa", "NEC_total_Pa", "Ricci_m2", "Ricci2_m4", "Kretsch_m4"]
            write_csv(ROOT/f"results/profile_f_{f:g}_alpha_{a:g}.csv",
                [{key: float(p[key][i]) for key in export} for i in range(len(p["r"]))])
        for label, r in SAMPLES.items():
            i = int(np.argmin(abs(p["r"]-r)))
            j = int(np.argmin(abs(fine["r"]-r)))
            g0 = float(composed([r], 0., None, 0.)["g"][0])
            g = float(p["g"][i])
            point = float(prem.gravity(r, f))
            samples.append({"case_id": number, "f": f, "alpha": a, "sample": label,
                "r_m": r, "g_QW_m_s2": g, "g_PREM_GR_m_s2": g0,
                "delta_g_m_s2": g-g0, "relative_g_PREM_GR": (g-g0)/g0,
                "g_previous_point_Newton_m_s2": point,
                "relative_QW_to_previous_point_Newton": (g-point)/point,
                "P_QW_Pa": float(p["P_Pa"][i]),
                "pressure_resolution_relative_change": abs(p["P_Pa"][i]-fine["P_Pa"][j])/
                                                          max(1., abs(fine["P_Pa"][j]))})
        checks.append({"case_id": number, "f": f, "alpha": a,
                       "mass_relative_error": row["mass_relative_error"],
                       "pressure_resolution_change_rel": row["pressure_resolution_change_rel"],
                       "finite_arrays": True, "P_nonnegative": True})
        if number % 16 == 0 or number == len(pairs)-1:
            print(f"Grade: {number+1}/{len(pairs)} casos validados", flush=True)
    summary = [r for r in rows if not r["f"] or r["alpha"] in ALPHA_BASE]
    write_csv(ROOT/"results/summary.csv", summary)
    write_csv(ROOT/"results/full_grid.csv", rows)
    write_csv(ROOT/"results/earth_samples.csv", samples)
    odechecks = []
    for f, a in [(1e-10, 1.01), (1e-8, 2.), (1e-3, 100.)]:
        exact = pressure_ode(f, a)
        r = next(v for v in rows if v["f"] == f and v["alpha"] == a)
        error = abs(r["P_throat_Pa"]/exact-1)
        if error > 2e-6:
            raise RuntimeError("Falha de validação independente da pressão")
        odechecks.append({"f": f, "alpha": a, "P_ODE_Pa": exact, "relative_error": error})
    asym = [abs(a*1e8**2*float(isolated(1e8, a)["g_r0_c2"])-1) for a in ALPHA_REFINED]
    maxsamplechange = max(s["pressure_resolution_relative_change"] for s in samples)
    if maxsamplechange > 2e-6:
        raise RuntimeError("Pressão nos raios terrestres não convergiu")
    validation = {"status": "EXECUÇÃO CONCLUÍDA", "cases_executed": len(rows),
        "cases_valid": len(rows), "wormholes_valid": len(rows)-1, "initial_grid_cases": len(summary),
        "tests": tests, "max_mass_relative_error": max(r["mass_relative_error"] for r in rows),
        "max_pressure_resolution_relative_change": max(r["pressure_resolution_change_rel"] for r in rows),
        "max_earth_sample_pressure_resolution_change": maxsamplechange,
        "max_pressure_ode_relative_error": max(v["relative_error"] for v in odechecks),
        "max_asymptotic_g_relative_error": max(asym),
        "PREM_source_verified": verify_source(), "case_checks": checks, "pressure_ODE": odechecks,
        "all_finite": True, "horizons_found": 0,
        "NEC_negative_width": "infinita no modelo isolado para cada alpha>1",
        "dynamical_stability_proven": False, "terrestrial_EOS_verified": False,
        "observational_f_max": None, "pressure_extreme_but_finite": True,
        "exotic_budget_definition": "-∫min(NEC_W,0)dV próprio; uma boca isolada até infinito",
        "boundary_alpha_1": "flare-out estrito falha; limite de distância própria infinita; A>0",
        "boundary_alpha_below_1": "F<0 em parte de r>=r0; família não admitida"}
    make_plots(ROOT, selected, baseline)
    make_report(ROOT, rows, validation, tests)
    required = [ROOT/"README.md", ROOT/"src/run_c5b_qo_qw01.py", ROOT/"tests/test_c5b_qo_qw01.py",
        ROOT/"results/summary.csv", ROOT/"results/full_grid.csv",
        ROOT/"report/C5B_QO_QW01_REPORT.md", ROOT/"report/symbolic_derivations.json"]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError("Artefato ausente: "+str(path))
    if len(list((ROOT/"plots").glob("*.png"))) < 12 or len(list((ROOT/"plots").glob("*.pdf"))) < 12:
        raise RuntimeError("Gráficos incompletos")
    validation["artifacts_verified"] = True
    write_json(ROOT/"results/validation.json", validation)
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(ROOT.rglob("*")) if p.is_file() and "__pycache__" not in p.parts
                and p.name != "manifest_sha256.json"}
    write_json(ROOT/"results/manifest_sha256.json", manifest)
    archive = make_zip(ROOT)
    print(json.dumps({"STATUS": "EXECUÇÃO CONCLUÍDA", "cases": len(rows), "valid": len(rows),
                      "tests_passed": tests["tests_run"], "ZIP": str(archive),
                      "ZIP_bytes": archive.stat().st_size}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        (ROOT/"results").mkdir(exist_ok=True)
        write_json(ROOT/"results/validation.json", {"status": "EXECUÇÃO FALHOU", "error": str(error)})
        print("STATUS: EXECUÇÃO FALHOU — "+str(error), file=sys.stderr)
        sys.exit(1)
