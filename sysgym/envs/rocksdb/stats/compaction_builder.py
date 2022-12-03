import logging
import re
from typing import List, Optional, Tuple

from sysgym.envs.rocksdb.parsers.utils import ensure_value_in_mb
from sysgym.envs.rocksdb.stats.compaction_dao import PerLevelCompactionStats

LOG = logging.getLogger("sysgym")


class CompactionStatsLevelStatsBuilder(object):
    # TODO this very complicated we should consider simplifying it at some point
    def __init__(self, line: List[str]):

        self._level_regex = re.compile(r"L(\d*)")
        self._value_parse_measure_regex = re.compile(r"(\d*)([a-zA-Z])")
        # levels parsing
        self.line = line

    def parse_level(self, level_line: str) -> Optional[int]:
        parsed_level = self._level_regex.findall(level_line)
        if len(parsed_level) != 1:
            LOG.error(f"Found level {level_line} in level parsing, skipping...")
            return
        level = int(parsed_level[0])
        return level

    def parse_files(self, files_line: str) -> Tuple[int, int]:
        # files_line parsing
        input_files, output_files = files_line.split("/")
        input_files = int(input_files)
        output_files = int(output_files)
        return input_files, output_files

    def parse_size(self, size: str, size_measurement: str) -> float:
        return ensure_value_in_mb(size, size_measurement)

    def parse_score(self, score_line: str) -> float:
        score = float(score_line)
        return score

    def parse_read_gb(self, read_gb_line: str) -> float:
        read_gb = float(read_gb_line)
        return read_gb

    def parse_rn_gb(self, rn_gb_line: str) -> float:
        rn_gb = float(rn_gb_line)
        return rn_gb

    def parse_rnp1_gb(self, rnp1_gb_line: str) -> float:
        rnp1_gb = float(rnp1_gb_line)
        return rnp1_gb

    def parse_write_gb(self, write_gb_line: str) -> float:
        write_gb = float(write_gb_line)
        return write_gb

    def parse_wnew_gb(self, wnew_gb_line: str) -> float:
        wnew_gb = float(wnew_gb_line)
        return wnew_gb

    def parse_moved_gb(self, moved_gb_line: str) -> float:
        moved_gb = float(moved_gb_line)
        return moved_gb

    def parse_w_amp(self, w_amp_line: str) -> float:
        w_amp = float(w_amp_line)
        return w_amp

    def parse_rd_mb_per_s(self, rd_mb_per_s_line: str) -> float:
        rd_mb_per_s = float(rd_mb_per_s_line)
        return rd_mb_per_s

    def parse_wr_mb_per_s(self, wr_mb_per_s_line: str) -> float:
        wr_mb_per_s = float(wr_mb_per_s_line)
        return wr_mb_per_s

    def parse_comp_sec(self, comp_sec_line: str) -> float:
        comp_sec = float(comp_sec_line)
        return comp_sec

    def parse_comp_merge_cpu_sec(self, comp_merge_cpu_sec_line: str) -> float:
        comp_merge_cpu_sec = float(comp_merge_cpu_sec_line)
        return comp_merge_cpu_sec

    def parse_comp_cnt(self, comp_cnt_line: str) -> float:
        comp_cnt = float(comp_cnt_line)
        return comp_cnt

    def parse_avg_sec(self, avg_sec_line: str) -> float:
        avg_sec = float(avg_sec_line)
        return avg_sec

    def parse_key_in(self, key_in_line: str):
        matches = self._value_parse_measure_regex.findall(key_in_line)
        if len(matches) != 1:
            # doesn't contain measurement, only number
            key_in = float(key_in_line)
        else:
            key_in_value, key_in_measure = matches[0]
            key_in = ensure_value_in_mb(key_in_value, key_in_measure)
        key_in = key_in
        return key_in

    def parse_key_drop(self, key_drop_line: str):
        matches = self._value_parse_measure_regex.findall(key_drop_line)
        if len(matches) != 1:
            key_drop = float(key_drop_line)
        else:
            key_drop_value, key_drop_measure = matches[0]
            key_drop = ensure_value_in_mb(key_drop_value, key_drop_measure)
        key_drop = key_drop
        return key_drop

    def build(self) -> Optional[PerLevelCompactionStats]:
        line = self.line
        level = self.parse_level(line[0])

        if level is None:
            return None

        out_files, in_files = self.parse_files(line[1])
        size_mb = self.parse_size(line[2], line[3])
        score = self.parse_score(line[4])
        read_gb = self.parse_read_gb(line[5])
        rn_gb = self.parse_rn_gb(line[6])
        rnp1_gb = self.parse_rnp1_gb(line[7])
        write_gb = self.parse_write_gb(line[8])
        wnew_gb = self.parse_wnew_gb(line[9])
        moved_gb = self.parse_moved_gb(line[10])
        w_amp = self.parse_w_amp(line[11])
        rd_mb_per_s = self.parse_rd_mb_per_s(line[12])
        wr_mb_per_s = self.parse_wr_mb_per_s(line[13])
        comp_sec = self.parse_comp_sec(line[14])
        comp_merge_cpu_sec = self.parse_comp_merge_cpu_sec(line[15])
        comp_cnt = self.parse_comp_cnt(line[16])
        avg_sec = self.parse_avg_sec(line[17])
        key_in = self.parse_key_in(line[18])
        key_drop = self.parse_key_drop(line[19])

        return PerLevelCompactionStats(
            level=level,
            in_files=in_files,
            out_files=out_files,
            size_mb=size_mb,
            score=score,
            read_gb=read_gb,
            rn_gb=rn_gb,
            rnp1_gb=rnp1_gb,
            write_gb=write_gb,
            wnew_gb=wnew_gb,
            moved_gb=moved_gb,
            w_amp=w_amp,
            rd_mb_per_s=rd_mb_per_s,
            wr_mb_per_s=wr_mb_per_s,
            comp_sec=comp_sec,
            comp_merge_cpu_sec=comp_merge_cpu_sec,
            comp_cnt=comp_cnt,
            avg_sec=avg_sec,
            key_in=key_in,
            key_drop=key_drop,
        )
