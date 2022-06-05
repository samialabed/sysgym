import math
from dataclasses import asdict, dataclass
from typing import Dict

from dataclasses_json import dataclass_json

from sysgym.env_abc import EnvMetrics
from sysgym.envs.gem5.stats import Gem5DetailedStats, SummaryStats


@dataclass_json
@dataclass(frozen=True)
class Gem5Metrics(EnvMetrics):
    summary_stats: SummaryStats
    detailed_stats: Gem5DetailedStats

    def as_flat_dict(self) -> Dict[str, any]:
        bench_stats_dict = asdict(self.summary_stats)
        detailed_stats_dict = self.detailed_stats.as_dict()

        return {**bench_stats_dict, **detailed_stats_dict}

    @property
    def log_pdp(self) -> float:
        """pdp: power * 1/time"""
        return math.log(self.summary_stats.avg_power) + math.log(
            1 / self.detailed_stats.system.sim_seconds
        )

    @property
    def log_epd(self) -> float:
        """EPD: now it is power * 1/time^2"""
        return self.log_pdp + math.log(1 / self.detailed_stats.system.sim_seconds)

    @property
    def pdp(self) -> float:
        """pdp: power * 1/time"""
        return self.summary_stats.avg_power * (
            1 / self.detailed_stats.system.sim_seconds
        )

    @property
    def epd(self) -> float:
        """EPD: now it is power * 1/time^2"""
        return self.pdp * (1 / self.detailed_stats.system.sim_seconds)
