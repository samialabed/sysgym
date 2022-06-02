from sysgym.envs.env_abc import Environment
from sysgym.envs.env_cfg import EnvConfig
from sysgym.envs.gem5.env_cfg import Gem5EnvConfig
from sysgym.envs.postgres.env_cfg import PostgresEnvConfig
from sysgym.envs.rocksdb.env_cfg import RocksDBEnvConfig
from sysgym.envs.synthetic.env_cfg import TestFunctionCfg


def env_from_cfg(env_cfg: EnvConfig) -> Environment:
    if isinstance(env_cfg, RocksDBEnvConfig):
        from sysgym.envs.rocksdb.env import RocksDBEnv

        env_cls = RocksDBEnv
    elif isinstance(env_cfg, TestFunctionCfg):
        from sysgym.envs.synthetic.funcs.syncth_factory import env_from_cfg

        env_cls = env_from_cfg(env_cfg)
    elif isinstance(env_cfg, Gem5EnvConfig):
        from sysgym.envs.gem5.env import Gem5

        env_cls = Gem5

    elif isinstance(env_cfg, PostgresEnvConfig):
        from sysgym.envs.postgres.env import Postgres

        env_cls = Postgres
    else:
        raise ValueError(f"Unrecognised environment type {type(env_cfg)}")

    return env_cls(env_cfg=env_cfg)
