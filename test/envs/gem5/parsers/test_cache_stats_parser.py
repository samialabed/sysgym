import unittest
from pathlib import Path

from core import TestInput
from parameterized import parameterized

from sysgym.envs.gem5.parsers import parse_cache_stats_file
from sysgym.envs.gem5.stats import CacheStats

RESOURCE_DIR = Path(__file__).parent / "resources"


class TestSummaryParser(unittest.TestCase):
    @parameterized.expand(
        [
            TestInput(
                name="Expect to sum over all results ",
                test_input="fft_transpose/fft_transpose_cache_stats.txt",
                expected=CacheStats(
                    system_datapath_dcache_average_pwr=0.0,
                    system_datapath_dcache_dynamic_pwr=0.0,
                    system_datapath_dcache_leakage_pwr=0.0,
                    system_datapath_dcache_area=0.0,
                    system_datapath_tlb_average_pwr=3.81578e-35,
                    system_datapath_tlb_dynamic_pwr=0.0,
                    system_datapath_tlb_leakage_pwr=3.81578e-35,
                    system_datapath_tlb_area=4.58799e-41,
                ),
            ),
        ]
    )
    def test_parse_compaction_level_return_empty_for_invalid_strings(
        self, name: str, stats_path: str, expected: CacheStats
    ):
        actual = parse_cache_stats_file(RESOURCE_DIR / stats_path)
        self.assertEqual(
            expected,
            actual,
            f"failed test {name} expected {expected}, actual {actual}",
        )
