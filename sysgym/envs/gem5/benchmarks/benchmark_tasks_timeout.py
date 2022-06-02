from typing import Dict

from sysgym.envs.gem5.benchmarks.benchmark_tasks import MachSuiteTask
from sysgym.utils.enum import BenchmarkTask

# Map between the task and its maximum running time (sometime the task will freeze)

TASK_TO_TIMEOUT_SECONDS: Dict[BenchmarkTask, int] = {
    # The maximum is set to x5 the average execution time
    # For now it doesn't make sense to make this configurable
    # but can easily be overriden
    MachSuiteTask.AES: 60,
    MachSuiteTask.FFT_TRANSPOSE: 250,
    MachSuiteTask.MD_KNN: 250,
    MachSuiteTask.SPMV_CRS: 250,
    MachSuiteTask.SPMV_ELLPACK: 400,
    MachSuiteTask.FFT_STRIDED: 500,
    MachSuiteTask.STENCIL_2D: 910,
    MachSuiteTask.STENCIL_3D: 1500,
    MachSuiteTask.GEMMA_NCUBED: 2500,
}
