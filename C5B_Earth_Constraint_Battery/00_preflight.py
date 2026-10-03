"""Inspect supplied inputs; rounded-report regression can replace unavailable CSVs."""
import hashlib,json,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def main():
    p=json.loads((ROOT/'parameters.json').read_text());source=ROOT/'data/C5B_QO_QW02_Open_Closed_Cavity_Local.md';prem=ROOT.parent/'c5b_qo/study.py'
    a=source.exists() and hashlib.sha256(source.read_bytes()).hexdigest()==p['QW02']['expected_report_sha256']
    b=prem.exists() and hashlib.sha256(prem.read_bytes()).hexdigest()==p['expected_PREM_sha256']
    regression=ROOT/'results/regression_QW02.json';passed=regression.exists() and json.loads(regression.read_text()).get('passed')
    result={'status':'QW02_REPORT_REGRESSION_PASSED' if a and b and passed else 'INPUTS_OR_REGRESSION_NOT_READY','QW02_report_hash_verified':a,'PREM_original_hash_verified':b,'QW02_original_CSVs_supplied':False,'regression_basis':'18 rounded values printed in supplied QW02 report','QW02_report_regression_passed':bool(passed),'dependencies_available':{name:importlib.util.find_spec(name) is not None for name in ['numpy','scipy','sympy','matplotlib']},'scientific_stages_completed':json.loads((ROOT/'results/stage_progress.json').read_text()) if (ROOT/'results/stage_progress.json').exists() else []}
    (ROOT/'results/preflight.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    return 0 if a and b and passed else 2
if __name__=='__main__':raise SystemExit(main())
