# RocksDB parameters
------


* __write_buffer_size__:   sets the size of a single memtable. Once memtable exceeds this size, it is marked immutable and a new one is created.
* __max_write_buffer_number__: sets the maximum number of memtables, both active and immutable. If the active memtable fills up and the total number of memtables is larger than max_write_buffer_number we stall further writes. This may happen if the flush process is slower than the write rate.
* __min_write_buffer_number_to_merge__:  is the minimum number of memtables to be merged before flushing to storage. For example, if this option is set to 2, immutable memtables are only flushed when there are two of them - a single immutable memtable will never be flushed. If multiple memtables are merged together, less data may be written to storage since two updates are merged to a single key. However, every Get() must traverse all immutable memtables linearly to check if the key is there. Setting this option too high may hurt read performance.
* __max_background_compactions__: is the maximum number of concurrent background compactions. The default is 1, but to fully utilize your CPU and storage you might want to increase this to the minimum of (the number of cores in the system, the disk throughput divided by the average throughput of one compaction thread)
* __max_background_flushes__:  is the maximum number of concurrent flush operations. It is usually good enough to set this to 1.
* __max_bytes_for_level_multiplier__: A multiplier to compute max bytes for level-N (N >= 2), each subsequenet level is max_bytes_for_level_multiplier larger than previous one.
* __block_size__:  RocksDB packs user data in blocks. When reading a key-value pair from a table file, an entire block is loaded into memory. Block size is 4KB by default. Each table file contains an index that lists offsets of all blocks. Increasing block_size means that the index contains fewer entries (since there are fewer blocks per file) and is thus smaller. Increasing block_size decreases memory usage and space amplification, but increases read amplification.
* __level0_file_num_compaction_trigger__: Once level 0 reaches this number of files, L0->L1 compaction is triggered. We can therefore estimate level 0 size in stable state as write_buffer_size * min_write_buffer_number_to_merge * level0_file_num_compaction_trigger.

* __target_file_size_base__ and __target_file_size_multiplier__: Files in level 1 will have target_file_size_base bytes. Each next level's file size will be target_file_size_multiplier bigger than previous one. However, by default target_file_size_multiplier is 1, so files in all L1..Lmax levels are equal. Increasing target_file_size_base will reduce total number of database files, which is generally a good thing. We recommend setting target_file_size_base to be max_bytes_for_level_base / 10, so that there are 10 files in level 1.

* __compression_per_level__: Use this option to set different compressions for different levels. It usually makes sense to avoid compressing levels 0 and 1 and to compress data only in higher levels. You can even set slower compression in highest level and faster compression in lower levels (by highest we mean Lmax).

* __num_levels__: It is safe for num_levels to be bigger than expected number of levels in the database. Some higher levels may be empty, but this will not impact performance in any way. Only change this option if you expect your number of levels will be greater than 7 (default).


* __filter_policy__: If you're doing point lookups on an uncompacted DB, you definitely want to turn bloom filters on. We use bloom filters to avoid unnecessary disk reads. You should set filter_policy to rocksdb::NewBloomFilterPolicy(bits_per_key). Default bits_per_key is 10, which yields ~1% false positive rate. Larger bits_per_key values will reduce false positive rate, but increase memory usage and space amplification.


-----
## To implement

# --compression_type=lz4 -enable_pipelined_write=true
    # filter_policy = CategoricalSpace(
    #     name="filter_policy", categories=["rocksdb.BuiltinBloomFilter", "nullptr"]
    # )

    # compression_type = CategoricalSpace(
    #     name="compression_type",
    #     categories=["Snappy", "ZSTD", "Zlib", "lz4"],
    # )
