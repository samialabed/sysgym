from dataclasses import dataclass, fields
from typing import List, Union

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.benchmarks.benchmark_settings import BenchmarkSettings
from sysgym.envs.rocksdb.benchmarks.dbbench.benchmarks_opts import (
    DBBenchBenchmarksOptions,
)


@dataclass_json
@dataclass(frozen=True)
class DBBenchSettings(BenchmarkSettings):
    # Reference: https://github.com/facebook/rocksdb/blob/master/tools/db_bench_tool.cc
    benchmarks: Union[str, DBBenchBenchmarksOptions]
    num: int  # Number of k/values to place in database
    duration: int = 0  # Time(sec) for the run. When 0 then num determine the duration
    statistics: bool = True  # collect statistics about the run
    value_size: int = 100  # size of each value
    cache_size: int = 8388608  # Number of bytes to use as a cache of uncompressed data
    threads: int = 1  # numbe of concurrent threads to run
    batch_size: int = 1  # (Batch size)
    benchmark_read_rate_limit: int = 0  # If !=0 rate-limit the reads in ops/sec
    benchmark_write_rate_limit: int = 0  # If !=0 rate-limit the writes in ops/sec
    use_existing_db: bool = False  # If true don't destroy the existing db
    db: str = "/tmp/rocksdb"
    wal_dir: str = "/tmp/rocksdb/WAL_LOG"
    prefix_size: int = 0  # control the prefix size for HashSkipList and plain table
    key_size: int = 16  # size of each k
    keys_per_prefix: int = 0  # control average number of keys generated per prefix
    perf_level: int = 1  # 1 disable, 2 counts, 3 time, 4 cpu&time!mutex, 5 count&time
    reads: int = -1  # Number of reads to do, if -1 do NUM
    use_direct_io_for_flush_and_compaction: bool = False  # Use O_DIRECT for flush&copct
    use_direct_reads: bool = False  # use O_DIRECT for reading data

    def as_cmd(self) -> List[str]:
        out = []
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, DBBenchBenchmarksOptions):
                value = value.as_settings()
            out.append(f"--{field.name}={value}")

        return out
