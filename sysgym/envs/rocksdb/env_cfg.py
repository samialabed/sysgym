from dataclasses import dataclass

from dataclasses_json import dataclass_json

from sysgym import EnvConfig
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench import DBBenchPlan


@dataclass_json
@dataclass(frozen=True)
class RocksDBEnvConfig(EnvConfig):
    bench_cfg: DBBenchPlan

    @property
    def name(self) -> str:
        return "rocksdb"
