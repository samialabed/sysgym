from abc import ABC, abstractmethod

from sysgym.envs.env_cfg import EnvConfig
from sysgym.envs.env_measure import EnvMeasurements
from sysgym.envs.params_dict_abc import EnvParamsDict
from sysgym.project import ExperimentManager
from sysgym.spaces.schema import ParamSchema


class Environment(ABC):
    """Environment to optimize"""

    def __init__(self, env_cfg: EnvConfig):
        self.ctx = ExperimentManager()
        self.env_cfg = env_cfg

    @abstractmethod
    def run(self, params: EnvParamsDict) -> EnvMeasurements:
        pass

    @abstractmethod
    def params_holder(self, params_schema: ParamSchema) -> EnvParamsDict:
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
