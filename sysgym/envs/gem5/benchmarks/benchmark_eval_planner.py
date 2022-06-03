from string import Template
from typing import List

from sysgym.envs.gem5.benchmarks.benchmark_settings import Gem5BenchmarkConfig
from sysgym.param_dict import EnvParamsDict


def from_env_params_to_sys(env_params: EnvParamsDict) -> List[str]:
    # TODO: workaround dependency until we do a refactor for hierarchcail parameter
    opts = []

    for (param_name, val) in env_params.items():
        if param_name == "cache_size":
            # Cache_size has to be x * cache_line_sz * cache_assoc
            val = val * env_params["cache_line_sz"] * env_params["cache_assoc"]
        elif param_name == "tlb_entries":
            # Note: tlb_entries has to be tlb_entries * tlb_assoc
            val = val * env_params["tlb_assoc"]

        opts.append(f"set {param_name} {val}")
    return opts


def generate_benchmark_eval_template(
    bench_cfg: Gem5BenchmarkConfig, output_dir: str, evaluation_configs: EnvParamsDict
) -> str:
    """Return a benchmark_container config file written in xe format to run in
    gem5."""

    # Prepare the generation commands:
    #   generate GenerationCommand, each on its own line
    generation_commands = "\n".join(
        map(lambda x: f"generate {x}", bench_cfg.generation_commands)
    )

    # Add for each line a "set <parameter> <value"
    evaluation_configs = from_env_params_to_sys(evaluation_configs)
    # ensure every configuration on its own line
    evaluation_configs = "\n".join(evaluation_configs)

    with open(bench_cfg.resource_path / "benchmark_template.xe") as bench_template_f:
        benchmark_template = Template(bench_template_f.read())

    benchmark_template_filled = benchmark_template.substitute(
        {
            "output_dir": str(output_dir),
            "source_dir": bench_cfg.source_dir,
            "simulator": str(bench_cfg.simulator),
            "memory_type": str(bench_cfg.memory_type),
            "generation_commands": generation_commands,
            "bench_suite": str(bench_cfg.bench_suite),
            "task": str(bench_cfg.task),
            "evaluation_configs": evaluation_configs,
            "task_constants": bench_cfg.task_constants,
        }
    )
    return benchmark_template_filled
