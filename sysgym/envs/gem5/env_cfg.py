from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from sysgym.envs.env_cfg import EnvConfig
from sysgym.envs.gem5.benchmarks.benchmark_docker import Gem5ContainerSettings
from sysgym.envs.gem5.benchmarks.benchmark_settings import Gem5BenchmarkConfig


@dataclass_json
@dataclass(frozen=True)
class Gem5EnvConfig(EnvConfig):
    container_settings: Gem5ContainerSettings
    bench_cfg: Gem5BenchmarkConfig
    name: str = field(init=False, default="gem5")
