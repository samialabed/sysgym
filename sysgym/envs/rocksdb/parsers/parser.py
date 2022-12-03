from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from sysgym.envs.rocksdb.stats.stats_dao import Statistics


class Parser(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def parse(self, line: str) -> Optional[Statistics]:
        pass

    def parse_lines(self, lines: List[str]) -> Dict[str, Statistics]:
        """Parse chunk of lines related to the parser
        return a list of bespoke stats."""
        parsed_stats = {}
        for line in lines:
            parsed_line = self.parse(line)
            if parsed_line:
                parsed_stats[parsed_line.name] = parsed_line
        return parsed_stats

    def __str__(self):
        return f"{self.name} parser."
