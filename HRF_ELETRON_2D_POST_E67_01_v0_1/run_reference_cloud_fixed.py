"""Full, unmodified E67 repeat with all-region nu tracking. Run on a cloud runner.
No credentials are included. This does not run extension cases or freeze a protocol.
"""
from pathlib import Path
import os, sys, zipfile, hashlib, json, time, platform, traceback

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reference_repeat'
def main():
    if os.environ.get('GITHUB_ACTIONS')!='true':
        raise SystemExit('Run this resource-intensive job on GitHub Actions.')
    OUT.mkdir(exist_ok=False)
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
        os.environ[key]='1'
    with zipfile.ZipFile(ROOT/'originals/E67_source.zip') as z: z.extractall(OUT)
    base=OUT/'HRF_ELETRON_67'
    check=[]
    for line in (base/'hashes_antes_da_execucao.txt').read_text().splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        digest,name=line.split(maxsplit=1);name=name.lstrip('*')
        p=base/name
        ok=hashlib.sha256(p.read_bytes()).hexdigest()==digest
        check.append({'path':name,'ok':ok})
    assert all(x['ok'] for x in check),'Source hash mismatch'
    sys.path.insert(0,str(base/'src'))
    import numpy as np
    import scipy
    import e67_rodar as runner
    import avaliar_e67 as evaluator
    original=runner.entropia_gauge
    calls=[]
    def tracked(*args,**kwargs):
        val=original(*args,**kwargs)
        calls.append(float(val[1]))
        return val
    runner.entropia_gauge=tracked
    env={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),'commit':os.environ.get('GITHUB_SHA'),'run':os.environ.get('GITHUB_RUN_ID'),'serial_cases':True}
    (OUT/'environment.json').write_text(json.dumps(env,indent=2))
    aud=[]
    try:
        for spec in [('aperto',float(w)) for w in range(4,8)]+[('padrao',4.),('padrao',5.),('vmais',5.)]:
            calls.clear();t=time.monotonic();runner.job(spec)
            aud.append({'case':spec,'calls':len(calls),'min_nu':min(calls),'seconds':time.monotonic()-t,'Vnu':min(calls)>=.5-1e-9})
            (OUT/'all_region_audit.json').write_text(json.dumps(aud,indent=2))
        evaluator.main()
        (OUT/'status.json').write_text(json.dumps({'execution':'COMPLETED','comparison_to_archive':'PENDING','extension_gate':'PENDING','closure_w7':'NOT_MEASURED'}))
    except BaseException:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise
    finally:
        after=[{'path':x['path'],'sha256':hashlib.sha256((base/x['path']).read_bytes()).hexdigest()} for x in check]
        (OUT/'source_hashes_after.json').write_text(json.dumps(after,indent=2))
if __name__=='__main__': main()
