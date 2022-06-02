from dataclasses import dataclass

from dataclasses_json import dataclass_json

from sysgym.envs import EnvConfig
from sysgym.envs.gem5.benchmarks.benchmark_docker import Gem5ContainerSettings
from sysgym.envs.gem5.benchmarks.benchmark_settings import Gem5BenchmarkConfig


@dataclass_json
@dataclass(frozen=True)
class Gem5EnvConfig(EnvConfig):
    container_settings: Gem5ContainerSettings
    bench_cfg: Gem5BenchmarkConfig
    retry_attempt: int  # number of times to retry in case of env failure
    repeat_eval: int = 1  # gem5 is a deterministic simulator no need to repeat

    @property
    def name(self) -> str:
        return "gem5"
