from dataclasses import dataclass

from sysgym.envs.rocksdb.schema.schema import RocksDBParamSchema
from sysgym.params.boxes import ContinuousBox, DiscreteBox


@dataclass(init=False, frozen=True)
class RocksDB10Params(RocksDBParamSchema):
    # Tuning flush and compactions:
    # Ref:
    # https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide#tuning-flushes-and-compactions

    # The default values are taken from rocksdb default, options.h
    max_background_compactions: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=256, default=1
    )

    # TODO(mixed optimization): Small discrete values should use optimize_discrete
    # max num concurrent bg compaction in parallel
    max_background_flushes: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=10, default=1
    )
    # Flushing options
    # Ref https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide#flushing-options
    write_buffer_size: DiscreteBox = DiscreteBox(
        lower_bound=12097152, upper_bound=167772160, default=67108864
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
    max_bytes_for_level_multiplier: ContinuousBox = ContinuousBox(
        lower_bound=5, upper_bound=15, default=10
    )

    block_size: DiscreteBox = DiscreteBox(
        lower_bound=32, upper_bound=500000, default=4096
    )

    # level optimization, compactions
    level0_file_num_compaction_trigger: DiscreteBox = DiscreteBox(
        lower_bound=1, upper_bound=64, default=4
    )

    level0_slowdown_writes_trigger: DiscreteBox = DiscreteBox(
        lower_bound=0, upper_bound=1024, default=0
    )
    level0_stop_writes_trigger: DiscreteBox = DiscreteBox(
        lower_bound=0, upper_bound=1024, default=36
    )

    # compression_type: CategoricalSpace = CategoricalBox(
    #     name="compression_type",
    #     categories=["Snappy", "ZSTD", "Zlib", "lz4"],
    #     lower_bound=0,
    #     upper_bound=3,
    # )
