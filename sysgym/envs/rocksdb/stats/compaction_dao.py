from dataclasses import dataclass
from typing import List, Union

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.stats_dao import Statistics


@dataclass_json
@dataclass(frozen=True)
class PerLevelCompactionStats(object):
    """
    * https://github.com/facebook/rocksdb/wiki/Compaction-Stats-and-DB-Status
    * Files: Number of files_line in this level
    * Size: Size of uncompressed data
    * Score: (current level size) / (max level size) => If score is greater than 1 it
     is a candidate for compaction
    * Time: Home many seconds spend in compacting this level
    * Read: Total bytes read during compaction between levels N and N+1
    * Write: Total bytes written during compaction between levels N and N+1
    * Rn: Bytes read from level N during compaction between levels N and N+1
    * Rnp1: Bytes read from level N+1 during compaction between levels N and N+1
    * Wnew: (Rnp1 - Write): New bytes written in this level
    * RW-Amplify: Ratio of how many data has been read to write new data.
            So if this number is big, a lot of data was read during compaction.
            However the effective data written was small. Smaller is better.
            Everything under 60 is OK
    * Read (MB/s): Read speed of the current IO-system
    * Write (MB/s): Write speed of the current IO-system
    * Rn: Files read from level N during compaction between levels N and N+1
    * Rnp1: Files read from level N+1 during compaction between levels N and N+1
    * Wnp1: Files written during compaction between levels N and N+1
    * NewW: (Wnp1 - Rnp1) New files_line creating during compaction within in this level
    * Count: Number of compactions done
    * msCom: Average duration of a single compaction (in milliseconds)
    * msStall: Average duration of a single stall (in milliseconds)
    * Ln-stall: Total time (in milliseconds) of stalls.
    In this time writes to that level were blocked.
    * Stall-cnt: Number of stalls triggered in this level.
            A stall is triggered if the the number of files_line
             within a certain level reach its maximum.
             => Writes are forbidden until a compaction runs.
    """

    __slots__ = [
        "level",
        "in_files",
        "out_files",
        "size_mb",
        "score",
        "read_gb",
        "rn_gb",
        "rnp1_gb",
        "write_gb",
        "wnew_gb",
        "moved_gb",
        "w_amp",
        "rd_mb_per_s",
        "wr_mb_per_s",
        "comp_sec",
        "comp_merge_cpu_sec",
        "comp_cnt",
        "avg_sec",
        "key_in",
        "key_drop",
    ]
    level: int
    in_files: int
    out_files: int
    size_mb: float
    score: float
    read_gb: float
    rn_gb: float
    rnp1_gb: float
    write_gb: float
    wnew_gb: float
    moved_gb: float
    w_amp: float
    rd_mb_per_s: float
    wr_mb_per_s: float
    comp_sec: float
    comp_merge_cpu_sec: float
    comp_cnt: float
    avg_sec: float
    key_in: float
    key_drop: float


@dataclass_json
@dataclass(frozen=True)
class CompactionStatsBase(object):
    pass


@dataclass_json
@dataclass(frozen=True)
class CompactionStallsStats(CompactionStatsBase):
    __slots__ = [
        "level0_slowdown",
        "level0_slowdown_with_compaction",
        "level0_numfiles",
        "level0_numfiles_with_compaction",
        "stop",
        "slowdown",
        "memtable_compaction",
        "memtable_slowdown",
        "total",
    ]

    level0_slowdown: float
    level0_slowdown_with_compaction: float
    level0_numfiles: float
    level0_numfiles_with_compaction: float
    stop: float
    slowdown: float
    memtable_compaction: float
    memtable_slowdown: float
    total: float


@dataclass_json
@dataclass(frozen=True)
class CompactionIOStats(CompactionStatsBase):
    __slots__ = [
        "write_size_mb",
        "write_throughput",
        "read_size_mb",
        "read_throughput",
        "time_sec",
    ]

    write_size_mb: float
    write_throughput: float
    read_size_mb: float
    read_throughput: float
    time_sec: float


@dataclass_json
@dataclass(frozen=True)
class CompactionGeneralStats(CompactionStatsBase):
    __slots__ = ["total", "interval"]
    total: float
    interval: float


@dataclass_json
@dataclass(frozen=True)
class OverallCompactionStats(CompactionStatsBase):
    __slots__ = [
        "uptime_secs",
        "flush_gb",
        "addfile_gb",
        "addfile_total_files",
        "addfile_l0_files",
        "addfile_keys",
        "cumulative_compaction",
        "interval_compaction",
        "stalls",
    ]
    uptime_secs: CompactionGeneralStats
    flush_gb: CompactionGeneralStats
    addfile_gb: CompactionGeneralStats
    addfile_total_files: CompactionGeneralStats
    addfile_l0_files: CompactionGeneralStats
    addfile_keys: CompactionGeneralStats
    cumulative_compaction: CompactionIOStats
    interval_compaction: CompactionIOStats
    stalls_count: CompactionStallsStats


@dataclass_json
@dataclass
class CompactionStatistics(Statistics):
    __slots__ = ["overall_compaction_stats", "per_level_compaction_stats"]
    overall_compaction_stats: OverallCompactionStats
    per_level_compaction_stats: List[PerLevelCompactionStats]


@dataclass_json
@dataclass(frozen=True)
class CompactionStatWithKey(object):
    key: str
    value: CompactionStatsBase


COMPACTION_PARSER_TYPES = Union[CompactionStatWithKey, PerLevelCompactionStats]
