from dataclasses import dataclass, fields
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class DBBenchBenchmarksOptions(object):
    fillseq: bool = False  # write N values in sequential k order in async mode
    fill100K: bool = False  # write N/1000 100K values in random order in async mode
    fillrandom: bool = False  # write N values in random k order in async mode
    deleteseq: bool = False  # delete N keys in sequential order
    deleterandom: bool = False  # delete N keys in random order
    readseq: bool = False  # read N times sequentially
    readrandom: bool = False  # read N times in random order
    readwhilewriting: bool = False  # 1 writer, N threads doing random reads
    readwhilemerging: bool = False  # 1 merger, N threads doing random reads
    updaterandom: bool = False  # N threads doing read-modify-write for random keys
    appendrandom: bool = False  # N threads doing read-modify-write with growing values
    mergerandom: bool = False  # same as (update/append)random using merge operator.
    filluniquerandom: bool = False  # write N values in a random k order
    mixgraph: bool = False  # allow expressing the qps using sine wave
    readrandomwriterandom: bool = False  # N threads doing random-read, random-write
    # statistics
    sstables: bool = False  # print sstables stats
    levelstats: bool = False  # print the number of files and bytes per level
    stats: bool = True  # default to collect detailed stats

    def as_settings(self) -> str:
        """Expected settings is of the form: opt1,opt2,opt3."""
        out = []
        for field in fields(self):
            if getattr(self, field.name):
                out.append(field.name)
        return ",".join(out)

    @property
    def enabled_benchmarks(self) -> List[str]:
        out = []
        for field in fields(self):
            if getattr(self, field.name) and field.name != "stats":
                out.append(field.name)
        return out
