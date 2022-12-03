from dataclasses import dataclass
from typing import Dict, List, Optional

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.compaction_dao import CompactionStatistics
from sysgym.envs.rocksdb.stats.db_bench_dao import DBBenchStatistics
from sysgym.envs.rocksdb.stats.file_read_dao import FileReadStats
from sysgym.envs.rocksdb.stats.rocksdb_stats import RocksDBStatistics


@dataclass_json
@dataclass
class BenchmarkStats:
    db_bench: Optional[Dict[str, DBBenchStatistics]] = None
    compaction_statistics: Optional[CompactionStatistics] = None
    file_read: Optional[List[FileReadStats]] = None
    statistics: Optional[RocksDBStatistics] = None
