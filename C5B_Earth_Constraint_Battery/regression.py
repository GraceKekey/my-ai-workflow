"""References transcribed from the supplied QW02 Markdown, not fabricated CSVs."""
import numpy as np
from core import *


def run():
    verify_prem()
    source=ROOT/'data/C5B_QO_QW02_Open_Closed_Cavity_Local.md'
    if not source.is_file():raise FileNotFoundError('Relatório QW02 ausente')
    report_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    expected=PARAMS['QW02'].get('expected_report_sha256')
    if expected and report_hash!=expected:raise RuntimeError('Relatório QW02 alterado')
    rows=[];f=1e-8;r0=2*G*f*M/C**2
    rows.append(dict(test='r0',expected=8.8701029e-11,calculated=r0,tolerance_rel=2e-8))
    cases=[('open',1,4.8717451e20),('closed',1.001,3.6035366e22),('closed',1.01,1.0643951e22),('closed',2,4.8717451e20),('open',2,2.6433218e20),('open',100,5.8660882e18),('closed',100,5.9251931e18)]
    for state,kappa,expected in cases:
        p,d=pressure(f,kappa*r0,state)
        rows.append(dict(test=f'pressure_{state}_kappa_{kappa}',expected=expected,calculated=p,tolerance_rel=2e-6))
    refs=[(1e-10,.1,.01433),(1e-10,.01,.14332),(1e-8,.1,1.433),(1e-8,.01,14.331),(1e-6,.1,143.309),(1e-6,.01,1432.),(1e-4,.1,14268.),(1e-4,.01,137567.),(1e-3,.1,137686.),(1e-3,.01,1153685.)]
    for f,tol,expected in refs:
        calc=cavity_threshold(f,tol)['rc_m']
        rows.append(dict(test=f'cavity_f_{f}_tol_{tol}',expected=expected,calculated=calc,tolerance_rel=.001))
    for row in rows:
        row['relative_error']=abs(row['calculated']/row['expected']-1)
        row['passed']=bool(row['relative_error']<=row['tolerance_rel'])
    result={'passed':all(r['passed'] for r in rows),'source':'data/C5B_QO_QW02_Open_Closed_Cavity_Local.md','reference_type':'Rounded values explicitly printed in supplied report; original CSVs and QW02 code not supplied','implementation':'Cavity-normalized matter-only TOV; additive log lapse and mass function as QW01; not a self-consistent perfect-fluid combined GR solution','cases':rows}
    result['source_sha256']=report_hash
    save_json('results/regression_QW02.json',result);write_csv('tables/regression_QW02.csv',rows)
    print(json.dumps(result,indent=2));return result['passed']

if __name__=='__main__':raise SystemExit(0 if run() else 1)
