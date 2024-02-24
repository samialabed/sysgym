from dataclasses import dataclass

from sysgym.envs.rocksdb.schema.schema import RocksDBParamSchema
from sysgym.params.boxes import BooleanBox, CategoricalBox, ContinuousBox, DiscreteBox
from sysgym.utils import converters


@dataclass(init=False, frozen=True)
class RocksDB17Params(RocksDBParamSchema):
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
        lower_bound=converters.short_size_to_bytes("10mb"),
        upper_bound=converters.short_size_to_bytes("1gb"),
        default=converters.short_size_to_bytes("64mb"),
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
        lower_bound=converters.short_size_to_bytes("1kb"),
        upper_bound=converters.short_size_to_bytes("128kb"),
        default=converters.short_size_to_bytes("4kb"),
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

    # V2 Extension from options.H!!!!!!!
    compression_type: CategoricalBox = CategoricalBox(
        categories=["Snappy", "ZSTD", "Zlib", "lz4"],
    )

    compaction_readahead_size: DiscreteBox = DiscreteBox(
        lower_bound=0,
        upper_bound=converters.short_size_to_bytes("4mb"),
        default=0,
        # If non-zero, we perform bigger reads when doing compaction. If you're
        # running RocksDB on spinning disks, you should set this to at least 2MB.
        # That way RocksDB's compaction is doing sequential instead of random
        # reads. When non-zero, we also force
        # new_table_reader_for_compaction_inputs to true.
    )

    writable_file_max_buffer_size: DiscreteBox = DiscreteBox(
        lower_bound=1024,
        upper_bound=converters.short_size_to_bytes("8mb"),
        default=converters.short_size_to_bytes("1mb"),
        # This is the maximum buffer size that is used by WritableFileWriter. With
        # direct IO, we need to maintain an aligned buffer for writes. We allow
        # the buffer to grow until it's size hits the limit in buffered IO and
        # fix the buffer size when using direct IO to ensure alignment of write
        # requests if the logical sector size is unusual
    )

    enable_pipelined_write: BooleanBox = BooleanBox(
        default=False
        # By default, a single write thread queue is maintained. The thread gets to
        # the head of the queue becomes write batch group leader and responsible
        # for writing to WAL and memtable for the batch group.
        #
        # If enable_pipelined_write is true, separate write thread queue is
        # maintained for WAL write and memtable write. A write thread first enter
        # WAL writer queue and then memtable writer queue. Pending thread on the
        # WAL writer queue thus only have to wait for previous writers to finish
        # their WAL writing but not the memtable writing. Enabling the feature
        # may improve write throughput and reduce latency of the prepare phase of
        # two-phase commit.
    )

    two_write_queues: BooleanBox = BooleanBox(
        default=False
        # If enabled it uses two queues for writes, one for the ones with
        # disable_memtable and one for the ones that also write to memtable. This
        # allows the memtable writes not to lag behind other writes. It can be
        # used to optimize MySQL 2PC in which only the commits, which are serial,
        # write to memtable.
    )

    use_direct_reads: BooleanBox = BooleanBox(
        default=False
        # Enable direct I/O mode for read/write
        # they may or may not improve performance depending on the use case
        # Files will be opened in "direct I/O" mode
        # which means that data r/w from the disk will not be cached or
        # buffered. The hardware buffer of the devices may however still
        # be used. Memory mapped files are not impacted by these parameters.
        #
        # Use O_DIRECT for user and compaction reads.
        # When true, we also force new_table_reader_for_compaction_inputs to true.
    )

    use_adaptive_mutex: BooleanBox = BooleanBox(
        default=False
        #  Use adaptive mutex, which spins in the user space before resorting
        # to kernel. This could reduce context switch when the mutex is not
        # heavily contended. However, if the mutex is hot, we could end up
        # wasting spin time.
        # Default: false
    )
