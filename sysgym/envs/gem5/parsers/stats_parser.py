import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd

from sysgym.envs.gem5.parsers.regex import performance_parser, system_parser


@dataclass
class Gem5SystemStatistics(object):
    final_tick: int = 0  # Number of ticks from beginning of simulation
    host_inst_rate: int = 0  # Simulator instruction rate (inst/s)
    host_mem_usage: int = 0  # Number of bytes of host memory used
    host_op_rate: int = 0  # Simulator op (including micro ops) rate (op/s)
    host_seconds: float = 0  # Real time elapsed on the host
    host_tick_rate: int = 0  # Simulator tick rate (ticks/s)
    sim_insts: int = 0  # Number of instructions simulated
    sim_ops: int = 0  # Number of ops (including micro ops) simulated
    sim_seconds: float = 0  # Number of seconds simulated
    sim_ticks: int = 0  # Number of ticks simulated

    def as_df(self) -> pd.DataFrame:
        return pd.DataFrame(dataclasses.asdict(self), index=[0]).T.astype(float)

    @staticmethod
    def from_df(df: pd.DataFrame) -> "Gem5SystemStatistics":
        return Gem5SystemStatistics(**df.to_dict())

    @staticmethod
    def from_str(s: str) -> "Gem5SystemStatistics":
        parsed_stats = dict(system_parser.findall(s))

        stats = {}
        for f in dataclasses.fields(Gem5SystemStatistics):
            stats[f.name] = f.type(parsed_stats[f.name])
        return Gem5SystemStatistics(**stats)

    def __add__(self, other: "Gem5SystemStatistics"):
        res = {}
        for f in dataclasses.fields(self):
            field_name = f.name
            res[field_name] = getattr(self, field_name) + getattr(other, field_name)

        return Gem5SystemStatistics(**res)


@dataclass
class Gem5AllStatistics:
    system: Gem5SystemStatistics
    performance: pd.DataFrame

    def as_dict(self) -> Dict[str, any]:
        system_dict = dataclasses.asdict(self.system)
        performance_dict = self.performance.to_dict(orient="records")[0]
        return {**system_dict, **performance_dict}

    @staticmethod
    def populate_from_sim(sim: str):
        system_df = (
            pd.DataFrame(system_parser.findall(sim)).set_index(0).T.astype(float)
        )

        performance_df = (
            pd.DataFrame(performance_parser.findall(sim)).set_index(0).T.astype(float)
        )
        return Gem5AllStatistics(system=system_df, performance=performance_df)

    def __add__(self, other: "Gem5AllStatistics"):
        res = {}
        for f in dataclasses.fields(self):
            field_name = f.name
            res[field_name] = getattr(self, field_name) + getattr(other, field_name)

        return Gem5AllStatistics(**res)


def parse_statistics(stats_fp: Path) -> Gem5AllStatistics:
    # Parses specifically stats.txt
    with open(stats_fp, "r") as f:
        contents = f.read()

    # simulation dumps data periodically or when it reset,
    # the token says when new dump started
    begin_sim_dump_token = "\n---------- Begin Simulation Statistics ----------\n"
    simulations = contents.split(begin_sim_dump_token)

    cumulative_system_metrics = None
    for sim in simulations:
        if not sim:
            # skip empty lines.
            # reason to not use enumerate: some lines are empty
            continue

        system_stats = Gem5AllStatistics.populate_from_sim(sim)
        if cumulative_system_metrics is None:
            cumulative_system_metrics = system_stats
        else:
            cumulative_system_metrics = cumulative_system_metrics + system_stats
        assert (
            cumulative_system_metrics
        ), "Expected to create a cumulative system metric"
    return cumulative_system_metrics
