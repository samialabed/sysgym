import logging
from pathlib import Path
from typing import Dict, List, Optional

from sysgym.envs.rocksdb.parsers.compaction_stats_parser import CompactionStatsParser
from sysgym.envs.rocksdb.parsers.dbbench_parser import DBBenchParser
from sysgym.envs.rocksdb.parsers.level_file_read_parser import FileReadByLevelParser
from sysgym.envs.rocksdb.parsers.parser import Parser
from sysgym.envs.rocksdb.parsers.statistics_parser import StatisticsParser
from sysgym.envs.rocksdb.stats.parser_factory_dao import BenchmarkStats

LOG = logging.getLogger("sysgym")


def parse_res_file(file_path: Path) -> BenchmarkStats:
    parser = ParserFactory()
    with open(file_path) as f:
        lines = f.readlines()
    stats = parser.parse_lines(lines)
    return stats


class ParsersTrigger(object):
    # TODO: surely there is a better way of doing this than this hack.
    DBBench = "------------------------------------------------"
    Compactions = "** Compaction Stats [default] **"
    Files = "** File Read Latency Histogram By Level [default] **"
    Statistics = "STATISTICS:"


class ParserFactory(object):
    def __init__(
        self,
        parse_dbbench: bool = True,
        parse_compaction_stats: bool = True,
        parse_file_read_stats: bool = True,
        parse_statistics: bool = True,
    ):
        self._parser_switcher: Dict[str, Parser] = {}

        if parse_dbbench:
            self._parser_switcher[ParsersTrigger.DBBench] = DBBenchParser()

        if parse_compaction_stats:
            self._parser_switcher[ParsersTrigger.Compactions] = CompactionStatsParser()

        if parse_file_read_stats:
            self._parser_switcher[ParsersTrigger.Files] = FileReadByLevelParser()

        if parse_statistics:
            self._parser_switcher[ParsersTrigger.Statistics] = StatisticsParser()

        self._stats_map = {}

    def parse_lines(self, lines: List[str]) -> BenchmarkStats:

        active_parser: Optional[Parser] = None
        all_stats_map = {}

        chunk_to_parse = []
        for line in lines:
            line = line.strip()
            if line not in self._parser_switcher:
                # Not a new parser
                if active_parser:
                    # we have an active parser
                    chunk_to_parse.append(line)
            elif self._parser_switcher[line] != active_parser:
                # we have a new parser to use
                if active_parser:
                    # We had a parser before, parse the content we collected so far
                    parsed_chunk = active_parser.parse_lines(chunk_to_parse)
                    all_stats_map[active_parser.name] = parsed_chunk

                # switch to new parser and empty the chunk
                active_parser = self._parser_switcher[line]
                chunk_to_parse = []

        if len(chunk_to_parse) != 0 and active_parser:
            parsed_chunk = active_parser.parse_lines(chunk_to_parse)
            all_stats_map[active_parser.name] = parsed_chunk

        return BenchmarkStats(**all_stats_map)
