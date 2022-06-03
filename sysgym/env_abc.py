from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from dataclasses_json import dataclass_json

from sysgym.param_dict import EnvParamsDict


@dataclass_json
@dataclass(frozen=True)
class EnvMetrics(ABC):
    @abstractmethod
    def as_flat_dict(self) -> Dict[str, any]:
        """Metrics of the environment as a dictionary"""


@dataclass_json
@dataclass(frozen=True)
class EnvConfig(ABC):
    artifacts_output_dir: Path  # directory storing the system artifacts and metrics

    @property
    @abstractmethod
    def name(self):
        """Name of the environment"""

    def __post_init__(self):
        self.artifacts_output_dir.mkdir(parents=True, exist_ok=True)


class Environment(ABC):
    """Environment to optimize"""

    def __init__(self, env_cfg: EnvConfig):
        self.env_cfg = env_cfg

    @abstractmethod
    def run(self, params: EnvParamsDict) -> EnvMetrics:
        """Run the environment using the provided parameters."""

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
