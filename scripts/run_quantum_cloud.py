"""Pass workflow inputs as literal arguments; enforce an external wall-clock limit."""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quantum.resources import Config


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('this launcher is only for GitHub Actions')
    seconds = int(os.environ.get('MAX_SECONDS', '600'))
    if not 60 <= seconds <= 2400:
        raise ValueError('MAX_SECONDS must be in [60,2400]')
    command = [sys.executable, '-m', 'quantum.run', '--output', 'results']
    for name in Config.__dataclass_fields__:
        value = os.environ.get(name.upper())
        if value:
            command.extend(['--' + name.replace('_', '-'), value])
    try:
        return subprocess.run(command, check=False, timeout=seconds).returncode
    except subprocess.TimeoutExpired:
        from quantum.run import write_json
        write_json(Path('results/status.json'), {'status': 'timed_out', 'calculation_completed': False,
                                                'error': 'external wall-clock limit exceeded; resume saved checkpoints'})
        print('Wall-clock limit reached; completed-grid checkpoints preserved.', flush=True)
        return 124


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, RuntimeError) as error:
        print(f'Invalid cloud configuration: {error}', file=sys.stderr)
        sys.exit(2)
