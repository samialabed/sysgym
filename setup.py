import os
import sys
from pathlib import Path
from typing import List, Union

from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(__file__)
REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7

# Check for python version
if sys.version_info < (REQUIRED_MAJOR, REQUIRED_MINOR):
    error = (
        f"Your version of python ({sys.version_info.major}.{sys.version_info.minor})"
        f" is too old. You need python >= {REQUIRED_MAJOR}.{REQUIRED_MINOR}. "
    )
    sys.exit(error)


def _parse_requirements(path: Union[Path, str]) -> List[str]:
    requirements = []
    with open(os.path.join(ROOT_DIR, path), "r") as fh:
        requirements += [
            line.strip() for line in fh.readlines() if not line.startswith("#")
        ]
    return requirements


def _setup():
    core_requires = _parse_requirements("dependencies/requirements.txt")
    fmt_requires = _parse_requirements("dependencies/fmt_requirements.txt")
    test_build_requires = _parse_requirements("dependencies/dev_requirements.txt")
    postgres_requires = _parse_requirements("dependencies/postgres_requirements.txt")
    gem5_requires = _parse_requirements("dependencies/gem5_requirements.txt")
    dev_requires = test_build_requires + fmt_requires

    # read in README.md as the long description
    with open(os.path.join(ROOT_DIR, "README.md"), "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(
        name="sysgym",
        description="SysGym a toolkit to evaluate different optimizers on  "
        "real-world systems",
        author="Sami Alabed",
        license="MIT",
        url="https://github.com/samialabed/sysgym/",
        project_urls={
            "Documentation": "https://github.com/samialabed/sysgym/",
            "Source": "https://github.com/samialabed/sysgym/",
        },
        keywords=[
            "Computer system optimization",
            "gym",
            "Bayesian optimization environments",
        ],
        classifiers=[
            "Development Status :: 0 - Alpha",
            "Programming Language :: Python :: 3 :: Only",
            "License :: OSI Approved :: MIT License",
            "Topic :: Scientific/Engineering",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        python_requires=">=3.7",
        packages=find_packages(exclude=["test", "test.*", "examples", "scripts"]),
        install_requires=core_requires,
        extras_require={
            "dev": dev_requires + postgres_requires + gem5_requires,
            "postgres": postgres_requires,
            "gem5": gem5_requires,
            "all": postgres_requires + gem5_requires,
        },
    )


if __name__ == "__main__":
    _setup()
