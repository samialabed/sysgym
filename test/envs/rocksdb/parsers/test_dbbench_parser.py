from pathlib import Path
from typing import Dict, Optional
from unittest import TestCase

from parameterized import parameterized

from sysgym.envs.rocksdb.parsers.dbbench_parser import DBBenchParser
from sysgym.envs.rocksdb.stats.db_bench_dao import DBBenchStatistics


class TestDBBenchParser(TestCase):
    def setUp(self) -> None:
        self.parser = DBBenchParser()

    @parameterized.expand(
        [
            ("Expect None for empty string", "", None),
            ("Expect None for invalid line", "String: Empty", None),
        ]
    )
    def test_parse_invalid_line(
        self, name: str, line_input: str, expected: Optional[DBBenchStatistics]
    ):
        actual = self.parser.parse(line=line_input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            (
                "Expect DBBenchStatistics for a valid dbbench line",
                "fillrandom   :       1.299 micros/op 770049 ops/sec;   88.1 MB/s",
                DBBenchStatistics("fillrandom", 1.299, 770049, 88.1),
            )
        ]
    )
    def test_parse_valid_line_return_expected(
        self, name: str, line_input: str, expected: Optional[DBBenchStatistics]
    ):
        actual = self.parser.parse(line=line_input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )


class TestDBBenchLinesParser(TestCase):
    def setUp(self) -> None:
        self.parser = DBBenchParser()

    @parameterized.expand(
        [
            (
                "Expect return list of multiple DBBenchStatistics that exists in logs",
                "dbbench_valid_testcase.txt",
                {
                    "fillrandom": DBBenchStatistics("fillrandom", 2.782, 359507, 39.8),
                    "fillseq": DBBenchStatistics("fillseq", 1.8, 555409, 61.4),
                },
            )
        ]
    )
    def test_parse_lines(
        self, name: str, test_file_name: str, expected: Dict[str, DBBenchStatistics]
    ):
        with open(Path(__file__).parent / "resources" / test_file_name) as f:
            contents = f.readlines()

        actual = self.parser.parse_lines(contents)
        self.assertDictEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )
