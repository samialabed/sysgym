from tenacity import retry, stop_after_attempt, wait_exponential

from sysgym.envs.env_abc import Environment
from sysgym.envs.env_measure import EnvMeasurements
from sysgym.envs.gem5.benchmarks.benchmark_docker import Gem5BenchmarkDocker
from sysgym.envs.gem5.env_cfg import Gem5EnvConfig
from sysgym.envs.gem5.env_measure import Gem5Measures
from sysgym.envs.gem5.params_dict import Gem5ParamsDict
from sysgym.envs.gem5.parsers import parse_statistics, parse_summary_file
from sysgym.envs.gem5.schema import Gem5ParamSchema


class Gem5(Environment):
    def __init__(self, env_cfg: Gem5EnvConfig):
        super().__init__(env_cfg)
        # TODO: allow selecting between docker client or non docker one
        self.benchmark_container = Gem5BenchmarkDocker(
            bench_cfg=env_cfg.bench_cfg, container_settings=env_cfg.container_settings
        )

    # TODO: move retry to environment creation and take the retry attempt from cfg
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(min=10, max=360))
    def run(self, params: Gem5ParamsDict) -> EnvMeasurements:
        with self.benchmark_container:
            self.benchmark_container.execute(params)
            # TODO: parse all statistics, and only need path to the output directory
            benchmark_results = parse_summary_file(
                self.ctx.env_output_dir / f"{self.env_cfg.bench_cfg.task}_summary"
            )
            detailed_stats = parse_statistics(self.ctx.env_output_dir / "stats.txt")
            return Gem5Measures(
                bench_stats=benchmark_results, detailed_stats=detailed_stats
            )

    def params_holder(self, params_schema: Gem5ParamSchema) -> Gem5ParamsDict:
        return Gem5ParamsDict(params_schema)
