"""Compare a freshly computed reference with archived data, without changing E67."""
from pathlib import Path
import json, math, hashlib, shutil, subprocess, sys, csv, os
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'reference_repeat'
HIST = ROOT / 'historical_inputs'
FRESH = OUT / 'HRF_ELETRON_67'
CONFIG = json.loads((ROOT / 'EXECUTION_REGISTRATION.json').read_text())

def clean(x):
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    if isinstance(x, float) and not math.isfinite(x): return None
    return x

def write(name, x):
    (OUT / name).write_text(json.dumps(clean(x), indent=2, ensure_ascii=False, allow_nan=False) + '\n')

def compare(a, b, atol, rtol, allow_nan=()):
    report = {'status': 'PASS', 'numeric_values': 0, 'max_absolute_difference': 0., 'max_fraction_of_tolerance': 0., 'differences': [], 'allowed_historical_NaN': []}
    def fail(path, reason): report['differences'].append({'path': path, 'reason': reason})
    def walk(x, y, path):
        if isinstance(x, dict) and isinstance(y, dict):
            if x.keys() != y.keys(): fail(path, 'keys')
            for k in sorted(x.keys() & y.keys()): walk(x[k], y[k], path + '/' + k)
        elif isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y): fail(path, 'length')
            for i, (u, v) in enumerate(zip(x, y)): walk(u, v, path + '/' + str(i))
        elif isinstance(x, (float, int)) and not isinstance(x, bool) and isinstance(y, (float, int)) and not isinstance(y, bool):
            if not math.isfinite(x) or not math.isfinite(y):
                if path in allow_nan and math.isnan(x) and math.isnan(y): report['allowed_historical_NaN'].append(path)
                else: fail(path, 'nonfinite')
                return
            error = abs(x - y); tolerance = atol + rtol * abs(y)
            report['numeric_values'] += 1
            report['max_absolute_difference'] = max(report['max_absolute_difference'], error)
            report['max_fraction_of_tolerance'] = max(report['max_fraction_of_tolerance'], error / tolerance)
            if error > tolerance: fail(path, 'numeric tolerance')
        elif type(x) != type(y) or x != y: fail(path, 'exact value')
    walk(a, b, '')
    if report['differences']: report['status'] = 'FAIL'
    return report

