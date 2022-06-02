import dataclasses
from dataclasses import dataclass
from typing import Dict

import pandas as pd

from sysgym.envs.gem5.parsers.regex import PERFORMANCE_PARSER, SYSTEM_RES_PARSER
from sysgym.envs.gem5.stats.system_stats import Gem5SystemStats


@dataclass
class Gem5DetailedStats:
    system: Gem5SystemStats
    performance: pd.DataFrame

    def as_dict(self) -> Dict[str, any]:
        system_dict = dataclasses.asdict(self.system)
        performance_dict = self.performance.to_dict(orient="records")[0]
        return {**system_dict, **performance_dict}

    @staticmethod
    def populate_from_sim(sim: str):
        system_df = (
            pd.DataFrame(SYSTEM_RES_PARSER.findall(sim)).set_index(0).T.astype(float)
        )

        performance_df = (
            pd.DataFrame(PERFORMANCE_PARSER.findall(sim)).set_index(0).T.astype(float)
        )
        return Gem5DetailedStats(system=system_df, performance=performance_df)

    def __add__(self, other: "Gem5DetailedStats"):
        res = {}
        for f in dataclasses.fields(self):
            field_name = f.name
            res[field_name] = getattr(self, field_name) + getattr(other, field_name)

        return Gem5DetailedStats(**res)
