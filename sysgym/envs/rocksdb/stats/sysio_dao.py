from dataclasses import dataclass
from typing import List

import numpy as np
from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.statistics_dao import MicroStats


@dataclass_json
@dataclass
class SystemIO:
    __slots__ = ["cpu_usage", "mem_usage", "exe_time"]
    cpu_usage: MicroStats
    mem_usage: MicroStats
    exe_time: float

    def __init__(self, cpu_usage: List[float], mem_usage: List[float], exe_time: float):

        cpu_p50, cpu_p95, cpu_p99, cpu_p100 = np.percentile(
            cpu_usage, [50, 95, 99, 100]
        )

        self.cpu_usage = MicroStats(
            name="cpu_usage",
            p50=cpu_p50,
            p95=cpu_p95,
            p99=cpu_p99,
            p100=cpu_p100,
            count=len(cpu_usage),
            sum=sum(cpu_usage),
        )

        mem_p50, mem_p95, mem_p99, mem_p100 = np.percentile(
            mem_usage, [50, 95, 99, 100]
        )

        self.mem_usage = MicroStats(
            name="mem_usage",
            p50=mem_p50,
            p95=mem_p95,
            p99=mem_p99,
            p100=mem_p100,
            count=len(mem_usage),
            sum=sum(mem_usage),
        )

        self.exe_time = exe_time
