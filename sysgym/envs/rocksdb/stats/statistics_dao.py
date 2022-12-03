from dataclasses import dataclass

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.stats_dao import Statistics


@dataclass_json
@dataclass
class MacroStats(Statistics):
    __slots__ = ["name", "count"]
    count: int


@dataclass_json
@dataclass
class MicroStats(Statistics):
    __slots__ = ["name", "p50", "p95", "p99", "p100", "count", "sum"]
    p50: float
    p95: float
    p99: float
    p100: float
    count: int
    sum: float
