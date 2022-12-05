import unittest
from typing import Dict

from parameterized import parameterized

from sysgym.envs.rocksdb.benchmarks.dbbench.benchmarks_opts import (
    DBBenchBenchmarksOptions,
)
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench_settings import DBBenchSettings


class TestDBBenchBenchmarksOptions(unittest.TestCase):
    @parameterized.expand(
        [
            (
                "Expect as_settings only has flags toggled on",
                DBBenchBenchmarksOptions(fillrandom=True, stats=False),
                "fillrandom",
            ),
            (
                "Expect when all flags off as_settings return empty string",
                DBBenchBenchmarksOptions(fillrandom=False, stats=False),
                "",
            ),
            (
                "Expect when all flags are True, as_settings return strings joint "
                "with comma no space.",
                DBBenchBenchmarksOptions(fillrandom=True, stats=True),
                "fillrandom,stats",
            ),
        ]
    )
    def test_as_settings_behaviour(
        self, name: str, db_input: DBBenchBenchmarksOptions, expected: str
    ):
        actual = db_input.as_settings()
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )


class TestDBBenchSettings(unittest.TestCase):
    @parameterized.expand(
        [
            (
                # test
                "Expect for_cmd able to handle str for benchmarks",
                # input
                DBBenchSettings(
                    benchmarks="hi",
                    threads=1,
                    statistics=False,
                    num=2,
                    db="/tmp/",
                ),
                # expected
                [
                    "--benchmarks=hi",
                    "--num=2",
                    "--duration=0",
                    "--statistics=False",
                    "--value_size=100",
                    "--cache_size=8388608",
                    "--threads=1",
                    "--batch_size=1",
                    "--benchmark_read_rate_limit=0",
                    "--benchmark_write_rate_limit=0",
                    "--use_existing_db=False",
                    "--db=/tmp/",
                    "--wal_dir=/tmp/rocksdb/WAL_LOG",
                    "--prefix_size=0",
                    "--key_size=16",
                    "--keys_per_prefix=0",
                    "--perf_level=1",
                    "--reads=-1",
                    "--use_direct_io_for_flush_and_compaction=False",
                    "--use_direct_reads=False",
                ],
            ),
            (
                # test
                "Expect for_cmd able to handle DBBenchBenchmarksOptions for benchmarks",
                # input
                DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(stats=True, fillrandom=True),
                    threads=1,
                    statistics=False,
                    num=2,
                    db="/tmp/",
                ),
                # expected
                [
                    "--benchmarks=fillrandom,stats",
                    "--num=2",
                    "--duration=0",
                    "--statistics=False",
                    "--value_size=100",
                    "--cache_size=8388608",
                    "--threads=1",
                    "--batch_size=1",
                    "--benchmark_read_rate_limit=0",
                    "--benchmark_write_rate_limit=0",
                    "--use_existing_db=False",
                    "--db=/tmp/",
                    "--wal_dir=/tmp/rocksdb/WAL_LOG",
                    "--prefix_size=0",
                    "--key_size=16",
                    "--keys_per_prefix=0",
                    "--perf_level=1",
                    "--reads=-1",
                    "--use_direct_io_for_flush_and_compaction=False",
                    "--use_direct_reads=False",
                ],
            ),
        ]
    )
    def test_as_cmd_behaviour(
        self, name: str, db_input: DBBenchSettings, expected: Dict[str, any]
    ):
        actual = db_input.as_cmd()
        self.assertEqual(
            expected, actual, f"failed test {name} expected {expected}, actual {actual}"
        )
