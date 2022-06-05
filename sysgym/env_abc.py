from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from dataclasses_json import dataclass_json

from sysgym.param_dict import EnvParamsDict


class BenchmarkConfig(ABC):
    # TODO: this placeholder until we refactor the benchmark out of the env cfg
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the benchmark being executed."""


@dataclass_json
@dataclass(frozen=True)
class EnvMetrics(ABC):
    @abstractmethod
    def as_flat_dict(self) -> Dict[str, any]:
        """Metrics of the environment as a dictionary"""


@dataclass_json
@dataclass(frozen=True)
class EnvConfig(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the environment"""


class Environment(ABC):
    """Environment runner"""

    def __init__(self, env_cfg: EnvConfig, artifacts_output_dir: Path):
        """


        :param env_cfg:
        :param artifacts_output_dir: directory storing the system artifacts and metrics

        """
        self.env_cfg = env_cfg
        self.artifacts_output_dir = artifacts_output_dir
        self.artifacts_output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def run(self, params: EnvParamsDict) -> EnvMetrics:
        """Run the environment using the provided parameters."""

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
