from dataclasses import dataclass

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.stats_dao import Statistics


@dataclass_json
@dataclass
class DBBenchStatistics(Statistics):
    __slots__ = ["name", "latency", "iops", "io_size"]

    latency: float
    iops: float
    io_size: float
