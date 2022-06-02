from pathlib import Path

from sysgym.envs.gem5.parsers import ParserException
from sysgym.envs.gem5.parsers.regex import summary_file_regex
from sysgym.envs.gem5.stats import BenchmarkStats


def parse_summary_file(summary_file_path: Path) -> BenchmarkStats:
    """Parse a summary file contents and output a BenchmarkStats"""
    # Parses specifically _summary_stats.txt

    with open(summary_file_path) as f:
        summary_file_contents = f.readlines()
    parsed_results = {}
    for line in summary_file_contents:
        line = line.strip()
        if line.startswith("=") or ":" not in line:
            # skip comments lines
            continue

        stats, val = line.split(":")
        stats = _clean_stats_name(stats)
        if stats not in summary_file_regex:
            # skip keys we don't have parsers for
            continue
        stat_parser = summary_file_regex[stats]
        val = val.strip()
        value_match = stat_parser.match(val)
        if not value_match:
            raise ParserException(
                f"Failed to parse: {val} with stat_parser: {stat_parser}"
            )
        value = value_match.group(1)
        parsed_results[stats] = float(value)

    return BenchmarkStats(**parsed_results)


def _clean_stats_name(stats: str) -> str:
    """Clean a stats name to be: lower_case_and_no_of"""
    return (
        stats.lower()
        .replace("(32-bit)", "")
        .strip()
        .replace(" of", "")
        .replace(" ", "_")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )
