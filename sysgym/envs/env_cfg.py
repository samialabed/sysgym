from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from sysgym.envs.bench_cfg import BenchmarkConfig


@dataclass_json
@dataclass(frozen=True)
class EnvConfig(object):
    bench_cfg: BenchmarkConfig
    name: str = field(init=False)
