from dataclasses import dataclass

import sysgym.utils.converters as conv
from sysgym.envs.gem5.schema.utils import power_of_two
from sysgym.spaces import DiscreteSpace

# TODO: move this as an example
@dataclass(init=False, frozen=True)
class Gem5ParametersCollection20(Gem5ParamSchema):
    """
    Notes:
        - Aladdin only accepts integer parameters,
         so continuous and booleans are instead mapped to discrete values
        - Default values taken from:
        https://github.com/harvard-acc/gem5-aladdin/blob/master/configs/aladdin/aladdin_template.cfgs
        - parameters upper and lower bounds;
        https://github.com/harvard-acc/ALADDIN/blob/master/common/power_func.cpp#L8
        - Parameters that should be power of 2 and not 0:
         l2cache_size, tlb_assoc, tlb_entries, cache_line_sz, cache_assoc, cache_size
         Source:
         https://github.com/harvard-acc/gem5-aladdin/blob/a573865e82a172734d20441dc272259ed4911ced/src/mem/cache/tags/indexing_policies/base.cc#L64
    List of all Aladdin Parameters:
    https://github.com/harvard-acc/gem5-aladdin/blob/master/sweeps/benchmarks/params.py
    """

    #  ##################### Core Aladdin parameters.  #####################
    cycle_time: DiscreteSpace = DiscreteSpace(
        name="cycle_time",
        lower_bound=1,
        upper_bound=10,
        default=1,
        # Doesn't allow cycle time of 7, 8, 9 (not sure why but in their docs)
        formula=lambda x: x if x <= 6 or x == 10 else 6,
    )
    #  ##################### Aladdin specific parameters  #####################
    # pipelining: TODO
    pipelining: DiscreteSpace = DiscreteSpace(
        name="pipelining", lower_bound=0, upper_bound=1, default=0
    )

    #  ##################### Cache memory system parameters. #####################
    cache_size: DiscreteSpace = DiscreteSpace(
        # Space: [16kb, 128kb], only allows power of 2
        name="cache_size",
        formula=power_of_two,
        lower_bound=conv.short_size_to_base2("16kb"),
        upper_bound=conv.short_size_to_base2("128kb"),  # (kb = 2^10, 128 = 2 ^7)
        default=conv.short_size_to_base2("16kb"),
    )

    cache_assoc: DiscreteSpace = DiscreteSpace(
        # bounds: [1, 32], use power of two transformation [2^0, 2^5]
        # Note: cache_size has to be x * cache_line_sz * cache_assoc
        name="cache_assoc",
        lower_bound=0,
        upper_bound=5,
        default=2,
        formula=power_of_two,
    )
    cache_line_sz: DiscreteSpace = DiscreteSpace(
        # Bounds: [16, 32, 64, 128]
        name="cache_line_sz",
        lower_bound=5,
        upper_bound=7,
        default=5,
        formula=power_of_two,
    )
    cache_hit_latency: DiscreteSpace = DiscreteSpace(
        name="cache_hit_latency", lower_bound=1, upper_bound=5, default=1
    )
    cache_queue_size: DiscreteSpace = DiscreteSpace(
        name="cache_queue_size", lower_bound=2**4, upper_bound=2**8, default=32
    )
    # cache_bandwidth: Maxium number of cache requests can be issued in one cycle
    cache_bandwidth: DiscreteSpace = DiscreteSpace(
        name="cache_bandwidth", lower_bound=2, upper_bound=18, default=4
    )
    # TLB parameters
    tlb_hit_latency: DiscreteSpace = DiscreteSpace(
        name="tlb_hit_latency", lower_bound=1, upper_bound=32, default=20
    )
    tlb_miss_latency: DiscreteSpace = DiscreteSpace(
        name="tlb_miss_latency", lower_bound=1, upper_bound=32, default=20
    )

    tlb_entries: DiscreteSpace = DiscreteSpace(
        # Bound: [1, 32] = [2^0, 2^5]
        name="tlb_entries",
        formula=power_of_two,
        lower_bound=0,
        upper_bound=5,
        default=3,
    )
    tlb_assoc: DiscreteSpace = DiscreteSpace(
        # Bounds: [2^0, 2^5] = [1, 32]
        name="tlb_assoc",
        formula=power_of_two,
        lower_bound=0,
        upper_bound=5,
        default=0,
    )
    tlb_page_size: DiscreteSpace = DiscreteSpace(
        name="tlb_page_size",
        lower_bound=conv.short_size_to_bytes("1kb"),
        upper_bound=conv.short_size_to_bytes("32kb"),
        default=conv.short_size_to_bytes("4kb"),
    )

    tlb_max_outstanding_walks: DiscreteSpace = DiscreteSpace(
        name="tlb_max_outstanding_walks", lower_bound=2, upper_bound=16, default=8
    )

    tlb_bandwidth: DiscreteSpace = DiscreteSpace(
        name="tlb_bandwidth", lower_bound=2, upper_bound=16, default=4
    )

    l2cache_size: DiscreteSpace = DiscreteSpace(
        # Lower bound: 128kb, upper bound: 2048kb
        name="l2cache_size",
        lower_bound=conv.short_size_to_base2("128kb"),
        upper_bound=conv.short_size_to_base2("2048kb"),
        default=conv.short_size_to_base2("128kb"),
        formula=power_of_two,
    )

    enable_l2: DiscreteSpace = DiscreteSpace(
        name="enable_l2", lower_bound=0, upper_bound=1, default=0
    )

    #  ##################### DMA settings. #####################
    # Use pipelined DMA optimization
    pipelined_dma: DiscreteSpace = DiscreteSpace(
        name="pipelined_dma", lower_bound=0, upper_bound=1, default=0
    )

    # Ready bits optimization optimization
    ready_mode: DiscreteSpace = DiscreteSpace(
        name="ready_mode", lower_bound=0, upper_bound=1, default=0
    )

    # Whether to ignore the DMA induced cache flush overhead
    ignore_cache_flush: DiscreteSpace = DiscreteSpace(
        name="ignore_cache_flush", lower_bound=0, upper_bound=1, default=0
    )
