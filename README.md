# SysGym
A suite of real-world systems and interface to compare iterative optimization algorithms.





## Supported environments



- [x] gem5-Aladdin: [System Documentation](https://github.com/harvard-acc/gem5-aladdin), SysGYM documentation

- [ ] PostgresSQL

- [ ] RocksDB

- [ ] Apache Flink



Feel free to contribute your own environment, please check `CONTRIBUTION` as well as (TODO: Provide link to documenting how to add new environment)



## Quick start

### Run a single optimization loop of a given environment 

```Python

TODO: API demo showing a single iterative loop 

```

### Run several benchmark against a specific environment 
```Python
TODO: show the environment runner script
```


## Supported libraries

You can use this interface and these following extensions to run optimizations using these following methods:

### Single-Objective Optimization
For optimizing a single objective (e.g. latency only, throughput only, etc...) 

* [BoTorch](https://github.com/pytorch/botorch/), [Turbo](https://proceedings.neurips.cc/paper/2019/file/6c990b7aca7bc7058f5e98ea909e924b-Paper.pdf), [DeepGP-BO](http://proceedings.mlr.press/v31/damianou13a.pdf):  Use the SysmGym-BoTorch [BoTorch-sysgym](https://github.com/samialabed/sysgym-botorch)
* DeepGP: Extension (TODO: link to our library that provide NNI link)
* [NNI suite](https://github.com/microsoft/nni): Use the SysmGym-NNI [Extension](https://github.com/samialabed/sysgym-nni)



### Multi-Objective Optimization


You can optimize multiple objectives using only the following: 
* [BoGraph](https://github.com/samialabed/bograph) (supports sysgym out othe box) 
* [BoTorch-sysgym](https://github.com/samialabed/sysgym-botorch)

## Setup 

Each environment has its own setup requirement, you can either install environment using script `install_all.sh` or a specific environment as found in the scripts directory.

## Citation





