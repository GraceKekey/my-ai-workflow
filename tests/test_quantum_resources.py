import math
import unittest
from dataclasses import replace

from quantum.resources import Config, estimate_memory_mb, plan


class TestQuantumResources(unittest.TestCase):
    def test_nested_grids_and_same_spacing_domain(self):
        config = Config().validate()
        self.assertEqual(config.grids(), [1023, 2047, 4095])
        self.assertEqual(config.domain_grid(), 5119)
        self.assertEqual(2 * config.half_width / (config.grid_points + 1),
                         2 * 1.25 * config.half_width / (config.domain_grid() + 1))

    def test_invalid_parameters(self):
        cases = dict(grid_points=[126, 200001, 4096, 4095.0], states=[0, 33],
                     levels=[2, 6], half_width=[2, 21, math.nan],
                     mass=[0, -1, math.inf], omega=[0, math.nan], hbar=[0, math.inf],
                     max_seconds=[59, 2401], memory_mb=[255, 4097])
        for name, values in cases.items():
            for value in values:
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    replace(Config(), **{name: value}).validate()

    def test_physical_scales(self):
        length, energy = Config(mass=2, omega=3, hbar=4).validate().scales()
        self.assertAlmostEqual(length, math.sqrt(2 / 3))
        self.assertEqual(energy, 12)

    def test_memory_and_time_rejection_before_increasing(self):
        with self.assertRaisesRegex(ValueError, 'memory'):
            plan(Config(memory_mb=256))
        with self.assertRaisesRegex(ValueError, 'memory'):
            plan(Config(), available_mb=400)
        with self.assertRaisesRegex(ValueError, 'runtime'):
            plan(Config(max_seconds=60), pilot_seconds=1)
        self.assertLess(estimate_memory_mb(4095, 6), 600)
        self.assertGreater(estimate_memory_mb(8191, 6), estimate_memory_mb(4095, 6))
        self.assertIsNone(plan(Config())['estimated_total_seconds'])


if __name__ == '__main__':
    unittest.main()
