import logging
from typing import Dict, Optional

from sysgym.envs.gem5.benchmarks.benchmark_tasks import MachSuiteTask
from sysgym.utils.enum import BenchmarkTask

# Map between the task and its maximum running time (sometime the task will freeze)
LOG = logging.getLogger("sysgym")

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


def gem5_task_timeout(task: BenchmarkTask, timeout_override: Optional[int]):
    """Each task has unique timeout, or can be overriden"""
    if timeout_override:
        task_timeout_secs = timeout_override
    else:
        task_timeout_secs = TASK_TO_TIMEOUT_SECONDS.get(task, None)
        if task_timeout_secs is None:
            LOG.warning(
                "No specific timeout provided for task %s. Defaulting to 15 mins.",
                task,
            )
            # Default to 15 minute timeout if no task specific timeout provided
            task_timeout_secs = 15 * 60
    return task_timeout_secs
