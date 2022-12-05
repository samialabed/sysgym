import logging
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

import psutil
from psutil import Process

from sysgym import EnvParamsDict
from sysgym.env_abc import BenchmarkConfig
from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench_settings import DBBenchSettings
from sysgym.envs.rocksdb.env_measure import RocksDBMeasurements
from sysgym.envs.rocksdb.parsers.parser_factory import parse_res_file
from sysgym.envs.rocksdb.stats.sysio_dao import SystemIO

LOG = logging.getLogger("sysgym")


def capture_process_io(benchmark_process: Process, monitoring_interval=10) -> SystemIO:
    """Monitor a process and capture its memory, cpu, and execution time."""
    experiment_start = time.time()
    mem_usages = []
    cpu_usages = []
    # while the process is running calculate resource utilization.
    while benchmark_process.is_running():
        # capture the memory and cpu_usage utilization at an instance
        mem = benchmark_process.memory_info().rss / float(2**30)
        cpu = benchmark_process.cpu_percent()
        if mem == 0:
            break
        mem_usages.append(mem)
        cpu_usages.append(cpu)
        time.sleep(monitoring_interval)
    benchmark_process.wait()
    duration = time.time() - experiment_start

    return SystemIO(cpu_usage=cpu_usages, mem_usage=mem_usages, exe_time=duration)


@dataclass
class DBBenchPlan:
    name: str
    load_phase: Optional[Union[str, DBBenchSettings]]
    run_phase: Union[str, DBBenchSettings]
    # TODO: add repeat_execution: int


class DBBench(BenchmarkConfig):
    CLEAR_LOCKS_WAIT_SEC = 10

    def __init__(
        self,
        artifacts_output_dir: Path,
        bench_plan: DBBenchPlan,
        clean_after: bool = True,
    ):
        self._cmd = "db_bench"
        self._bench_plan = bench_plan
        self._artifacts_output_dir = artifacts_output_dir
        self._name = f"dbbench_{bench_plan.name}"
        # Clean the database afterward, for update/read workload this isn't needed
        # But it is useful for any workload that inserts item in the db.
        self._clean_after = clean_after

    @staticmethod
    def env_params_dict_to_sys(params: EnvParamsDict) -> List[str]:
        return [f"--{k}={v}" for k, v in params.items()]

    @property
    def run_phase_results(self) -> Path:
        return self._artifacts_output_dir / f"{self.name}_run_results.logs"

    @property
    def run_phase_errs(self) -> Path:
        return self._artifacts_output_dir / f"{self.name}_run_err.logs"

    @property
    def load_phase_results(self) -> Path:
        return self._artifacts_output_dir / f"{self.name}_load_results.logs"

    @property
    def load_phase_errs(self) -> Path:
        return self._artifacts_output_dir / f"{self.name}_load_err.logs"

    def cleanup(self):
        """Remove any produced artifacts."""
        if self._clean_after:
            if self._bench_plan.load_phase:
                if os.path.exists(self._bench_plan.load_phase.db):
                    shutil.rmtree(self._bench_plan.load_phase.db)
                if os.path.exists(self._bench_plan.load_phase.wal_dir):
                    shutil.rmtree(self._bench_plan.load_phase.wal_dir)

    def execute(self, params: EnvParamsDict) -> RocksDBMeasurements:
        try:
            if self._bench_plan.load_phase:
                # Load phase is always standard, prepare the cache of the system
                self._load_phase()
            run_process = self._run_phase(params)
            system_io = capture_process_io(run_process)
            parsed_stats = parse_res_file(self.run_phase_results)
            LOG.debug("%s finished in %s", self._bench_plan.name, system_io.exe_time)
            return RocksDBMeasurements(sysio=system_io, bench_stats=parsed_stats)
        finally:
            self.cleanup()

    def _load_phase(self):
        LOG.info("Executing the the load_phase.")
        start_time = time.time()
        load_phase = self._bench_plan.load_phase
        if isinstance(load_phase, DBBenchSettings):
            load_phase = load_phase.as_cmd()

        LOG.debug("Load_phase cmd: %s.", load_phase)
        with open(self.load_phase_results, "wb") as out, open(
            self.load_phase_errs, "wb"
        ) as err:
            with subprocess.Popen(
                [self._cmd] + load_phase, stdout=out, stderr=err
            ) as p:
                p.communicate()  # finish loading

        finish_time = time.time() - start_time
        LOG.info("Populating the database took: %s seconds.", finish_time)
        time.sleep(self.CLEAR_LOCKS_WAIT_SEC)  # give sometime to clear db_bench locks

    def _run_phase(self, params: EnvParamsDict):
        LOG.info("Executing the run_phase.")
        rocksdb_params_options = self.env_params_dict_to_sys(params)
        run_phase = self._bench_plan.run_phase
        if isinstance(run_phase, DBBenchSettings):
            run_phase = run_phase.as_cmd()
        run_args = run_phase + rocksdb_params_options
        LOG.debug("run_args cmd: %s.", run_args)

        with open(self.run_phase_results, "wb") as out, open(
            self.run_phase_errs, "wb"
        ) as err:
            process = psutil.Popen([self._cmd] + run_args, stdout=out, stderr=err)
        return process

    @property
    def name(self) -> str:
        return self._name
