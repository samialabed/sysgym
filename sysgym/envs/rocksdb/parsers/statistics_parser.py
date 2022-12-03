import logging
import re
from typing import List, Optional

from sysgym.envs.rocksdb.parsers.constant_regex import NUM
from sysgym.envs.rocksdb.parsers.parser import Parser
from sysgym.envs.rocksdb.parsers.utils import clean_key, parse_number_in_string
from sysgym.envs.rocksdb.stats.rocksdb_stats import RocksDBStatistics, StatisticsType
from sysgym.envs.rocksdb.stats.statistics_dao import MacroStats, MicroStats

LOG = logging.getLogger("sysgym")


class StatisticsParser(Parser):
    def __init__(self):
        super().__init__("statistics")
        self._regex = re.compile(f"([a-zA-Z0-9]+) : ({NUM})")

    def parse(self, line: str) -> Optional[StatisticsType]:
        key, _, values = line.partition(" ")
        if values:
            metrics_values_str = self._regex.findall(values)
            metrics_values = {}
            for (k, v) in metrics_values_str:
                metrics_values[clean_key(k)] = parse_number_in_string(v)
            metric_name = clean_key(key)

            if len(metrics_values) + 1 == len(MacroStats.__slots__):
                return MacroStats(name=metric_name, **metrics_values)
            if len(metrics_values) + 1 == len(MicroStats.__slots__):
                return MicroStats(name=metric_name, **metrics_values)

        LOG.debug("Skipping DBBenchParser line: %s", line)
        return None

    def parse_lines(self, lines: List[str]) -> RocksDBStatistics:
        parsed_stats = {}
        for line in lines:
            parsed_line = self.parse(line)
            if parsed_line:
                parsed_stats[parsed_line.name] = parsed_line
        return RocksDBStatistics(name="RocksDBStatistics", **parsed_stats)
