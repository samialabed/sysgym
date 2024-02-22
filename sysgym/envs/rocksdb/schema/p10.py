from dataclasses import dataclass

from sysgym.envs.rocksdb.schema.schema import RocksDBParamSchema
from sysgym.params.boxes import DiscreteBox
from sysgym.utils import converters


@dataclass(init=False, frozen=True)
class RocksDB10Params(RocksDBParamSchema):
    # Tuning flush and compactions:
    # Ref:
    # https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide#tuning-flushes-and-compactions

    # The default values are taken from rocksdb default, options.h
    max_background_compactions: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=6, default=1
    )

    # max num concurrent bg compaction in parallel
    max_background_flushes: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=10, default=1
    )
    # Flushing options
    # Ref https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide#flushing-options
    write_buffer_size: DiscreteBox = DiscreteBox(
        lower_bound=converters.short_size_to_base2("10mb"),
        upper_bound=converters.short_size_to_base2("1gb"),
        default=converters.short_size_to_base2("64mb"),
    )
    max_write_buffer_number: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=128, default=2
    )
    min_write_buffer_number_to_merge: DiscreteBox = DiscreteBox(
        lower_bound=1,
        upper_bound=32,
        default=1,
    )

    # space params, tuning space
    max_bytes_for_level_multiplier: DiscreteBox = DiscreteBox(
        lower_bound=5, upper_bound=20, default=10
    )

    block_size: DiscreteBox = DiscreteBox(
        lower_bound=converters.short_size_to_base2("1kb"),
        upper_bound=converters.short_size_to_base2("128kb"),
        default=converters.short_size_to_base2("4kb"),
    )

    # level optimization, compactions
    level0_file_num_compaction_trigger: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=64, default=4
    )

    level0_slowdown_writes_trigger: DiscreteBox = DiscreteBox(
        lower_bound=-1, upper_bound=64, default=20
    )
    level0_stop_writes_trigger: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=64, default=36
    )
