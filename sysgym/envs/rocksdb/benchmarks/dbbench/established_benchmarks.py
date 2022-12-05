from pathlib import Path

from sysgym.envs.rocksdb.benchmarks.dbbench.benchmarks_opts import (
    DBBenchBenchmarksOptions,
)
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench import DBBenchPlan
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench_settings import DBBenchSettings
from sysgym.envs.rocksdb.benchmarks.dbbench.mixgraph_opts import MixGraphDBBenchOptions
from sysgym.utils.enum import BenchmarkTask

_WORKLOAD_DIRS = Path(__file__).parent / "benchmark_cmd"


def convert_to_sec(time_value: int, measure: str):
    # TODO I am sure there is a real lib for this
    sec_to_min = 60
    min_to_hr = 60
    if measure.lower() == "h" or measure.lower() == "hour":
        return time_value * sec_to_min * min_to_hr
    elif measure.lower() == "m" or measure.lower() == "minute":
        return time_value * sec_to_min
    else:
        raise ValueError(f"Unrecognised measurement {measure}")


def read_benchmark(name: str) -> str:
    with open(_WORKLOAD_DIRS / name) as f:
        contents = f.readline()
    return contents


class DBBenchTasks(BenchmarkTask):
    FILL_RANDOM = "fill_random"  # used in NNI
    READ_RANDOM_WRITE_RANDOM = "read_random_write_random"  # Quick no load benchmarks
    # https://www.levyx.com/sites/default/files/white-papers/herocks_facebook_report_2018-02.pdf
    FB_DOC_STORE = "fb_document_store"
    FAST_ZIPPY_WORKLOAD = "fast_zippy_workload"
    TEST_WORKLOAD_1MIN = "test_workload_1min"
    ALL_RANDOM_WORKLOAD = "all_random_workload"
    ZIPPY_WORKLOAD = "zippy_workload"

    def get_plan(self) -> DBBenchPlan:
        if self == DBBenchTasks.FILL_RANDOM:
            return DBBenchPlan(
                # Used in NNI to compare.
                name="fillrandom",
                load_phase=None,
                run_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(fillrandom=True),
                    num=13107200,
                    threads=1,
                    use_existing_db=False,
                    statistics=True,
                    key_size=20,
                    value_size=100,
                    # cache_size=17179869184,
                ),
            )
        if self == DBBenchTasks.READ_RANDOM_WRITE_RANDOM:
            return DBBenchPlan(
                name="readrandomwriterandom",
                load_phase=None,
                run_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(readrandomwriterandom=True),
                    num=13107200,
                    threads=8,
                    use_existing_db=False,
                    statistics=True,
                    cache_size=17179869184,
                    key_size=16,
                    value_size=152,
                    keys_per_prefix=0,
                ),
            )
        if self == DBBenchTasks.FB_DOC_STORE:
            return DBBenchPlan(
                name="fb_document_store",
                load_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(filluniquerandom=True),
                    num=250000000,
                    use_existing_db=False,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    key_size=16,
                    cache_size=2147483648,
                    value_size=152,
                    statistics=False,
                ),
                run_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(readrandomwriterandom=True),
                    num=250000000,
                    threads=16,
                    use_existing_db=False,
                    statistics=True,
                    cache_size=2147483648,
                    key_size=16,
                    value_size=152,
                    keys_per_prefix=0,
                    duration=convert_to_sec(15, "m"),
                ),
            )

        """
        DBBenchPlan from Benchmarking RocksDB in FB infra 
        https://www.usenix.org/system/files/fast20-cao_zhichao.pdf

        The workloads has 0.42 billion queries and 50 million KV-pairs in total.
        Use 30 k-ranges.
        Note that, if user runs the benchmark_container following the 24 hours Sine period, 
        it will take about 22-24 hours.
        In order to speedup the benchmarking, 
        user can increase the sine_d to a larger value such as 45000
        to increase the workload intensiveness and also reduce the sine_b accordingly.

        More information:
            https://github.com/facebook/rocksdb/wiki/RocksDB-Trace%2C-Replay%2C-Analyzer%2C-and-Workload-Generation
        """
        if self == DBBenchTasks.FAST_ZIPPY_WORKLOAD:
            return DBBenchPlan(
                name="zippy_workload_5min",
                load_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(fillrandom=True),
                    num=50000000,
                    use_existing_db=False,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    key_size=48,
                    cache_size=268435456,
                    value_size=43,
                    statistics=False,
                ),
                run_phase=MixGraphDBBenchOptions(
                    benchmarks=DBBenchBenchmarksOptions(mixgraph=True, stats=True),
                    cache_size=268435456,
                    num=50000000,
                    reads=4200000,
                    statistics=True,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    use_existing_db=True,
                    keyrange_dist_a=14.18,
                    keyrange_dist_b=-2.917,
                    keyrange_dist_c=0.0164,
                    keyrange_dist_d=-0.08082,
                    keyrange_num=30,
                    value_k=0.2615,
                    value_sigma=25.45,
                    iter_k=2.517,
                    iter_sigma=14.236,
                    mix_get_ratio=0.85,
                    mix_put_ratio=0.14,
                    mix_seek_ratio=0.01,
                    sine_mix_rate_interval_milliseconds=5000,
                    sine_a=1000,
                    sine_b=0.00000073,
                    sine_d=4500000,
                    perf_level=1,
                    key_size=48,
                    duration=convert_to_sec(5, "m"),
                ),
            )

        if self == DBBenchTasks.TEST_WORKLOAD_1MIN:
            return DBBenchPlan(
                name="test_workload_1min",
                load_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(fillrandom=True),
                    num=100000,
                    use_existing_db=False,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    key_size=48,
                    cache_size=268435456,
                    value_size=43,
                    statistics=False,
                ),
                run_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(fillrandom=True, stats=True),
                    statistics=True,
                    num=100000,
                    duration=convert_to_sec(1, "m"),
                ),
            )
        if self == DBBenchTasks.ALL_RANDOM_WORKLOAD:
            return DBBenchPlan(
                name="all_random_workload_10min",
                load_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(fillrandom=True),
                    num=100000,
                    use_existing_db=False,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    key_size=48,
                    cache_size=268435456,
                    value_size=43,
                    statistics=False,
                ),
                run_phase=MixGraphDBBenchOptions(
                    benchmarks=DBBenchBenchmarksOptions(mixgraph=True, stats=True),
                    cache_size=268435456,
                    num=100000,
                    reads=4200000,
                    statistics=True,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    use_existing_db=True,
                    keyrange_dist_a=14.18,
                    keyrange_dist_b=-2.917,
                    keyrange_dist_c=0.0164,
                    keyrange_dist_d=-0.08082,
                    keyrange_num=30,
                    value_k=0.2615,
                    value_sigma=25.45,
                    iter_k=2.517,
                    iter_sigma=14.236,
                    mix_get_ratio=0.85,
                    mix_put_ratio=0.14,
                    mix_seek_ratio=0.01,
                    sine_mix_rate_interval_milliseconds=5000,
                    sine_a=1000,
                    sine_b=0.00000073,
                    sine_d=4500000,
                    perf_level=1,
                    key_size=48,
                    duration=convert_to_sec(10, "m"),
                ),
            )

        if self == DBBenchTasks.ZIPPY_WORKLOAD:
            return DBBenchPlan(
                name="zippy_workload_15min",
                load_phase=DBBenchSettings(
                    benchmarks=DBBenchBenchmarksOptions(fillrandom=True),
                    num=1000000,
                    use_existing_db=False,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    key_size=48,
                    cache_size=268435456,
                    value_size=43,
                    statistics=False,
                ),
                run_phase=MixGraphDBBenchOptions(
                    benchmarks=DBBenchBenchmarksOptions(mixgraph=True, stats=True),
                    cache_size=268435456,
                    num=5000000,
                    reads=42000000,
                    statistics=True,
                    use_direct_io_for_flush_and_compaction=True,
                    use_direct_reads=True,
                    use_existing_db=True,
                    keyrange_dist_a=14.18,
                    keyrange_dist_b=-2.917,
                    keyrange_dist_c=0.0164,
                    keyrange_dist_d=-0.08082,
                    keyrange_num=30,
                    value_k=0.2615,
                    value_sigma=25.45,
                    iter_k=2.517,
                    iter_sigma=14.236,
                    mix_get_ratio=0.85,
                    mix_put_ratio=0.14,
                    mix_seek_ratio=0.01,
                    sine_mix_rate_interval_milliseconds=5000,
                    sine_a=100000,
                    sine_b=0.00000073,
                    sine_d=450000,
                    perf_level=1,
                    key_size=48,
                    duration=convert_to_sec(15, "m"),
                ),
            )


