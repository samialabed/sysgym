import logging
from pathlib import Path

from sysgym.envs import Gem5, Gem5EnvConfig
from sysgym.envs.gem5.benchmarks.benchmark_settings import (
    BenchmarkSuite,
    Gem5BenchmarkConfig,
    MemoryType,
    Simulators,
)
from sysgym.envs.gem5.benchmarks.benchmark_tasks import MachSuiteTask
from sysgym.envs.gem5.benchmarks.pre_defained_docker_settings import (
    aladdin_docker_settings,
)
from sysgym.envs.gem5.schemas import AladdinSweeper20Params
from sysgym.param_dict import EnvParamsDict

logging.basicConfig(level=logging.DEBUG)

# you can define your own parameter space, or use one of the pre-defined one
param_space = AladdinSweeper20Params()
# Customizable execution: you can customize the benchmark to your need
docker_container_cfg = aladdin_docker_settings()
benchmark_cfg = Gem5BenchmarkConfig(
    source_dir=docker_container_cfg.gem_workspace_dir,
    bench_suite=BenchmarkSuite.MACHSUITE,
    task=MachSuiteTask.AES,
    simulator=Simulators.CPU,
    memory_type=MemoryType.CACHE,
)
# Define execution plan: how many times to retry at failures, the benchmark to use, etc.
cfg = Gem5EnvConfig(
    container_settings=docker_container_cfg,
    bench_cfg=benchmark_cfg,
    retry_attempt=1,
)
# Create the env
env = Gem5(env_cfg=cfg, artifacts_output_dir=Path("/tmp/gem5/"))
params_dict = EnvParamsDict(param_space=param_space)
# run the system with default param space values
env_measures = env.run(params=params_dict)
# obser the env_measures
print(env_measures)  # this would be what your optimizer want to observe
# update the parameters of the env and run it
params_dict["cache_assoc"] = 4  # this would be the values proposed by your optimizer
env_measures = env.run(params_dict)
print(env_measures)
