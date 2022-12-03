import logging
import re
from collections import defaultdict
from typing import Dict, List, Optional

from sysgym.envs.rocksdb.parsers.constant_regex import ALPHANUM, NUM
from sysgym.envs.rocksdb.parsers.constant_types import NUM_VALUE
from sysgym.envs.rocksdb.parsers.parser import Parser
from sysgym.envs.rocksdb.parsers.utils import (
    clean_key,
    merge_dictionary,
    parse_number_in_string,
)
from sysgym.envs.rocksdb.stats.file_read_dao import FileReadStats

LOG = logging.getLogger("sysgym")


class FileReadByLevelParser(Parser):
    def __init__(self):
        super().__init__("file_read")
        # Regex matching: alphaNum: floatNum
        self._regex = re.compile(f"({ALPHANUM}): ({NUM})")
        self._level_regex = re.compile(r"Level (\d+)")

    def parse_lines(self, lines: List[str]) -> List[FileReadStats]:
        parsed_stats: List[FileReadStats] = []
        parsed_values_at_level: Dict[int, Dict[str, NUM_VALUE]] = defaultdict(dict)
        current_level: int = -1
        skip_until_level = True

        for line in lines:
            line = line.strip()
            if not line:
                # empty line, break point
                LOG.debug(f"Found the termination line for level: {current_level}.")
                # skip this line
                continue

            is_level = self._level_regex.findall(line)
            if is_level:
                # New level breakpoint, extract and capture the level
                current_level = int(is_level[0])
                LOG.debug(f"Parsing values at level: {current_level}")
                # start collecting metric values
                skip_until_level = False
                continue
            elif skip_until_level:
                # Skip lines until we meet new level.
                # We have already captured all the data we need from this level
                continue
            else:
                extracted_values = self.parse(line)
                if not extracted_values:
                    # Line isn't parse-able
                    continue
                previous_values = parsed_values_at_level[current_level]
                metrics_so_far = merge_dictionary(previous_values, extracted_values)
                parsed_values_at_level[current_level] = metrics_so_far

                if len(metrics_so_far) + 2 == len(FileReadStats.__slots__):
                    # convert what we have already to a stats
                    LOG.debug("Finished collecting the stats of this level.")
                    stats_dao = FileReadStats(
                        name=f"FileReadStatsLevel{current_level}",
                        level=current_level,
                        **parsed_values_at_level[current_level],
                    )
                    parsed_stats.append(stats_dao)
                    skip_until_level = True

        return parsed_stats

    def parse(self, line: str) -> Optional[Dict[str, NUM_VALUE]]:
        metrics_values_str = self._regex.findall(line)

        if metrics_values_str:
            extracted_metrics_values = {}
            for (k, v) in metrics_values_str:
                extracted_metrics_values[clean_key(k)] = parse_number_in_string(v)
            return extracted_metrics_values
        return None
