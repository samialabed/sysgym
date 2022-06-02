import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import List, Optional

from dataclasses_json import dataclass_json

from sysgym.envs.bench_cfg import BenchmarkConfig
from sysgym.envs.gem5.benchmarks.benchmark_tasks import BenchmarkTask
from sysgym.envs.gem5.params_dict import Gem5ParamsDict
from sysgym.logging_util import ENV_RUNNER_LOGGER
from sysgym.utils.enum import ExtendedEnum

LOG = logging.getLogger(ENV_RUNNER_LOGGER)


def aladdin_docker_settings() -> Gem5ContainerSettings:
    return Gem5ContainerSettings(
        gem_docker_volume="gem5-aladdin-workspace",
        container_name="gem5aladdin",
        docker_img="xyzsam/gem5-aladdin",
    )


def smaug_docker_settings() -> Gem5ContainerSettings:
    return Gem5ContainerSettings(
        gem_docker_volume="smaug-workspace",
        container_name="gem5aladdin",
        docker_img="xyzsam/smaug",
    )


class Simulators(ExtendedEnum):
    # gem5-cpu: Run Aladdin with a gem5 CPU.
    CPU = "gem5-cpu"
    # aladdin: Run Aladdin only.
    ALADDIN = "aladdin"


class MemoryType(ExtendedEnum):
    CACHE = "cache"


class BenchmarkSuite(ExtendedEnum):
    # CORTEXSUITE = "cortexsuite"
    MACHSUITE = "machsuite"
    SHOC = "shoc"


BENCHMARK_SUITE_BINARY_PATH = {
    BenchmarkSuite.MACHSUITE: "src/aladdin/MachSuite",
    BenchmarkSuite.SHOC: "src/aladdin/shoc",
}


class GenerationCommand(ExtendedEnum):
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
class Gem5BenchmarkConfig(BenchmarkConfig):
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
                with open(path_to_constants) as constants_file:
                    # TODO(post paper): Add tests for the regex
                    constants_vals = constants_file.read()
                task_pattern = re.compile(f"set \w* for \S*{self.task}\S* .*")
                self.task_constants = "\n".join(task_pattern.findall(constants_vals))
            else:
                LOG.info("No constant overrides")

    def generate_benchmark_eval_template(
        self, output_dir: str, evaluation_configs: Gem5ParamsDict
    ) -> str:
        """Return a benchmark_container config file written in xe format to run in
        gem5."""

        # Prepare the generation commands:
        #   generate GenerationCommand, each on its own line
        generation_commands = "\n".join(
            map(lambda x: f"generate {x}", self.generation_commands)
        )

        # Add for each line a "set <parameter> <value"
        evaluation_configs = evaluation_configs.as_sys()
        # ensure every configuration on its own line
        evaluation_configs = "\n".join(evaluation_configs)

        with open(self.resource_path / "benchmark_template.xe") as bench_template_f:
            benchmark_template = Template(bench_template_f.read())

        benchmark_template_filled = benchmark_template.substitute(
            {
                "output_dir": str(output_dir),
                "source_dir": self.source_dir,
                "simulator": str(self.simulator),
                "memory_type": str(self.memory_type),
                "generation_commands": generation_commands,
                "bench_suite": str(self.bench_suite),
                "task": str(self.task),
                "evaluation_configs": evaluation_configs,
                "task_constants": self.task_constants,
            }
        )
        return benchmark_template_filled
