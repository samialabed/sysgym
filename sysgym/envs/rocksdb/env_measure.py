from dataclasses import asdict, dataclass
from typing import Dict

from dataclasses_json import dataclass_json

from sysgym import EnvMetrics
from sysgym.envs.rocksdb.stats.parser_factory_dao import BenchmarkStats
from sysgym.envs.rocksdb.stats.sysio_dao import SystemIO


@dataclass_json
@dataclass(frozen=True)
class RocksDBMeasurements(EnvMetrics):
    def as_flat_dict(self) -> Dict[str, any]:
        bench_stats_dict = asdict(self.bench_stats)
        sysio_dict = asdict(self.sysio)
        return {**bench_stats_dict, **sysio_dict}

    bench_stats: BenchmarkStats
    sysio: SystemIO
