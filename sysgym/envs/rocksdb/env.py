import logging
from pathlib import Path

from sysgym import Environment, EnvParamsDict
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench import DBBench
from sysgym.envs.rocksdb.env_cfg import RocksDBEnvConfig
from sysgym.envs.rocksdb.env_measure import RocksDBMeasurements

LOG = logging.getLogger("sysgym")


class RocksDBEnv(Environment):
    def __init__(self, env_cfg: RocksDBEnvConfig, artifacts_output_dir: Path):
        super().__init__(env_cfg=env_cfg, artifacts_output_dir=artifacts_output_dir)
        self.benchmark = DBBench(artifacts_output_dir, env_cfg.bench_cfg)

    def run(self, params: EnvParamsDict) -> RocksDBMeasurements:
        LOG.debug("Evaluating params: %s", params)
        return self.benchmark.execute(params=params)