def main():
    atol = CONFIG['raw_data_comparison']['atol']; rtol = CONFIG['raw_data_comparison']['rtol']
    results = []
    for case in CONFIG['cases']:
        a = json.loads((FRESH / 'dados' / (case + '.json')).read_text())
        b = json.loads((HIST / 'dados' / (case + '.json')).read_text())
        q = compare(a, b, atol, rtol); q['case'] = case; results.append(q)
    replay = OUT / 'archival_evaluator_replay'; replay.mkdir(exist_ok=False)
    shutil.copytree(FRESH / 'src', replay / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(HIST / 'dados', replay / 'dados'); (replay / 'resultados').mkdir()
    proc = subprocess.run([sys.executable, str(replay / 'src/avaliar_e67.py')], capture_output=True, text=True, check=True)
    (OUT / 'archival_evaluator_stdout.txt').write_text(proc.stdout)
    a = json.loads((FRESH / 'resultados/E67_resumo.json').read_text())
    b = json.loads((HIST / 'E67_resumo.json').read_text())
    allow = CONFIG['historical_NaN_allowlist']
    summary = compare(a, b, atol, rtol, allow)
    archive_replay = compare(json.loads((replay / 'resultados/E67_resumo.json').read_text()), b, 1e-10, 1e-10, allow)
    exact_decisions = a['decisoes'] == b['decisoes']
    audit = json.loads((OUT / 'all_region_audit.json').read_text())
    counts = {f"{q['case'][0]}_{q['case'][1]:g}": q['calls'] for q in audit}
    all_nu = all(q['Vnu'] and math.isfinite(q['min_nu']) for q in audit)
    hashes = json.loads((OUT / 'source_hashes_after.json').read_text())
    originals = {}
    for line in (FRESH / 'hashes_antes_da_execucao.txt').read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            digest, name = line.split(maxsplit=1); originals[name.lstrip('*')] = digest
    hashes_ok = len(hashes) == len(originals) and all(q['sha256'] == originals[q['path']] for q in hashes)
    ok = all(q['status'] == 'PASS' for q in results) and summary['status'] == 'PASS' and archive_replay['status'] == 'PASS' and exact_decisions and counts == CONFIG['expected_entropy_calls'] and all_nu and hashes_ok
    comparison = {'measurement_tag': '[M]', 'scope': 'Fresh full 64x74 covariance computation; stored entropies, probes, energies, centered profiles, maps and evaluator metrics compared. Full covariance matrices are not stored or independently compared.', 'atol': atol, 'rtol': rtol, 'raw_cases': results, 'evaluator_metrics': summary, 'archival_evaluator_replay': archive_replay, 'decisions_identical': exact_decisions, 'entropy_calls': counts, 'entropy_calls_total': sum(counts.values()), 'all_regions_nu_pass': all_nu, 'min_nu_all_regions': min(q['min_nu'] for q in audit), 'source_hashes_after_match': hashes_ok, 'source_hash_count': len(hashes), 'status': 'PASS' if ok else 'FAIL'}
    write('COMPARISON_TO_ARCHIVE.json', comparison)
    write('E67_resumo_JSON_PADRAO.json', a)
    annotation = {'measurement_tag': '[M]', 'H67': 'SIM — regime não linear' if all(a['validacoes'][k]['ok'] for k in ['V0_lei_de_area', 'Vnu', 'VK', 'Vmais_fecho', 'VC_controles_grudados']) and a['decisoes']['H67-N (objeto do bulk × grudado)'] == 'NORMALIZÁVEL' and a['decisoes']['H67-Z (profundidade ∝ tamanho)'] == 'PROPORCIONAL' and not a['validacoes']['VL_linearidade']['ok'] else a['decisoes']['H67 (partícula no bulk)'], 'H67_N': a['decisoes']['H67-N (objeto do bulk × grudado)'], 'H67_Z': a['decisoes']['H67-Z (profundidade ∝ tamanho)'], 'VL': 'PASS' if a['validacoes']['VL_linearidade']['ok'] else 'FAIL', 'closure_w7': 'NOT_MEASURED', 'original_evaluator_preserved': True, 'historical_thresholds_unchanged': True}
    write('DECISAO_CONFORME_PROTOCOLO.json', annotation)
    rows = []
    for w in range(4, 8):
        q = a['aperto'][f'w{w}']; v = q['0.25']; rows.append({'w': w, 'p_min': v['p_min'], 'class': v['classe_N'], 'z': v['z_centroide'], 'VL': q['linearidade'], 'closure': clean(v['fecho']), 'closure_status': 'NOT_MEASURED' if w == 7 else ('PASS' if v['fecho'] <= .01 else 'FAIL')})
    with (OUT / 'reference_metrics.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    status = {'measurement_tag': '[M]', 'reference_computation': 'COMPLETED', 'comparison_to_archive': comparison['status'], 'A1': archive_replay['status'], 'A2': 'COMPLETED', 'A3': comparison['status'], 'B0': 'REFERENCE_RESOURCES_MEASURED_SCALABLE_IMPLEMENTATION_NOT_VALIDATED', 'extension_protocol': 'DRAFT_NOT_FROZEN', 'finite_size': 'NOT_EXECUTED', 'spatial_refinement': 'NOT_EXECUTED', 'closure_w7': 'NOT_MEASURED', 'dynamic_phase': 'PENDING', 'robustness_question': 'OPEN', 'remaining_gates': ['Validate scalable implementation before large-network execution', 'Freeze extension configuration, source, evaluator and resource budget before new measurements'], 'execution_repository': 'GraceKekey/my-ai-workflow', 'github_sha': os.environ.get('GITHUB_SHA'), 'github_run_id': os.environ.get('GITHUB_RUN_ID')}
    write('STATUS_VERIFICADO.json', status)
    print(json.dumps({'comparison': comparison['status'], 'numeric_values': sum(q['numeric_values'] for q in results), 'max_abs_raw_error': max(q['max_absolute_difference'] for q in results), 'calls': sum(counts.values()), 'decisions': annotation}, ensure_ascii=False))
    if not ok: raise SystemExit('Reference comparison or integrity audit failed; negative results retained.')

if __name__ == '__main__': main()
