from pathlib import Path
from typing import Dict, List, Optional
from unittest import TestCase

from parameterized import parameterized

from sysgym.envs.rocksdb.parsers.constant_types import NUM_VALUE
from sysgym.envs.rocksdb.parsers.level_file_read_parser import FileReadByLevelParser
from sysgym.envs.rocksdb.stats.file_read_dao import FileReadStats


class TestFileReadByLevelLineParser(TestCase):
    def setUp(self) -> None:
        self.parser = FileReadByLevelParser()

    @parameterized.expand(
        [
            ("Expect None for empty string", "", None),
            ("Expect None for invalid line", "String: Empty", None),
        ]
    )
    def test_parse_invalid_line(
        self, name: str, input: str, expected: Optional[Dict[str, NUM_VALUE]]
    ):
        actual = self.parser.parse(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            (
                "Expect to parse various values separated by random number of spaces",
                "Count: 321868 Average: 0.8364  StdDev: 0.59",
                dict(count=321868, average=0.8364, stddev=0.59),
            ),
            (
                "Expect to parse median max and min",
                "Min: 0  Median: 0.5059  Max: 45",
                dict(min=0, median=0.5059, max=45),
            ),
            (
                "Expect to parse percentiles",
                "Percentiles: P50: 0.51 P75: 0.76 P99: 1.15 P99.9: 1.99 P99.99: 20.52",
                dict(p50=0.51, p75=0.76, p99=1.15, p99_9=1.99, p99_99=20.52),
            ),
        ]
    )
    def test_parse_valid_line_return_expected(
        self, name: str, input: str, expected: Optional[Dict[str, NUM_VALUE]]
    ):
        actual = self.parser.parse(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )


class TestFileReadByLevelLinesParser(TestCase):
    def setUp(self) -> None:
        self.parser = FileReadByLevelParser()

    @parameterized.expand(
        [
            (
                "Expect to return list of multiple FileReadStats levels that exists in logs",
                "level_file_parser_valid_testcases.txt",
                [
                    FileReadStats(
                        name="FileReadStatsLevel0",
                        level=0,
                        count=321868,
                        average=0.8364,
                        stddev=0.59,
                        min=0,
                        median=0.5059,
                        max=45,
                        p50=0.51,
                        p75=0.76,
                        p99=1.15,
                        p99_9=1.99,
                        p99_99=20.52,
                    ),
                    FileReadStats(
                        name="FileReadStatsLevel1",
                        level=1,
                        count=513322,
                        average=0.8247,
                        stddev=0.62,
                        min=0,
                        median=0.5053,
                        max=207,
                        p50=0.51,
                        p75=0.76,
                        p99=1.06,
                        p99_9=1.98,
                        p99_99=20.27,
                    ),
                ],
            )
        ]
    )
    def test_parse_lines(self, name: str, input: str, expected: List[FileReadStats]):
        with open(Path(__file__).parent / "resources" / input) as f:
            contents = f.readlines()

        actual = self.parser.parse_lines(contents)
        self.assertListEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            (
                "Expect to return only valid line input and ignore the invalid one",
                "level_file_parser_invalid_testcases.txt",
                [
                    FileReadStats(
                        name="FileReadStatsLevel0",
                        level=0,
                        count=321868,
                        average=0.8364,
                        stddev=0.59,
                        min=0,
                        median=0.5059,
                        max=45,
                        p50=0.51,
                        p75=0.76,
                        p99=1.15,
                        p99_9=1.99,
                        p99_99=20.52,
                    ),
                ],
            )
        ]
    )
    def test_parse_lines(self, name: str, input: str, expected: List[FileReadStats]):
        with open(Path(__file__).parent / "resources" / input) as f:
            contents = f.readlines()

        actual = self.parser.parse_lines(contents)
        self.assertListEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )
