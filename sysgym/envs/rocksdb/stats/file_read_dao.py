from dataclasses import dataclass

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.stats_dao import Statistics


@dataclass_json
@dataclass
class FileReadStats(Statistics):
    __slots__ = [
        "name",
        "level",
        "count",
        "average",
        "stddev",
        "min",
        "median",
        "max",
        "p50",
        "p75",
        "p99",
        "p99_9",
        "p99_99",
    ]
    level: int
    count: float
    average: float
    stddev: float
    min: float
    median: float
    max: float
    p50: float
    p75: float
    p99: float
    p99_9: float
    p99_99: float
