import unittest
from pathlib import Path
from typing import Optional

from parameterized import parameterized

from sysgym.envs.gem5.parsers import parse_summary_file
from sysgym.envs.gem5.stats import SummaryStats

RESOURCE_DIR = Path(__file__).parent / "resources"


class TestSummaryParser(unittest.TestCase):
    @parameterized.expand(
        [
            (
                # test
                "Expect to skip valid lines but aren't level",
                # input
                "fft_transpose/fft_transpose_summary",
                # expected
                SummaryStats(
                    cycle=24156,
                    total_area=962188,
                    avg_power=22.0119,
                    idle_fu_cycles=4877,
                    avg_fu_power=20.9856,
                    avg_fu_dynamic_power=12.6527,
                    avg_fu_leakage_power=8.33294,
                    avg_mem_power=1.02628,
                    avg_mem_dynamic_power=0.0888076,
                    avg_mem_leakage_power=0.937476,
                    fu_area=907193,
                    mem_area=54995.5,
                    num_double_precision_fp_multipliers=33.0,
                    num_double_precision_fp_adders=27.0,
                    num_trigonometric_units=14.0,
                    num_bitwise_operators=9.0,
                    num_shifters=6.0,
                    num_registers=544,
                ),
            ),
        ]
    )
    def test_parse_compaction_level_return_empty_for_invalid_strings(
        self, name: str, input: str, expected: Optional[SummaryStats]
    ):
        actual = parse_summary_file(RESOURCE_DIR / input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )
