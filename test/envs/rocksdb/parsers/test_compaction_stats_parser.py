import unittest
from pathlib import Path
from typing import Optional

from parameterized import parameterized

from sysgym.envs.rocksdb.parsers.compaction_stats_parser import CompactionStatsParser
from sysgym.envs.rocksdb.stats.compaction_dao import (
    CompactionGeneralStats,
    CompactionIOStats,
    CompactionStallsStats,
    CompactionStatistics,
    CompactionStatWithKey,
    OverallCompactionStats,
    PerLevelCompactionStats,
)


class TestCompactionStatsParserHelpers(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CompactionStatsParser()

    @parameterized.expand(
        [
            ("Expect None for empty string", "", None),
            ("Expect None for invalid line", "String: Empty", None),
            (
                # test
                "Expect to skip valid lines but aren't level",
                # input
                " Sum     18/10  622.87 MB   0.0      1.7     0.7      1.0       2.3      1.3       0.3   2.9    100.1    137.0     16.89             15.97        20    0.844     26M  2349K",
                # expected
                None,
            ),
        ]
    )
    def test_parse_compaction_level_return_empty_for_invalid_strings(
        self, name: str, input: str, expected: Optional[PerLevelCompactionStats]
    ):
        actual = self.parser._parse_compaction_level(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            (
                # test
                "Expect for valid line",
                # input
                "   L0      2/2   112.67 MB   0.0      0.0     0.0      0.0       0.8      0.8       0.0   1.0      0.0    145.1      5.44              5.12        14    0.388       0      0",
                # expected
                PerLevelCompactionStats(
                    level=0,
                    in_files=2,
                    out_files=2,
                    size_mb=112.67,
                    score=0.0,
                    read_gb=0.0,
                    rn_gb=0.0,
                    rnp1_gb=0.0,
                    write_gb=0.8,
                    wnew_gb=0.8,
                    moved_gb=0.0,
                    w_amp=1.0,
                    rd_mb_per_s=0.0,
                    wr_mb_per_s=145.1,
                    comp_sec=5.44,
                    comp_merge_cpu_sec=5.12,
                    comp_cnt=14.0,
                    avg_sec=0.388,
                    key_in=0.0,
                    key_drop=0.0,
                ),
            ),
        ]
    )
    def test_parse_compaction_level_return_PerLevelCompactionStats(
        self, name: str, input: str, expected: Optional[PerLevelCompactionStats]
    ):
        actual = self.parser._parse_compaction_level(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            ("Expect None for empty string", "", None),
            ("Expect None for invalid line", "String: Empty", None),
        ]
    )
    def test_parse_overall_compaction_line_return_empty_for_invalid_strings(
        self, name: str, input: str, expected: Optional[CompactionStatWithKey]
    ):
        actual = self.parser._parse_overall_compaction_line(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )

    @parameterized.expand(
        [
            (
                "Expect to parse uptime to CompactionGeneralStats",
                "Uptime(secs): 17.0 total, 14.0 interval",
                CompactionStatWithKey(
                    key="uptime_secs",
                    value=CompactionGeneralStats(total=17, interval=14),
                ),
            ),
            (
                "Expect to parse flush to CompactionGeneralStats",
                "Flush(GB): cumulative 0.770, interval 0.660",
                CompactionStatWithKey(
                    key="flush_gb",
                    value=CompactionGeneralStats(total=0.77, interval=0.660),
                ),
            ),
            (
                "Expect to parse addfile_gb to CompactionGeneralStats",
                "AddFile(GB): cumulative 0.000, interval 0.000",
                CompactionStatWithKey(
                    key="addfile_gb", value=CompactionGeneralStats(total=0, interval=0)
                ),
            ),
            (
                "Expect to parse addfile_total_files to CompactionGeneralStats",
                "AddFile(Total Files): cumulative 0, interval 0",
                CompactionStatWithKey(
                    key="addfile_total_files",
                    value=CompactionGeneralStats(total=0, interval=0),
                ),
            ),
            (
                "Expect to parse addfile_l0_files to CompactionGeneralStats",
                "AddFile(L0 Files): cumulative 0, interval 0",
                CompactionStatWithKey(
                    key="addfile_l0_files",
                    value=CompactionGeneralStats(total=0, interval=0),
                ),
            ),
            (
                "Expect to parse addfile_keys to CompactionGeneralStats",
                "AddFile(Keys): cumulative 0, interval 0",
                CompactionStatWithKey(
                    key="addfile_keys",
                    value=CompactionGeneralStats(total=0, interval=0),
                ),
            ),
            (
                "Expect to parse cumulative_compaction to CompactionIOStats",
                "Cumulative compaction: 2.26 GB write, 135.73 MB/s write, 1.65 GB read, 99.17 MB/s read, 16.9 seconds",
                CompactionStatWithKey(
                    key="cumulative_compaction",
                    value=CompactionIOStats(
                        write_size_mb=2260,
                        write_throughput=135.73,
                        read_size_mb=1650,
                        read_throughput=99.17,
                        time_sec=16.9,
                    ),
                ),
            ),
            (
                "Expect to parse interval_compaction to CompactionIOStats",
                "Interval compaction: 2.15 GB write, 156.91 MB/s write, 1.65 GB read, 120.52 MB/s read, 16.1 seconds",
                CompactionStatWithKey(
                    key="interval_compaction",
                    value=CompactionIOStats(
                        write_size_mb=2150,
                        write_throughput=156.91,
                        read_size_mb=1650,
                        read_throughput=120.52,
                        time_sec=16.1,
                    ),
                ),
            ),
            (
                "Expect to parse stalls_count into CompactionStallsStats",
                "Stalls(count): 0 level0_slowdown, 0 level0_slowdown_with_compaction, 0 level0_numfiles, 0 level0_numfiles_with_compaction, 0 stop for pending_compaction_bytes, 0 slowdown for pending_compaction_bytes, 0 memtable_compaction, 0 memtable_slowdown, interval 0 total count",
                CompactionStatWithKey(
                    key="stalls_count",
                    value=CompactionStallsStats(
                        level0_slowdown=0,
                        level0_slowdown_with_compaction=0,
                        level0_numfiles=0,
                        level0_numfiles_with_compaction=0,
                        stop=0,
                        slowdown=0,
                        memtable_compaction=0,
                        memtable_slowdown=0,
                        total=0,
                    ),
                ),
            ),
        ]
    )
    def test_parse_overall_compaction_line_return_valid_CompactionStatWithKey(
        self, name: str, input: str, expected: Optional[CompactionStatWithKey]
    ):
        actual = self.parser._parse_overall_compaction_line(line=input)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )


