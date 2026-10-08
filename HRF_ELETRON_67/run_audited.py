"""Run the complete supplied E67 pipeline and audit every uncertainty bound."""
import json
import os
from pathlib import Path
import platform
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
OUT = ROOT
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import scipy
import e67_rodar as suite

original_entropy = suite.entropia_gauge
original_job = suite.job
calls = 0
minimum = 1.0
started = 0.0
case_name = ''


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


def tracked_entropy(*args, **kwargs):
    global calls, minimum
    result = original_entropy(*args, **kwargs)
    calls += 1
    minimum = min(minimum, float(result[1]))
    if calls % 25 == 0:
        print(f'PROGRESS {case_name}: {calls} entropy regions, '
              f'nu_min={minimum:.12f}, elapsed={time.monotonic()-started:.1f}s', flush=True)
    return result


def tracked_job(spec):
    global calls, minimum, started, case_name
    calls, minimum, started = 0, 1.0, time.monotonic()
    case_name = f'{spec[0]}_{spec[1]:g}'
    suite.entropia_gauge = tracked_entropy
    print(f'START {case_name}', flush=True)
    record = dict(case=case_name, started_unix=time.time(), pid=os.getpid())
    try:
        result = original_job(spec)
        record['execution_status'] = 'COMPLETED'
        return result
    except BaseException:
        record['execution_status'] = 'FAILED'
        record['traceback'] = traceback.format_exc()
        raise
    finally:
        record.update(entropy_region_calls=calls, nu_min_all_calls=minimum,
                      Vnu_same_original_tolerance_ok=minimum >= .5 - 1e-9,
                      wall_seconds=time.monotonic()-started)
        save(OUT/'auditoria'/f'{case_name}.json', record)
        print(f"END {case_name}: {record['execution_status']}, {record['wall_seconds']:.1f}s", flush=True)


def main():
    if list((OUT/'dados').glob('*.json')) or list((OUT/'auditoria').glob('*.json')) or (OUT/'resultados'/'E67_resumo.json').exists() or (OUT/'resultados'/'log_execucao.txt').exists():
        raise FileExistsError('Refusing to overwrite an existing E67 execution')
    OUT.mkdir(parents=True, exist_ok=True)
    save(OUT/'ambiente.json', dict(python=sys.version, numpy=np.__version__,
                                 scipy=scipy.__version__, platform=platform.platform(),
                                 mode='FULL', processes=2, thread_limit=1,
                                 github_run_id=os.environ.get('GITHUB_RUN_ID'),
                                 github_commit=os.environ.get('GITHUB_SHA'),
                                 github_repository=os.environ.get('GITHUB_REPOSITORY')))
    suite.job = tracked_job
    suite.main()


if __name__ == '__main__':
    main()
