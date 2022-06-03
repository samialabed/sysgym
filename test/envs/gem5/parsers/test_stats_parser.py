import unittest
from pathlib import Path
from typing import Dict

import numpy as np
from core import TestInput
from parameterized import parameterized

from sysgym.envs.gem5.parsers import parse_statistics
from sysgym.envs.gem5.stats import Gem5SystemStats

RESOURCE_DIR = Path(__file__).parent / "resources"


class TestSummaryParser(unittest.TestCase):
    @parameterized.expand(
        [
            TestInput(
                name="Expect to sum over all results ",
                test_input="fft_transpose/stats.txt",
                expected={
                    "system": Gem5SystemStats(
                        final_tick=149710365441,  # this is max value and not cumulative
                        host_inst_rate=257796,
                        host_mem_usage=9147144,
                        host_op_rate=542959,
                        host_seconds=46.75,
                        host_tick_rate=6177232821,
                        sim_insts=6579872,
                        sim_ops=13579928,
                        sim_seconds=0.14971,
                        sim_ticks=149710365441,
                    ),
                    "performance": {
                        "system.cpu.commit.branches": 1388891.0,
                        "system.cpu.int_regfile_writes": 9269864.0,
                    },
                },
            ),
        ]
    )
    def test_parse_compaction_level_return_empty_for_invalid_strings(
        self, name: str, stats_path: str, expected: Dict
    ):
        actual = parse_statistics(RESOURCE_DIR / stats_path)
        self.assertEqual(
            expected["system"],
            actual.system,
            f"failed test {name} expected {expected}, actual {actual}",
        )
        for (expected_col_name, expected_col_value) in expected["performance"].items():
            self.assertEqual(
                expected_col_value,
                np.asscalar(actual.performance[expected_col_name].values),
                f"failed test {name} expected {expected_col_value}, "
                f"actual {actual.performance[expected_col_name]}",
            )
