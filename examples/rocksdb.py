import logging
from pathlib import Path

from sysgym.envs import RocksDBEnv, RocksDBEnvConfig
from sysgym.envs.rocksdb.benchmarks.dbbench import established_benchmarks
from sysgym.envs.rocksdb.schema import RocksDB10Params
from sysgym.param_dict import EnvParamsDict

logging.basicConfig(level=logging.DEBUG)

# you can define your own parameter space, or use one of the pre-defined one
param_space = RocksDB10Params()
# You can customize your benchmark with DBBenchPlan or use predefined one
benchmark_cfg = established_benchmarks.DBBenchTasks.READ_RANDOM_WRITE_RANDOM.get_plan()
# Define execution plan: how many times to retry at failures, the benchmark to use, etc.
cfg = RocksDBEnvConfig(
    bench_cfg=benchmark_cfg,
)
# Create the env
env = RocksDBEnv(env_cfg=cfg, artifacts_output_dir=Path("/tmp/rocksdb_exp/"))
params_dict = EnvParamsDict(param_space=param_space)
# run the system with default param space values
env_measures = env.run(params=params_dict)
# obser the env_measures
# this would be what your optimizer want to observe
print(f"Env measurements before: {env_measures}")
# update the parameters of the env and run it
# this would be the values proposed by your optimizer
params_dict["max_background_compactions"] = 4
env_measures = env.run(params_dict)
print(f"Env measurements after: {env_measures}")
