import logging
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Optional

import docker
from docker.errors import NotFound
from docker.models.containers import Container
from docker.types import Mount
from timeout_decorator import timeout

from sysgym.envs.gem5.benchmarks.benchmark_eval_planner import (
    generate_benchmark_eval_template,
)
from sysgym.envs.gem5.benchmarks.benchmark_settings import Gem5BenchmarkConfig
from sysgym.envs.gem5.benchmarks.benchmark_tasks_timeout import TASK_TO_TIMEOUT_SECONDS
from sysgym.envs.gem5.benchmarks.exception import DockerExecutionException

# Constant container settings
from sysgym.envs.gem5.env_measure import Gem5Metrics
from sysgym.envs.gem5.parsers import parse_statistics, parse_summary_file
from sysgym.params.param_dict import EnvParamsDict

WORKSPACE_ROOT_DIR = "/workspace"
PATH_TO_GEM_WORKSPACE = "/workspace/gem5-aladdin"
LOG = logging.getLogger("sysgym")


@dataclass
class Gem5ContainerSettings:
    gem_docker_volume: str
    container_name: str
    docker_img: str


class Gem5BenchmarkDocker:
    def __init__(
        self,
        bench_cfg: Gem5BenchmarkConfig,
        container_settings: Gem5ContainerSettings,
        output_dir: Path,
    ):
        self._container_settings = container_settings
        self._bench_cfg = bench_cfg
        self._output_dir = output_dir
        task_name = str(bench_cfg.task)
        # name of files to copy from the docker volume that contains benchmark info
        self.files_to_capture = [
            "stderr",
            "stdout",
            "stats.txt",
            f"{task_name}_cache_stats.txt",
            f"{task_name}_spad_stats.txt",
            f"{task_name}_summary",
        ]
        self._docker_cli = docker.from_env()
        if self._bench_cfg.timeout_override:
            task_timeout_secs = self._bench_cfg.timeout_override
        else:
            task_timeout_secs = TASK_TO_TIMEOUT_SECONDS.get(self._bench_cfg.task, None)
            if task_timeout_secs is None:
                LOG.warning(
                    "No specific timeout provided for task %s. Defaulting to 15 mins.",
                    self._bench_cfg.task,
                )
                # Default to 15 minute timeout if no task specific timeout provided
                task_timeout_secs = 15 * 60
        self._exec_benchmark = timeout(seconds=task_timeout_secs)(self._exec_benchmark)

        self._gem5_container: Optional[Container] = None
        self._compiled_sim_path = f"{WORKSPACE_ROOT_DIR}/compiled_simulation/"

    def initialize(self):
        self._gem5_container = self._get_gem5_container(
            self._container_settings.container_name
        )
        sleep(10)  # wait for the container to properly start

    def cleanup(self, container: Container):
        LOG.debug("Cleaning up container %s.", container.name)
        container.exec_run(
            workdir=WORKSPACE_ROOT_DIR, cmd=f"rm -r {self._compiled_sim_path}"
        )
        container.kill()
        sleep(10)  # wait for the container to properly close

    def execute(self, params: EnvParamsDict) -> Gem5Metrics:
        """Execute the benchmark_container in docker given set parameters"""
        assert (
            self._gem5_container
        ), "Expected the container to be initialized before executing the benchmark"

        try:
            # build the task directory structure
            status = self._gem5_container.exec_run(
                workdir=WORKSPACE_ROOT_DIR,
                cmd=f"mkdir -p {self._compiled_sim_path}",
            )
            if status.exit_code != 0:
                raise DockerExecutionException(
                    f"Docker exec failed with error: {status.output}"
                )

            # Create the benchmark_container execution template for gem5
            benchmark_eval_plan = generate_benchmark_eval_template(
                bench_cfg=self._bench_cfg,
                output_dir=self._compiled_sim_path,
                evaluation_configs=params,
            )

            # Copy the plan into docker
            benchmark_eval_filename = f"{str(self._bench_cfg.task)}_eval.xe"

            status = self._gem5_container.exec_run(
                workdir=self._compiled_sim_path,
                cmd=[
                    "bash",
                    "-c",
                    f"echo '{benchmark_eval_plan}' > {benchmark_eval_filename}",
                ],
            )
            if status.exit_code != 0:
                raise DockerExecutionException(
                    f"Docker exec failed with error: {status.output}"
                )

            # Generate the benchmark_container according to the execution plan
            workspace_dir = PATH_TO_GEM_WORKSPACE

            status = self._gem5_container.exec_run(
                workdir=f"{workspace_dir}/sweeps/benchmarks",
                cmd=[
                    f"{workspace_dir}/sweeps/generate_design_sweeps.py",
                    f"{self._compiled_sim_path}/{benchmark_eval_filename}",
                ],
            )
            if status.exit_code != 0:
                raise DockerExecutionException(
                    f"Docker exec failed with error: {status.output}"
                )

            # run the benchmark_container
            benchmark_dir_in_container = (
                f"{self._compiled_sim_path}/{self._bench_cfg.task}/0"
            )

            self._exec_benchmark(
                benchmark_dir_in_container=benchmark_dir_in_container,
                benchmark_eval_plan=benchmark_eval_plan,
            )
            self.grab_env_output(benchmark_dir_in_container=benchmark_dir_in_container)

            summary_stats = parse_summary_file(
                self._output_dir / f"{self._bench_cfg.task}_summary"
            )
            detailed_stats = parse_statistics(self._output_dir / "stats.txt")

            return Gem5Metrics(
                summary_stats=summary_stats, detailed_stats=detailed_stats
            )
        except TimeoutError as te:
            LOG.error("Executing the benchmark failed. %s", te)
        except Exception as e:
            LOG.error("Docker execution failed: %s", e)
            raise e

    def _exec_benchmark(
        self, benchmark_dir_in_container: str, benchmark_eval_plan: str
    ):
        status = self._gem5_container.exec_run(
            workdir=benchmark_dir_in_container,
            cmd=["bash", "run.sh"],
        )
        if status.exit_code != 0:
            # Capture the stderr from the docker instance
            # download it into the experiment manager directory
            file_content = self._gem5_container.exec_run(
                workdir=benchmark_dir_in_container,
                cmd=["bash", "-c", "cat outputs/stderr"],
            )
            with open(self._output_dir / "stderr", "wb") as outf:
                outf.write(file_content.output)
            with open(self._output_dir / "execution_plan", "w") as outf:
                outf.writelines(benchmark_eval_plan)
            raise DockerExecutionException(
                f"Docker exec failed with error: {status.output}"
            )

    def grab_env_output(self, benchmark_dir_in_container: str) -> None:
        # capture the statistics files from the container
        for file_name in self.files_to_capture:
            file_content = self._gem5_container.exec_run(
                workdir=benchmark_dir_in_container,
                cmd=["bash", "-c", f"cat outputs/{file_name}"],
            )
            if file_content.exit_code != 0:
                raise DockerExecutionException(
                    f"Docker exec failed with error: {file_content.output}"
                )

            # download it into the experiment manager directory
            with open(self._output_dir / file_name, "wb") as outf:
                outf.write(file_content.output)

    def _get_gem5_container(
        self, container_name: str, reuse: bool = False
    ) -> Container:
        """
        Check if the benchmark_container is running, if not attach_container it.

        Args:
            reuse (bool): Specify whether to reuse an existing
            running container or kill an existing container if it exists

        """
        try:
            container = self._docker_cli.containers.get(container_name)
            LOG.debug(
                "Found a container running already with the name %s", container_name
            )
            if reuse:
                LOG.debug("Reusing container.")
                return container
            else:
                # perform cleanup and initialize again
                self.cleanup(container)
        except NotFound:
            container = self._create_container_w_persistent_volume(container_name)
            return container
        raise Exception("Failed to create gem5 container")

    def _create_container_w_persistent_volume(self, container_name: str) -> Container:
        LOG.debug("Creating container %s.", container_name)
        persistent_volume = Mount(
            source=self._container_settings.gem_docker_volume,
            target=WORKSPACE_ROOT_DIR,
        )

        # Check if we need to create the volume and compile all libraries
        if not self._is_volume_created():
            install_script_loc = "/scripts/gem5_dockersetup/aladdin_setup.sh"
            raise SystemError(
                f"No gem5 docker volume detected. Run {install_script_loc}"
            )

        # Create a container
        container: Container = self._docker_cli.containers.run(
            image=self._container_settings.docker_img,
            name=container_name,
            detach=True,
            mounts=[persistent_volume],
            tty=True,
            remove=True,
            platform="linux/amd64",
        )
        if container.status == "exited":
            raise DockerExecutionException(
                f"Creating container ({container.name}) failed: {container.status}."
            )
        return container

    def _is_volume_created(self) -> bool:
        """Check if docker volume created or not, to persist changes and avoid
        rebuilding gem5"""
        volume_name = self._container_settings.gem_docker_volume
        try:
            self._docker_cli.volumes.get(volume_name)
            return True
        except NotFound as e:
            LOG.debug("%s volume not found. API NotFound trace: %s.", volume_name, e)
            return False

    def __enter__(self):
        self.initialize()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup(self._gem5_container)
