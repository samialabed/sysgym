import unittest
from pathlib import Path
from typing import Dict
from unittest.mock import MagicMock

from sysgym.envs.rocksdb.parsers.parser_factory import ParserFactory
from sysgym.envs.rocksdb.parsers.parser_factory import ParsersTrigger as Triggers
from sysgym.envs.rocksdb.stats.parser_factory_dao import BenchmarkStats


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        parser = ParserFactory()

        mocked_dbbench_parser = MagicMock()
        mocked_dbbench_parser.parse_lines = MagicMock(return_value=["db"])
        mocked_dbbench_parser.name = "db_bench"

        mocked_compact = MagicMock()
        mocked_compact.parse_lines = MagicMock(return_value=["compact"])
        mocked_compact.name = "compaction_statistics"

        mocked_files = MagicMock()
        mocked_files.parse_lines = MagicMock(return_value=["files"])
        mocked_files.name = "file_read"

        mocked_statistics = MagicMock()
        mocked_statistics.parse_lines = MagicMock(return_value=["stats"])
        mocked_statistics.name = "statistics"

        mocked_parser_switcher: Dict[Triggers, MagicMock] = {
            Triggers.DBBench: mocked_dbbench_parser,
            Triggers.Compactions: mocked_compact,
            Triggers.Files: mocked_files,
            Triggers.Statistics: mocked_statistics,
        }

        parser._parser_switcher = mocked_parser_switcher

        self._mocked_parser_switcher = mocked_parser_switcher
        self._parser = parser

    def test_only_dbbench_is_called_when_lines_has_no_other_triggers(self):
        with open(
            Path(__file__).parent / "resources" / "dbbench_valid_testcase.txt"
        ) as f:
            contents = f.readlines()

        actual = self._parser.parse_lines(contents)

        parsers = self._mocked_parser_switcher

        parsers[Triggers.DBBench].parse_lines.assert_called_once()
        parsers[Triggers.Compactions].parse_lines.assert_not_called()
        parsers[Triggers.Files].parse_lines.assert_not_called()
        parsers[Triggers.Statistics].parse_lines.assert_not_called()

        expected = BenchmarkStats(db_bench=["db"])
        self.assertEqual(
            expected, actual, f"failed dbbench expected {expected}, actual {actual}"
        )

    def test_only_compactions_is_called_when_lines_has_no_other_triggers(self):
        with open(
            Path(__file__).parent
            / "resources"
            / "compaction_stats_parser_valid_test_cases.txt"
        ) as f:
            contents = f.readlines()

        actual = self._parser.parse_lines(contents)

        parsers = self._mocked_parser_switcher

        parsers[Triggers.DBBench].parse_lines.assert_not_called()
        parsers[Triggers.Compactions].parse_lines.assert_called_once()
        parsers[Triggers.Files].parse_lines.assert_not_called()
        parsers[Triggers.Statistics].parse_lines.assert_not_called()

        expected = BenchmarkStats(compaction_statistics=["compact"])
        self.assertEqual(
            expected, actual, f"failed dbbench expected {expected}, actual {actual}"
        )

    def test_only_files_is_called_when_lines_has_no_other_triggers(self):
        with open(
            Path(__file__).parent
            / "resources"
            / "level_file_parser_valid_testcases.txt"
        ) as f:
            contents = f.readlines()

        actual = self._parser.parse_lines(contents)

        parsers = self._mocked_parser_switcher

        parsers[Triggers.DBBench].parse_lines.assert_not_called()
        parsers[Triggers.Compactions].parse_lines.assert_not_called()
        parsers[Triggers.Files].parse_lines.assert_called_once()
        parsers[Triggers.Statistics].parse_lines.assert_not_called()

        expected = BenchmarkStats(file_read=["files"])
        self.assertEqual(
            expected, actual, f"failed dbbench expected {expected}, actual {actual}"
        )

    def test_only_statistics_is_called_when_lines_has_no_other_triggers(self):
        with open(
            Path(__file__).parent / "resources" / "statistics_valid_testcase.txt"
        ) as f:
            contents = f.readlines()

        actual = self._parser.parse_lines(contents)

        parsers = self._mocked_parser_switcher

        parsers[Triggers.DBBench].parse_lines.assert_not_called()
        parsers[Triggers.Compactions].parse_lines.assert_not_called()
        parsers[Triggers.Files].parse_lines.assert_not_called()
        parsers[Triggers.Statistics].parse_lines.assert_called_once()

        expected = BenchmarkStats(statistics=["stats"])
        self.assertEqual(
            expected, actual, f"failed dbbench expected {expected}, actual {actual}"
        )
