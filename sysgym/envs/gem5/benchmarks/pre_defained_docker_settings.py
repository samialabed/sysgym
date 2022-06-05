from sysgym.envs.gem5.benchmarks.benchmark_docker import Gem5ContainerSettings


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
