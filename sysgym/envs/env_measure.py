from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class EnvMeasurements(ABC):
    @abstractmethod
    def as_flat_dict(self) -> Dict[str, any]:
        """Metrics of the environment as a dictionary"""
