import logging
import time
from pathlib import Path

from psutil import Process

from sysgym import Environment, EnvParamsDict
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench import DBBench
from sysgym.envs.rocksdb.env_cfg import RocksDBEnvConfig
from sysgym.envs.rocksdb.env_measure import RocksDBMeasurements
from sysgym.envs.rocksdb.parsers.parser_factory import parse_res_file
from sysgym.envs.rocksdb.stats.sysio_dao import SystemIO

LOG = logging.getLogger("sysgym")


class RocksDBEnv(Environment):
    def __init__(self, env_cfg: RocksDBEnvConfig, artifacts_output_dir: Path):
        super().__init__(env_cfg=env_cfg, artifacts_output_dir=artifacts_output_dir)
        # TODO: handle different benchmarks
        benchmark = DBBench(artifacts_output_dir, env_cfg.bench_cfg)
        self.benchmark = benchmark

    def run(self, params: EnvParamsDict) -> RocksDBMeasurements:
        benchmark_process = self.benchmark.execute(params=params)
        system_io = capture_process_io(benchmark_process)
        parsed_stats = parse_res_file(self.benchmark.run_phase_results)
        LOG.debug("%s finished in %s", self.benchmark.name, system_io.exe_time)
        slo = RocksDBMeasurements(sysio=system_io, bench_stats=parsed_stats)

        return slo


def capture_process_io(benchmark_process: Process, monitoring_interval=10) -> SystemIO:
    """Monitor a process and capture its memory, cpu, and execution time."""
    experiment_start = time.time()
    mem_usages = []
    cpu_usages = []
    # while the process is running calculate resource utilization.
    while benchmark_process.is_running():
        time.sleep(monitoring_interval)
        # capture the memory and cpu_usage utilization at an instance
        mem = benchmark_process.memory_info().rss / float(2**30)
        cpu = benchmark_process.cpu_percent()
        if mem == 0:
            break
        mem_usages.append(mem)
        cpu_usages.append(cpu)
    benchmark_process.wait()
    duration = time.time() - experiment_start

    return SystemIO(cpu_usage=cpu_usages, mem_usage=mem_usages, exe_time=duration)
