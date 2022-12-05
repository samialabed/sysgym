from pathlib import Path
from test.envs.rocksdb.parsers.resources.valid_statics import statistics_valid_testcase
from typing import List, Optional, Union
from unittest import TestCase

from parameterized import parameterized

from sysgym.envs.rocksdb.parsers.statistics_parser import Parser, StatisticsParser
from sysgym.envs.rocksdb.stats.rocksdb_stats import StatisticsType
from sysgym.envs.rocksdb.stats.statistics_dao import MacroStats, MicroStats


class TestStatisticsParser(TestCase):
    def setUp(self) -> None:
        self.parser = StatisticsParser()

    @parameterized.expand(
        [
            ("Expect None for empty string", "", None),
            ("Expect None for invalid line", "String: Empty", None),
        ]
    )
    def test_parse_invalid_line(
        self, name: str, input: str, expected: Optional[Union[MicroStats, MacroStats]]
    ):
        actual = self.parser.parse(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            (
                "Expect MacroStats for a line containing only count",
                "rocksdb.files.deleted.immediately COUNT : 4",
                MacroStats("rocksdb_files_deleted_immediately", count=4),
            ),
            (
                "Expect MicroStats for a line containing all the micros",
                "rocksdb.db.get.micros P50 : 0.000000 P95 : 95.000000 P99 : 99.000000 P100 : 1.00000 COUNT : 2 SUM : 5",
                MicroStats(
                    "rocksdb_db_get_micros",
                    p50=0,
                    p95=95,
                    p99=99,
                    p100=1,
                    count=2,
                    sum=5,
                ),
            ),
        ]
    )
    def test_parse_valid_line_return_expected(
        self, name: str, input: str, expected: Optional[StatisticsType]
    ):
        actual = self.parser.parse(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )


class TestStatisticsLinesParser(TestCase):
    def setUp(self) -> None:
        self.parser = StatisticsParser()

    @parameterized.expand(
        [
            (
                "Expect to return list of multiple StatisticsType that exists in logs",
                "statistics_valid_testcase.txt",
                statistics_valid_testcase,
            )
        ]
    )
    def test_parse_lines(self, name: str, input: str, expected: List[StatisticsType]):
        with open(Path(__file__).parent / "resources" / input) as f:
            contents = f.readlines()

        actual = self.parser.parse_lines(contents)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )
