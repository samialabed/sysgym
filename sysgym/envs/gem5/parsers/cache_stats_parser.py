from pathlib import Path

from sysgym.envs.gem5.parsers.regex import CACHE_STATS_PARSER
from sysgym.envs.gem5.stats import CacheStats


def parse_cache_stats_file(cache_stats_fp: Path) -> CacheStats:
    """Parse a summary file contents and output a SummaryStats."""
    # Parses specifically _cache_stats.txt
    with open(cache_stats_fp) as f:
        contents = f.read()
    matched_res = CACHE_STATS_PARSER.findall(contents)
    parsed_results = {k: float(v) for k, v in matched_res}

    return CacheStats(**parsed_results)


def _clean_key(k: str) -> str:
    """Make sure the name is compatible with cache stats"""
    return k.replace("-", "_")
