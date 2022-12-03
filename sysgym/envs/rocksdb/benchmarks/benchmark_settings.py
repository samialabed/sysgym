from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class BenchmarkSettings(ABC):
    @abstractmethod
    def as_cmd(self) -> List[str]:
        pass
