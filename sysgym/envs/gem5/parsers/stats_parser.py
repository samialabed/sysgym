from pathlib import Path

import pandas as pd

from sysgym.envs.gem5.parsers.regex import PERFORMANCE_PARSER, SYSTEM_RES_PARSER
from sysgym.envs.gem5.stats import Gem5DetailedStats, Gem5SystemStats


def parse_statistics(stats_fp: Path) -> Gem5DetailedStats:
    # Parses specifically stats.txt
    with open(stats_fp, "r") as file:
        contents = file.read()

    # simulation dumps data periodically or when it reset,
    # the token says when new dump started
    begin_sim_dump_token = "\n---------- Begin Simulation Statistics ----------\n"
    simulations = contents.split(begin_sim_dump_token)

    cumulative_system_metrics = None
    for sim in simulations:
        if not sim:
            # skip empty lines.
            # reason to not use enumerate: some lines are empty
            continue

        # parse the lines and find the core system params and performance params
        all_lines_with_system_info = SYSTEM_RES_PARSER.findall(sim)
        all_lines_with_perf_info = PERFORMANCE_PARSER.findall(sim)

        # Create a DF of the parameters
        performance_df = (
            pd.DataFrame(all_lines_with_perf_info).set_index(0).T.astype(float)
        )

        system_stats = Gem5DetailedStats(
            system=Gem5SystemStats.from_dict(dict(all_lines_with_system_info)),
            performance=performance_df,
        )

        if cumulative_system_metrics is None:
            cumulative_system_metrics = system_stats
        else:
            cumulative_system_metrics = cumulative_system_metrics + system_stats
        assert (
            cumulative_system_metrics
        ), "Expected to create a cumulative system metric"
    return cumulative_system_metrics
