"""Lightweight validation and resource planning (no numerical dependencies)."""

from dataclasses import asdict, dataclass
import math
import os


@dataclass(frozen=True)
class Config:
    grid_points: int = 4095
    states: int = 6
    half_width: float = 8.0
    levels: int = 3
    mass: float = 1.0
    omega: float = 1.0
    hbar: float = 1.0
    max_seconds: int = 600
    memory_mb: int = 4096

    def validate(self):
        for name in ('grid_points', 'states', 'levels', 'max_seconds', 'memory_mb'):
            if type(getattr(self, name)) is not int:
                raise ValueError(f'{name} must be an integer')
        if not 127 <= self.grid_points <= 200_000:
            raise ValueError('grid_points must be in [127, 200000]')
        if not 1 <= self.states <= 32 or not 3 <= self.levels <= 5:
            raise ValueError('states must be in [1,32]; levels in [3,5]')
        if (self.grid_points + 1) % 2 ** (self.levels - 1):
            raise ValueError('grid_points + 1 must be divisible by 2**(levels-1)')
        if self.grids()[0] < max(31, 2 * self.states + 1):
            raise ValueError('coarsest grid is too small for the requested states')
        if not math.isfinite(self.half_width) or not 3 <= self.half_width <= 20:
            raise ValueError('half_width must be finite and in [3,20] oscillator lengths')
        for name in ('mass', 'omega', 'hbar'):
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f'{name} must be finite and positive')
        length, energy = self.scales()
        if not all(math.isfinite(v) and v > 0 for v in (length, energy)):
            raise ValueError('physical scales overflow or underflow float64')
        if not 60 <= self.max_seconds <= 2400:
            raise ValueError('max_seconds must be in [60,2400]')
        if not 256 <= self.memory_mb <= 4096:
            raise ValueError('memory_mb must be in [256,4096]')
        return self

    def grids(self):
        return [(self.grid_points + 1) // 2**i - 1
                for i in reversed(range(self.levels))]

    def scales(self):
        # Logarithms avoid overflow in intermediate products for SI inputs.
        length = math.exp((math.log(self.hbar) - math.log(self.mass)
                           - math.log(self.omega)) / 2)
        energy = self.hbar * self.omega
        return length, energy

    def domain_grid(self):
        return round(1.25 * (self.grid_points + 1)) - 1


def estimate_memory_mb(n, states):
    """Conservative float64 CSC/LU, ARPACK workspace, arrays and plotting allowance."""
    ncv = min(n, max(20, 2 * states + 1))
    return 512 + (8 * n * (4 * ncv + 16 * states + 80)
                  + 8 * ncv * ncv) / 1024**2


def available_memory_mb():
    """Use available memory and, on Linux, any tighter cgroup limit."""
    values = []
    try:
        with open('/proc/meminfo', encoding='utf-8') as stream:
            for line in stream:
                if line.startswith('MemAvailable:'):
                    values.append(int(line.split()[1]) / 1024)
        with open('/sys/fs/cgroup/memory.max', encoding='utf-8') as stream:
            maximum = stream.read().strip()
        if maximum != 'max':
            with open('/sys/fs/cgroup/memory.current', encoding='utf-8') as stream:
                used = int(stream.read())
            values.append(max(0, (int(maximum) - used) / 1024**2))
    except (OSError, ValueError):
        pass
    return min(values) if values else None


def plan(config, pilot_seconds=None, available_mb=None):
    config.validate()
    grids = config.grids() + [config.domain_grid()]
    memory = [estimate_memory_mb(n, config.states) for n in grids]
    budget = config.memory_mb
    if available_mb is not None:
        budget = min(budget, 0.6 * available_mb)
    # Measured at 255 points; linear scaling is a heuristic, not a guarantee.
    seconds = None if pilot_seconds is None else [
        2 + 10 * max(pilot_seconds, 0.02) * n / 255 for n in grids]
    result = {'parameters': asdict(config), 'grids': grids,
              'estimated_peak_mb_per_grid': memory, 'memory_budget_mb': budget,
              'estimated_seconds_per_grid': seconds,
              'estimated_total_seconds': None if seconds is None else sum(seconds) + 30,
              'pilot_seconds': pilot_seconds, 'cpu_count': os.cpu_count(),
              'memory_model': '512 MiB + 8*N*(4*ncv+16*k+80) + 8*ncv**2 bytes',
              'time_model': '10x measured 255-point solve scaled linearly + 2s/grid + 30s output',
              'time_estimate_is_guarantee': False}
    if max(memory) > budget:
        raise ValueError(f'estimated memory {max(memory):.1f} MiB exceeds budget {budget:.1f} MiB')
    if seconds is not None and sum(seconds) + 30 > config.max_seconds * 0.8:
        raise ValueError('estimated runtime exceeds 80% of time budget; reduce grid/states/levels')
    return result
