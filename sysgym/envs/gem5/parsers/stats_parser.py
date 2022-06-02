from pathlib import Path

from sysgym.envs.gem5.stats.detailed_stats import Gem5DetailedStats


def parse_statistics(stats_fp: Path) -> Gem5DetailedStats:
    # Parses specifically stats.txt
    with open(stats_fp, "r") as f:
        contents = f.read()

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

        system_stats = Gem5DetailedStats.populate_from_sim(sim)
        if cumulative_system_metrics is None:
            cumulative_system_metrics = system_stats
        else:
            cumulative_system_metrics = cumulative_system_metrics + system_stats
        assert (
            cumulative_system_metrics
        ), "Expected to create a cumulative system metric"
    return cumulative_system_metrics
