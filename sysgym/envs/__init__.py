from sysgym.env_abc import EnvConfig, Environment
from sysgym.envs.gem5 import Gem5, Gem5EnvConfig

__all__ = ["Gem5"]


def env_from_cfg(env_cfg: EnvConfig) -> Environment:
    if isinstance(env_cfg, Gem5EnvConfig):

        env_cls = Gem5
    else:
        raise ValueError(f"Unrecognised environment type {type(env_cfg)}")

    return env_cls(env_cfg=env_cfg)
