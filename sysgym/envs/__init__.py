from typing import Type

from sysgym.env_abc import EnvConfig, Environment
from sysgym.envs.gem5 import Gem5, Gem5EnvConfig, RocksDBEnv, RocksDBEnvConfig


def env_from_cfg(env_cfg: EnvConfig) -> Type[Environment]:
    if isinstance(env_cfg, Gem5EnvConfig):
        env_cls = Gem5
    elif isinstance(env_cfg, RocksDBEnvConfig):
        env_cls = RocksDBEnv
    else:
        raise ValueError(f"Unrecognised environment type {type(env_cfg)}")

    return env_cls
