# SysGym gem5-Aladdin interface

## gem5-Aladdin

TODO: introduction about gem5-Aladdin


## Installation

Read the [README](https://github.com/samialabed/sysgym/scripts/gem5_dockersetup/README.md)

## Parameter space

TODO: explain the parameter space 

## Parameter dictionary


## Caveats
Some parameters depend on each other. 
The relationship is hardcoded in `benchmark_eval_planner.py`:

* Cache_size has to be x * cache_line_sz * cache_assoc
* tlb_entries has to be tlb_entries * tlb_assoc
