import logging
import re
from typing import Dict, List, Optional

from sysgym.envs.rocksdb.parsers.constant_regex import NUM
from sysgym.envs.rocksdb.parsers.parser import Parser
from sysgym.envs.rocksdb.parsers.utils import (
    clean_key,
    ensure_value_in_mb,
    parse_number_in_string,
)
from sysgym.envs.rocksdb.stats.compaction_builder import (
    CompactionStatsLevelStatsBuilder,
)
from sysgym.envs.rocksdb.stats.compaction_dao import (
    COMPACTION_PARSER_TYPES,
    CompactionGeneralStats,
    CompactionIOStats,
    CompactionStallsStats,
    CompactionStatistics,
    CompactionStatsBase,
    CompactionStatWithKey,
    OverallCompactionStats,
    PerLevelCompactionStats,
)

LOG = logging.getLogger("sysgym")


class CompactionStatsParser(Parser):
    # TODO: we should look into refactoring it
    def __init__(self):
        super().__init__("compaction_statistics")
        self._mode = None  # Either Level or Priority

        val_size_reg = f"({NUM}) ([A-Z][A-Z])"
        self._priority_compaction_regex = re.compile(
            f"{val_size_reg} write, {val_size_reg}/s write,"
            f" {val_size_reg} read, {val_size_reg}/s read,"
            f" ({NUM}) seconds"
        )
        self._priority_files_regex = re.compile(f"cumulative ({NUM}), interval ({NUM})")

        self._priority_stalls_regex = re.compile(rf"({NUM}) (\w*)")

    def parse_lines(self, lines: List[str]) -> CompactionStatistics:
        levels_compaction_stats = []
        overall_compaction_stats: Dict[str, CompactionStatsBase] = {}

        for line in lines:
            line = line.strip()
            if not line or "----" in line or "**" in line:
                continue  # skip line
            parsed_values = self.parse(line)
            if parsed_values:
                if isinstance(parsed_values, PerLevelCompactionStats):
                    levels_compaction_stats.append(parsed_values)
                elif isinstance(parsed_values, CompactionStatWithKey):
                    overall_compaction_stats[parsed_values.key] = parsed_values.value

        return CompactionStatistics(
            name="CompactionStatistics",
            overall_compaction_stats=OverallCompactionStats(**overall_compaction_stats),
            per_level_compaction_stats=levels_compaction_stats,
        )

    def parse(self, line: str) -> Optional[COMPACTION_PARSER_TYPES]:
        if ":" in line:
            return self._parse_overall_compaction_line(line)
        elif re.findall(r"L(\d+)", line):
            # LEVEL STUFF
            level_line_stats = self._parse_compaction_level(line)
            return level_line_stats
        return None

    @staticmethod
    def _parse_compaction_level(line: str) -> Optional[PerLevelCompactionStats]:
        if not line:
            return None

        slitted_line = line.split()

        if len(slitted_line) != 20 or "L" not in slitted_line[0]:
            LOG.debug(
                "Skipping line.... Expected the line to contain 20 items with first "
                "item being LevelNum. Instead has %s. Full line: %s",
                len(slitted_line),
                line,
            )
            # not a level stat
            return None
        compaction_stats = CompactionStatsLevelStatsBuilder(slitted_line).build()
        return compaction_stats

    def _parse_overall_compaction_line(
        self, line: str
    ) -> Optional[CompactionStatWithKey]:
        key, _, metrics = line.partition(":")
        if not metrics:
            return None

        key = clean_key(key)

        if "uptime" in key:
            parsed_value = re.findall(f"({NUM}) total, ({NUM}) interval", metrics)
            if not parsed_value:
                return None

            total_sec, interval_sec = parsed_value[0]
            val = CompactionGeneralStats(
                total=float(total_sec), interval=float(interval_sec)
            )
        elif "stalls" in key:
            parsed_metrics = self._priority_stalls_regex.findall(metrics)
            if not parsed_metrics:
                return None

            parsed_values = {}
            for (v, k) in parsed_metrics:
                # value is on left, key is on the right for some weird ROCKSDB reason...
                parsed_values[k] = parse_number_in_string(v)
            val = CompactionStallsStats(**parsed_values)
        elif "compaction" in key:
            parsed_values = self._priority_compaction_regex.findall(metrics)
            if not parsed_values:
                return None

            [
                write_size,
                write_measure,
                write_throughput,
                write_throughput_measurement,
                read_size,
                read_size_measurement,
                read_throughput,
                read_throughput_measurement,
                seconds,
            ] = parsed_values[0]
            # ensure all values in mb
            write_size = ensure_value_in_mb(write_size, write_measure)
            write_throughput = ensure_value_in_mb(
                write_throughput, write_throughput_measurement
            )
            read_size = ensure_value_in_mb(read_size, read_size_measurement)
            read_throughput = ensure_value_in_mb(
                read_throughput, read_throughput_measurement
            )
            val = CompactionIOStats(
                write_size_mb=write_size,
                write_throughput=write_throughput,
                read_size_mb=read_size,
                read_throughput=read_throughput,
                time_sec=parse_number_in_string(seconds),
            )
        elif "interval" in line and "cumulative" in line:
            parsed_value = self._priority_files_regex.findall(metrics)
            if not parsed_value:
                return None
            cumulative, interval = parsed_value[0]
            cumulative = parse_number_in_string(cumulative)
            interval = parse_number_in_string(interval)
            val = CompactionGeneralStats(total=cumulative, interval=interval)
        else:
            return None
        return CompactionStatWithKey(key=key, value=val)
