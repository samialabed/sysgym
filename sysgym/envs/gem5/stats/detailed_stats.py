import dataclasses
from dataclasses import dataclass
from typing import Dict

import pandas as pd

from sysgym.envs.gem5.stats.system_stats import Gem5SystemStats


@dataclass
class Gem5DetailedStats:
    system: Gem5SystemStats
    performance: pd.DataFrame

    @staticmethod
    def from_df(
        system_df: pd.DataFrame, performance_df: pd.DataFrame
    ) -> "Gem5DetailedStats":
        return Gem5DetailedStats(
            system=Gem5SystemStats.from_df(system_df), performance=performance_df
        )

    def as_dict(self) -> Dict[str, any]:
        system_dict = dataclasses.asdict(self.system)
        performance_dict = self.performance.to_dict(orient="records")[0]
        return {**system_dict, **performance_dict}

    def __add__(self, other: "Gem5DetailedStats"):
        res = {}
        for field in dataclasses.fields(self):
            field_name = field.name
            res[field_name] = getattr(self, field_name) + getattr(other, field_name)

        return Gem5DetailedStats(**res)
