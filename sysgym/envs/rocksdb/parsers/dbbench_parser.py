import logging
import re
from typing import Optional

from sysgym.envs.rocksdb.parsers.constant_regex import NUM
from sysgym.envs.rocksdb.parsers.parser import Parser
from sysgym.envs.rocksdb.parsers.utils import clean_key, ensure_value_in_mb
from sysgym.envs.rocksdb.stats.db_bench_dao import DBBenchStatistics

LOG = logging.getLogger("sysgym")


class DBBenchParser(Parser):
    def __init__(self):
        super().__init__("db_bench")
        self._regex = re.compile(
            rf"\s*({NUM}) micros/op ({NUM}) ops/sec;\s*({NUM}) (\w+)"
        )

    def parse(self, line: str) -> Optional[DBBenchStatistics]:
        key, _, value = line.partition(":")
        if value:
            parsed_values = self._regex.findall(value)
            if len(parsed_values) == 1:
                latency, iops, io_size, io_measure = parsed_values[0]
                latency = float(latency)
                iops = float(iops)
                io_size = ensure_value_in_mb(io_size, io_measure)
                return DBBenchStatistics(
                    name=clean_key(key), latency=latency, iops=iops, io_size=io_size
                )

        LOG.debug(f"Skipping DBBenchParser line: {line}")
        return None
