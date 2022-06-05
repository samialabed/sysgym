import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from dataclasses_json import dataclass_json

from sysgym.envs.gem5.benchmarks.benchmark_tasks import BenchmarkTask
from sysgym.utils.enum import ListableEnum

LOG = logging.getLogger("sysgym")


class Simulators(ListableEnum):
    # gem5-cpu: Run Aladdin with a gem5 CPU.
    CPU = "gem5-cpu"
    # aladdin: Run Aladdin only.
    ALADDIN = "aladdin"


class MemoryType(ListableEnum):
    CACHE = "cache"


class BenchmarkSuite(ListableEnum):
    # CORTEXSUITE = "cortexsuite"
    MACHSUITE = "machsuite"
    SHOC = "shoc"


BENCHMARK_SUITE_BINARY_PATH = {
    BenchmarkSuite.MACHSUITE: "src/aladdin/MachSuite",
    BenchmarkSuite.SHOC: "src/aladdin/shoc",
}


class GenerationCommand(ListableEnum):
    # configs: All design sweep configurations and required files.
    CONFIGS = "configs"
    # trace: The dynamic traces required for each benchmark_container. Since all
    # configurations of a design sweep for a benchmark_container use the same trace,
    # and traces can take much longer to generate than design sweep configurations,
    # this component is specified separate.
    TRACE = "trace"
    # dma_trace: Same as above, but DMA load and store function calls are included.
    DMA_TRACE = "dma_trace"
    # Use the DMA version when you expect data for arrays to be supplied through DMA,
    # and use the non-DMA version if you are using caches
    # or running Aladdin in standalone.
    GEM5_BINARY = "gem5_binary"


@dataclass_json
@dataclass
class Gem5BenchmarkConfig:
    # Path to the source directory of the benchmark_container suite being swept.
    # Make sure the source directory isn't a relative path, it breaks so many things
    source_dir: str
    simulator: Simulators
    memory_type: MemoryType
    bench_suite: BenchmarkSuite
    task: BenchmarkTask
    generation_commands: List[GenerationCommand] = field(
        default_factory=lambda: [
            GenerationCommand.CONFIGS,
            GenerationCommand.TRACE,
            GenerationCommand.GEM5_BINARY,
        ]
    )
    resource_path_override: Optional[str] = None
    # Take override for task constants or read the one defined in the resource directory
    task_constants: Optional[str] = ""
    # Optional override of timeout, if provided, override the default timeout
    timeout_override: Optional[int] = None

    def __post_init__(self):
        if self.resource_path_override:
            self.resource_path = Path(self.resource_path_override)
        else:
            self.resource_path = Path(__file__).parent / "resources"

        self.source_dir = (
            f"{self.source_dir}/{BENCHMARK_SUITE_BINARY_PATH[self.bench_suite]}"
        )

        # Read the constants for this task once if they are defined
        if not self.task_constants:
            path_to_constants = self.resource_path / f"{self.bench_suite}_constants.xe"
            if path_to_constants.is_file():
                LOG.info("Constants override detected, reading them.")
                with open(path_to_constants, encoding="utf-8") as constants_file:
                    constants_vals = constants_file.read()
                task_pattern = re.compile(rf"set \w* for \S*{self.task}\S* .*")
                self.task_constants = "\n".join(task_pattern.findall(constants_vals))
            else:
                LOG.info("No constant overrides")