"""
RocksDB InMemory workload performance benchmark_container
https://github.com/facebook/rocksdb/wiki/RocksDB-In-Memory-Workload-Performance-Benchmarks

The goal of these benchmarks is to measure the performance of RocksDB when the data 
resides in RAM. The system is configured to store transaction logs on persistent 
storage so that data is not lost on machine reboots. Database is initially loaded with 
500M unique keys by using db_bench's filluniquerandom mode, 
then read performance is measured for a 7200-second run in readwhilewriting mode 
with 32 reader threads.  Each reader thread issues random k request, 
which is guaranteed to be found. 
Another dedicated writer thread issues write requests in the meantime.

"""
IN_MEMORY_WORKLOADS = {
    # POINT LOOKUP QUERIES ##########################
    # 10k
    "point_lookup_10k_write": DBBenchPlan(
        name="point_lookup_10k_write",
        load_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(filluniquerandom=True),
            num=524288000,
            use_existing_db=False,
            cache_size=17179869184,
            threads=1,
            prefix_size=20,
            key_size=20,
            keys_per_prefix=0,
            statistics=False,
        ),
        run_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(readwhilewriting=True),
            num=524288000,
            threads=32,
            use_existing_db=True,
            cache_size=17179869184,
            prefix_size=20,
            key_size=20,
            keys_per_prefix=0,
            duration=7200,
        ),
    ),
    "baseline_point_lookup_10k_write": DBBenchPlan(
        name="point_lookup_10k_write",
        load_phase=read_benchmark("point_lookup_10k_load.txt"),
        run_phase=read_benchmark("point_lookup_10k_run.txt"),
    ),
    # 80k
    "point_lookup_80k_write": DBBenchPlan(
        name="point_lookup_80k_write",
        load_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(filluniquerandom=True),
            num=524288000,
            use_existing_db=False,
            threads=1,
            cache_size=17179869184,
            prefix_size=20,
            key_size=20,
            keys_per_prefix=0,
            statistics=False,
        ),
        run_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(readwhilewriting=True),
            num=524288000,
            threads=32,
            use_existing_db=True,
            cache_size=17179869184,
            prefix_size=20,
            key_size=20,
            keys_per_prefix=0,
            duration=7200,
        ),
    ),
    "baseline_point_lookup_80k_write": DBBenchPlan(
        name="point_lookup_80k_write",
        load_phase=read_benchmark("point_lookup_80k_load.txt"),
        run_phase=read_benchmark("point_lookup_80k_run.txt"),
    ),
    # PREFIX RANGE QUERIES ##########################
    # 10k
    "prefix_range_query_10k_write": DBBenchPlan(
        name="prefix_range_query_10k_write",
        load_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(filluniquerandom=True),
            num=524288000,
            use_existing_db=False,
            prefix_size=12,
            key_size=20,
            keys_per_prefix=10,
            cache_size=17179869184,
            statistics=False,
        ),
        run_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(readwhilewriting=True),
            num=524288000,
            threads=32,
            use_existing_db=True,
            duration=7200,
            prefix_size=12,
            key_size=20,
            keys_per_prefix=10,
            cache_size=17179869184,
        ),
    ),
    "baseline_prefix_range_query_10k_write": DBBenchPlan(
        name="prefix_range_query_10k_write",
        load_phase=read_benchmark("prefix_range_query_10k_load.txt"),
        run_phase=read_benchmark("prefix_range_query_10k_run.txt"),
    ),
    # 80k
    "prefix_range_query_80k_write": DBBenchPlan(
        name="prefix_range_query_80k_write",
        load_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(filluniquerandom=True),
            num=524288000,
            use_existing_db=False,
            prefix_size=12,
            key_size=20,
            keys_per_prefix=10,
            cache_size=17179869184,
            statistics=False,
        ),
        run_phase=DBBenchSettings(
            benchmarks=DBBenchBenchmarksOptions(readwhilewriting=True),
            num=524288000,
            threads=32,
            use_existing_db=True,
            duration=7200,
            prefix_size=12,
            key_size=20,
            keys_per_prefix=10,
            cache_size=17179869184,
        ),
    ),
    "baseline_prefix_range_query_80k_write": DBBenchPlan(
        name="prefix_range_query_80k_write",
        load_phase=read_benchmark("prefix_range_query_80k_load.txt"),
        run_phase=read_benchmark("prefix_range_query_80k_run.txt"),
    ),
}
