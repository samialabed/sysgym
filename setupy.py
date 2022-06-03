import os
import sys

from setuptools import find_packages, setup

REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7

# Check for python version
if sys.version_info < (REQUIRED_MAJOR, REQUIRED_MINOR):
    error = (
        "Your version of python ({major}.{minor}) is too old. You need "
        "python >= {required_major}.{required_minor}."
    ).format(
        major=sys.version_info.major,
        minor=sys.version_info.minor,
        required_minor=REQUIRED_MINOR,
        required_major=REQUIRED_MAJOR,
    )
    sys.exit(error)

# Requirements
TEST_REQUIRES = []
FMT_REQUIRES = []

# Read in the pinned versions of the formatting tools
root_dir = os.path.dirname(__file__)
with open(os.path.join(root_dir, "fmt_requirements.txt"), "r") as fh:
    FMT_REQUIRES += [
        line.strip() for line in fh.readlines() if not line.startswith("#")
    ]
with open(os.path.join(root_dir, "test_requirements.txt"), "r") as fh:
    TEST_REQUIRES += [
        line.strip() for line in fh.readlines() if not line.startswith("#")
    ]

DEV_REQUIRES = TEST_REQUIRES + FMT_REQUIRES

# read in README.md as the long description
with open(os.path.join(root_dir, "README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name="sysgym",
    description="SysGym toolkit to simplify evaluating different configurations on  "
    "real-world systems",
    author="Sami Alabed",
    license="MIT",
    url="https://github.com/samialabed/sysgym/",
    project_urls={
        "Documentation": "https://github.com/samialabed/sysgym/",
        "Source": "https://github.com/samialabed/sysgym/",
    },
    keywords=["Computer system optimization", "gym"],
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
    setup_requires=["setuptools-scm"],
    packages=find_packages(exclude=["test", "test.*"]),
    install_requires=[
        "scipy",
        "numpy",
        "docker",
    ],
    extras_require={
        "dev": DEV_REQUIRES,
        "test": TEST_REQUIRES,
    },
)
