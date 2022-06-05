# SysGym
A suite of real-world systems and interface to compare iterative optimization algorithms.


## Installation

SysGym relies on using [Docker](https://docs.docker.com/) to simplify executing a wide variety of real-world environments and benchmarks. Follow the [official Docker's documentation](https://docs.docker.com/get-docker/) to install it.

Once docker is installed you can either run `python setup.py all` to install all environments and their dependencies, or `pip install[name_of_env]` for example `pip install [postgres]` to install 

Once installed, you will need to configure the docker instance, e.g., pulling the right image and setup the dev workspace, we provide convienent scripts for  you to run. For example to prepare gem5-Aladdin you would run [`sh scripts/gem5_dockersetup/aladdin_setup.sh`](scripts/gem5_dockersetup/aladdin_setup.sh).
Other scripts available in the [`scripts`](scripts) directory

## Quick start

### Run a single optimization loop of a given environment 

```Python

#TODO: API demo showing a single iterative loop 

```

### Run several benchmark against a specific environment 
```Python
#TODO: show the environment runner script
```


## Supported libraries

You can use this interface and these following extensions to run optimizations using these following methods:

### Single-Objective Optimization
For optimizing a single objective (e.g. latency only, throughput only, etc...) 

* [BoTorch](https://github.com/pytorch/botorch/), [Turbo](https://proceedings.neurips.cc/paper/2019/file/6c990b7aca7bc7058f5e98ea909e924b-Paper.pdf), or [DeepGP-BO](http://proceedings.mlr.press/v31/damianou13a.pdf):  Use the [SysmGym-BoTorch](https://github.com/samialabed/sysgym-botorch) extension.
* [NNI suite](https://github.com/microsoft/nni): Use the [SysmGym-NNI](https://github.com/samialabed/sysgym-nni) extension.
 


### Multi-Objective Optimization


You can optimize multiple objectives using only the following: 
* [BoGraph](https://github.com/samialabed/bograph) (supports sysgym out othe box) 
* [BoTorch-sysgym](https://github.com/samialabed/sysgym-botorch)


## Supported environments



- [x] gem5-Aladdin: [System Documentation](https://github.com/harvard-acc/gem5-aladdin), SysGYM documentation

- [ ] PostgresSQL

- [ ] RocksDB

- [ ] Apache Flink


Feel free to contribute your own environment, please check [CONTRIBUTION](CONTRIBUTION.md) as well as [Instruction on adding new environment](sysgym/envs/instruction.md).


## Towards V1 release
As we are still in v0.1 expect the API to change overtime as we simplify the process of using it, the primary goal of V1 release are:
- [ ]Simplify the process of importing the desirable API: which means creating hooks to perform the installation at import time rather than requiring the user to manually run scripts.
- [ ] improving the space abstraction to allow incorporating hierarchical dependencies between the parameters. 

## Citation