class TestCompactionStatsParserWholeLines(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CompactionStatsParser()

    @parameterized.expand(
        [
            (
                "Expect to return CompactionStatistics that exists in logs",
                "compaction_stats_parser_valid_test_cases.txt",
                CompactionStatistics(
                    name="CompactionStatistics",
                    overall_compaction_stats=OverallCompactionStats(
                        uptime_secs=CompactionGeneralStats(total=17.0, interval=14.0),
                        flush_gb=CompactionGeneralStats(total=0.77, interval=0.66),
                        addfile_gb=CompactionGeneralStats(total=0.0, interval=0.0),
                        addfile_total_files=CompactionGeneralStats(total=0, interval=0),
                        addfile_l0_files=CompactionGeneralStats(total=0, interval=0),
                        addfile_keys=CompactionGeneralStats(total=0, interval=0),
                        cumulative_compaction=CompactionIOStats(
                            write_size_mb=2260.0,
                            write_throughput=135.73,
                            read_size_mb=1650.0,
                            read_throughput=99.17,
                            time_sec=16.9,
                        ),
                        interval_compaction=CompactionIOStats(
                            write_size_mb=2150.0,
                            write_throughput=156.91,
                            read_size_mb=1650.0,
                            read_throughput=120.52,
                            time_sec=16.1,
                        ),
                        stalls_count=CompactionStallsStats(
                            level0_slowdown=0,
                            level0_slowdown_with_compaction=0,
                            level0_numfiles=0,
                            level0_numfiles_with_compaction=0,
                            stop=0,
                            slowdown=0,
                            memtable_compaction=0,
                            memtable_slowdown=0,
                            total=0,
                        ),
                    ),
                    per_level_compaction_stats=[
                        PerLevelCompactionStats(
                            level=0,
                            in_files=2,
                            out_files=2,
                            size_mb=112.67,
                            score=0.0,
                            read_gb=0.0,
                            rn_gb=0.0,
                            rnp1_gb=0.0,
                            write_gb=0.8,
                            wnew_gb=0.8,
                            moved_gb=0.0,
                            w_amp=1.0,
                            rd_mb_per_s=0.0,
                            wr_mb_per_s=145.1,
                            comp_sec=5.44,
                            comp_merge_cpu_sec=5.12,
                            comp_cnt=14.0,
                            avg_sec=0.388,
                            key_in=0.0,
                            key_drop=0.0,
                        ),
                        PerLevelCompactionStats(
                            level=1,
                            in_files=8,
                            out_files=8,
                            size_mb=252.7,
                            score=0.0,
                            read_gb=1.7,
                            rn_gb=0.7,
                            rnp1_gb=1.0,
                            write_gb=1.5,
                            wnew_gb=0.5,
                            moved_gb=0.0,
                            w_amp=2.3,
                            rd_mb_per_s=147.6,
                            wr_mb_per_s=133.1,
                            comp_sec=11.45,
                            comp_merge_cpu_sec=10.85,
                            comp_cnt=6.0,
                            avg_sec=1.908,
                            key_in=26.0,
                            key_drop=2.349,
                        ),
                        PerLevelCompactionStats(
                            level=2,
                            in_files=0,
                            out_files=8,
                            size_mb=257.5,
                            score=0.1,
                            read_gb=0.0,
                            rn_gb=0.0,
                            rnp1_gb=0.0,
                            write_gb=0.0,
                            wnew_gb=0.0,
                            moved_gb=0.3,
                            w_amp=0.0,
                            rd_mb_per_s=0.0,
                            wr_mb_per_s=0.0,
                            comp_sec=0.0,
                            comp_merge_cpu_sec=0.0,
                            comp_cnt=0.0,
                            avg_sec=0.0,
                            key_in=0.0,
                            key_drop=0.0,
                        ),
                        PerLevelCompactionStats(
                            level=12,
                            in_files=0,
                            out_files=8,
                            size_mb=257.5,
                            score=0.1,
                            read_gb=60.0,
                            rn_gb=0.0,
                            rnp1_gb=0.0,
                            write_gb=0.0,
                            wnew_gb=0.0,
                            moved_gb=0.3,
                            w_amp=0.0,
                            rd_mb_per_s=0.0,
                            wr_mb_per_s=0.0,
                            comp_sec=0.0,
                            comp_merge_cpu_sec=0.0,
                            comp_cnt=0.0,
                            avg_sec=0.0,
                            key_in=5000.0,
                            key_drop=0.0,
                        ),
                    ],
                ),
            )
        ]
    )
    def test_parse_lines(self, name: str, input: str, expected: CompactionStatistics):
        with open(Path(__file__).parent / "resources" / input) as f:
            contents = f.readlines()

        actual = self.parser.parse_lines(contents)
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )
