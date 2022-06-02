from dataclasses import dataclass
from typing import Dict

from sysgym.envs.env_measure import EnvMeasurements
from sysgym.envs.params_dict_abc import EnvParamsDict


@dataclass(frozen=True)
class EnvState:
    params: EnvParamsDict
    measurements: EnvMeasurements

    def as_dict(self) -> Dict[str, any]:
        params_dict = dict(self.params.items())
        measurements_dict = self.measurements.as_flat_dict()

        return {**params_dict, **measurements_dict}
