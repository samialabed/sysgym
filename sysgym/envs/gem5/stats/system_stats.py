import dataclasses
from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class Gem5SystemStats:
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
    def from_df(df: pd.DataFrame) -> "Gem5SystemStats":
        stats_input = {}
        for field in dataclasses.fields(Gem5SystemStats):
            stats_input[field.name] = df[field.name].values
        stats = Gem5SystemStats(**stats_input)
        return stats

    @staticmethod
    def from_dict(res: Dict[str, any]) -> "Gem5SystemStats":
        stats_input = {}
        for f in dataclasses.fields(Gem5SystemStats):
            stats_input[f.name] = f.type(res[f.name])
        stats = Gem5SystemStats(**stats_input)
        return stats

    def __add__(self, other: "Gem5SystemStats"):
        res = {}
        for f in dataclasses.fields(self):
            field_name = f.name
            if field_name == "final_tick":
                res[field_name] = max(
                    getattr(self, field_name), getattr(other, field_name)
                )
            else:
                res[field_name] = getattr(self, field_name) + getattr(other, field_name)

        return Gem5SystemStats(**res)
