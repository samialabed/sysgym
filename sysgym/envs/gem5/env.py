import logging

from tenacity import retry, stop_after_attempt, wait_exponential

from sysgym.env_abc import Environment, EnvMetrics
from sysgym.envs.gem5.benchmarks.benchmark_docker import Gem5BenchmarkDocker
from sysgym.envs.gem5.env_cfg import Gem5EnvConfig
from sysgym.param_dict import EnvParamsDict

LOG = logging.getLogger("sysgym")


class Gem5(Environment):
    def __init__(self, env_cfg: Gem5EnvConfig):
        super().__init__(env_cfg)
        self.benchmark_container = Gem5BenchmarkDocker(
            bench_cfg=env_cfg.bench_cfg,
            container_settings=env_cfg.container_settings,
            output_dir=env_cfg.artifacts_output_dir,
        )
        self.run = retry(
            stop=stop_after_attempt(env_cfg.retry_attempt),
            wait=wait_exponential(min=10, max=360),
        )(self.run)

    def run(self, params: EnvParamsDict) -> EnvMetrics:
        LOG.debug("Evaluating params: %s", params)
        with self.benchmark_container:
            benchmark_results = self.benchmark_container.execute(params)
            return benchmark_results
