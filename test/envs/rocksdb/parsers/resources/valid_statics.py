from sysgym.envs.rocksdb.stats.rocksdb_stats import RocksDBStatistics
from sysgym.envs.rocksdb.stats.statistics_dao import MacroStats, MicroStats

statistics_valid_testcase = RocksDBStatistics(
    name="RocksDBStatistics",
    rocksdb_block_cache_miss=MacroStats(name="rocksdb_block_cache_miss", count=0),
    rocksdb_block_cache_hit=MacroStats(name="rocksdb_block_cache_hit", count=0),
    rocksdb_block_cache_add=MacroStats(name="rocksdb_block_cache_add", count=0),
    rocksdb_block_cache_add_failures=MacroStats(
        name="rocksdb_block_cache_add_failures", count=0
    ),
    rocksdb_block_cache_index_miss=MacroStats(
        name="rocksdb_block_cache_index_miss", count=0
    ),
    rocksdb_block_cache_index_hit=MacroStats(
        name="rocksdb_block_cache_index_hit", count=0
    ),
    rocksdb_block_cache_index_add=MacroStats(
        name="rocksdb_block_cache_index_add", count=0
    ),
    rocksdb_block_cache_index_bytes_insert=MacroStats(
        name="rocksdb_block_cache_index_bytes_insert", count=0
    ),
    rocksdb_block_cache_index_bytes_evict=MacroStats(
        name="rocksdb_block_cache_index_bytes_evict", count=0
    ),
    rocksdb_block_cache_filter_miss=MacroStats(
        name="rocksdb_block_cache_filter_miss", count=0
    ),
    rocksdb_block_cache_filter_hit=MacroStats(
        name="rocksdb_block_cache_filter_hit", count=0
    ),
    rocksdb_block_cache_filter_add=MacroStats(
        name="rocksdb_block_cache_filter_add", count=0
    ),
    rocksdb_block_cache_filter_bytes_insert=MacroStats(
        name="rocksdb_block_cache_filter_bytes_insert", count=0
    ),
    rocksdb_block_cache_filter_bytes_evict=MacroStats(
        name="rocksdb_block_cache_filter_bytes_evict", count=0
    ),
    rocksdb_block_cache_data_miss=MacroStats(
        name="rocksdb_block_cache_data_miss", count=0
    ),
    rocksdb_block_cache_data_hit=MacroStats(
        name="rocksdb_block_cache_data_hit", count=0
    ),
    rocksdb_block_cache_data_add=MacroStats(
        name="rocksdb_block_cache_data_add", count=0
    ),
    rocksdb_block_cache_data_bytes_insert=MacroStats(
        name="rocksdb_block_cache_data_bytes_insert", count=0
    ),
    rocksdb_block_cache_bytes_read=MacroStats(
        name="rocksdb_block_cache_bytes_read", count=0
    ),
    rocksdb_block_cache_bytes_write=MacroStats(
        name="rocksdb_block_cache_bytes_write", count=0
    ),
    rocksdb_bloom_filter_useful=MacroStats(name="rocksdb_bloom_filter_useful", count=0),
    rocksdb_bloom_filter_full_positive=MacroStats(
        name="rocksdb_bloom_filter_full_positive", count=0
    ),
    rocksdb_bloom_filter_full_true_positive=MacroStats(
        name="rocksdb_bloom_filter_full_true_positive", count=0
    ),
    rocksdb_bloom_filter_micros=MacroStats(name="rocksdb_bloom_filter_micros", count=0),
    rocksdb_persistent_cache_hit=MacroStats(
        name="rocksdb_persistent_cache_hit", count=0
    ),
    rocksdb_persistent_cache_miss=MacroStats(
        name="rocksdb_persistent_cache_miss", count=0
    ),
    rocksdb_sim_block_cache_hit=MacroStats(name="rocksdb_sim_block_cache_hit", count=0),
    rocksdb_sim_block_cache_miss=MacroStats(
        name="rocksdb_sim_block_cache_miss", count=0
    ),
    rocksdb_memtable_hit=MacroStats(name="rocksdb_memtable_hit", count=0),
    rocksdb_memtable_miss=MacroStats(name="rocksdb_memtable_miss", count=23016590),
    rocksdb_l0_hit=MacroStats(name="rocksdb_l0_hit", count=0),
    rocksdb_l1_hit=MacroStats(name="rocksdb_l1_hit", count=0),
    rocksdb_l2andup_hit=MacroStats(name="rocksdb_l2andup_hit", count=0),
    rocksdb_compaction_key_drop_new=MacroStats(
        name="rocksdb_compaction_key_drop_new", count=0
    ),
    rocksdb_compaction_key_drop_obsolete=MacroStats(
        name="rocksdb_compaction_key_drop_obsolete", count=0
    ),
    rocksdb_compaction_key_drop_range_del=MacroStats(
        name="rocksdb_compaction_key_drop_range_del", count=0
    ),
    rocksdb_compaction_key_drop_user=MacroStats(
        name="rocksdb_compaction_key_drop_user", count=0
    ),
    rocksdb_compaction_range_del_drop_obsolete=MacroStats(
        name="rocksdb_compaction_range_del_drop_obsolete", count=0
    ),
    rocksdb_compaction_optimized_del_drop_obsolete=MacroStats(
        name="rocksdb_compaction_optimized_del_drop_obsolete", count=0
    ),
    rocksdb_compaction_cancelled=MacroStats(
        name="rocksdb_compaction_cancelled", count=0
    ),
    rocksdb_number_keys_written=MacroStats(
        name="rocksdb_number_keys_written", count=3795643
    ),
    rocksdb_number_keys_read=MacroStats(
        name="rocksdb_number_keys_read", count=23016590
    ),
    rocksdb_number_keys_updated=MacroStats(name="rocksdb_number_keys_updated", count=0),
    rocksdb_bytes_written=MacroStats(name="rocksdb_bytes_written", count=371664902),
    rocksdb_bytes_read=MacroStats(name="rocksdb_bytes_read", count=0),
    rocksdb_number_db_seek=MacroStats(name="rocksdb_number_db_seek", count=270766),
    rocksdb_number_db_next=MacroStats(name="rocksdb_number_db_next", count=154936133),
    rocksdb_number_db_prev=MacroStats(name="rocksdb_number_db_prev", count=0),
    rocksdb_number_db_seek_found=MacroStats(
        name="rocksdb_number_db_seek_found", count=270759
    ),
    rocksdb_number_db_next_found=MacroStats(
        name="rocksdb_number_db_next_found", count=154936101
    ),
    rocksdb_number_db_prev_found=MacroStats(
        name="rocksdb_number_db_prev_found", count=0
    ),
    rocksdb_db_iter_bytes_read=MacroStats(
        name="rocksdb_db_iter_bytes_read", count=26165742983
    ),
    rocksdb_no_file_closes=MacroStats(name="rocksdb_no_file_closes", count=0),
    rocksdb_no_file_opens=MacroStats(name="rocksdb_no_file_opens", count=0),
    rocksdb_no_file_errors=MacroStats(name="rocksdb_no_file_errors", count=0),
    rocksdb_l0_slowdown_micros=MacroStats(name="rocksdb_l0_slowdown_micros", count=0),
    rocksdb_memtable_compaction_micros=MacroStats(
        name="rocksdb_memtable_compaction_micros", count=0
    ),
    rocksdb_l0_num_files_stall_micros=MacroStats(
        name="rocksdb_l0_num_files_stall_micros", count=0
    ),
    rocksdb_stall_micros=MacroStats(name="rocksdb_stall_micros", count=0),
    rocksdb_db_mutex_wait_micros=MacroStats(
        name="rocksdb_db_mutex_wait_micros", count=0
    ),
    rocksdb_rate_limit_delay_millis=MacroStats(
        name="rocksdb_rate_limit_delay_millis", count=0
    ),
    rocksdb_num_iterators=MacroStats(name="rocksdb_num_iterators", count=0),
    rocksdb_number_multiget_get=MacroStats(name="rocksdb_number_multiget_get", count=0),
    rocksdb_number_multiget_keys_read=MacroStats(
        name="rocksdb_number_multiget_keys_read", count=0
    ),
    rocksdb_number_multiget_bytes_read=MacroStats(
        name="rocksdb_number_multiget_bytes_read", count=0
    ),
    rocksdb_number_deletes_filtered=MacroStats(
        name="rocksdb_number_deletes_filtered", count=0
    ),
    rocksdb_number_merge_failures=MacroStats(
        name="rocksdb_number_merge_failures", count=0
    ),
    rocksdb_bloom_filter_prefix_checked=MacroStats(
        name="rocksdb_bloom_filter_prefix_checked", count=0
    ),
    rocksdb_bloom_filter_prefix_useful=MacroStats(
        name="rocksdb_bloom_filter_prefix_useful", count=0
    ),
    rocksdb_number_reseeks_iteration=MacroStats(
        name="rocksdb_number_reseeks_iteration", count=0
    ),
    rocksdb_getupdatessince_calls=MacroStats(
        name="rocksdb_getupdatessince_calls", count=0
    ),
    rocksdb_block_cachecompressed_miss=MacroStats(
        name="rocksdb_block_cachecompressed_miss", count=0
    ),
    rocksdb_block_cachecompressed_hit=MacroStats(
        name="rocksdb_block_cachecompressed_hit", count=0
    ),
    rocksdb_block_cachecompressed_add=MacroStats(
        name="rocksdb_block_cachecompressed_add", count=0
    ),
    rocksdb_block_cachecompressed_add_failures=MacroStats(
        name="rocksdb_block_cachecompressed_add_failures", count=0
    ),
    rocksdb_wal_synced=MacroStats(name="rocksdb_wal_synced", count=0),
    rocksdb_wal_bytes=MacroStats(name="rocksdb_wal_bytes", count=371664902),
    rocksdb_write_self=MacroStats(name="rocksdb_write_self", count=3795643),
    rocksdb_write_other=MacroStats(name="rocksdb_write_other", count=0),
    rocksdb_write_timeout=MacroStats(name="rocksdb_write_timeout", count=0),
    rocksdb_write_wal=MacroStats(name="rocksdb_write_wal", count=3795643),
    rocksdb_compact_read_bytes=MacroStats(name="rocksdb_compact_read_bytes", count=0),
    rocksdb_compact_write_bytes=MacroStats(name="rocksdb_compact_write_bytes", count=0),
    rocksdb_flush_write_bytes=MacroStats(name="rocksdb_flush_write_bytes", count=0),
    rocksdb_compact_read_marked_bytes=MacroStats(
        name="rocksdb_compact_read_marked_bytes", count=0
    ),
    rocksdb_compact_read_periodic_bytes=MacroStats(
        name="rocksdb_compact_read_periodic_bytes", count=0
    ),
    rocksdb_compact_read_ttl_bytes=MacroStats(
        name="rocksdb_compact_read_ttl_bytes", count=0
    ),
    rocksdb_compact_write_marked_bytes=MacroStats(
        name="rocksdb_compact_write_marked_bytes", count=0
    ),
    rocksdb_compact_write_periodic_bytes=MacroStats(
        name="rocksdb_compact_write_periodic_bytes", count=0
    ),
    rocksdb_compact_write_ttl_bytes=MacroStats(
        name="rocksdb_compact_write_ttl_bytes", count=0
    ),
    rocksdb_number_direct_load_table_properties=MacroStats(
        name="rocksdb_number_direct_load_table_properties", count=0
    ),
    rocksdb_number_superversion_acquires=MacroStats(
        name="rocksdb_number_superversion_acquires", count=5
    ),
    rocksdb_number_superversion_releases=MacroStats(
        name="rocksdb_number_superversion_releases", count=0
    ),
    rocksdb_number_superversion_cleanups=MacroStats(
        name="rocksdb_number_superversion_cleanups", count=0
    ),
    rocksdb_number_block_compressed=MacroStats(
        name="rocksdb_number_block_compressed", count=0
    ),
    rocksdb_number_block_decompressed=MacroStats(
        name="rocksdb_number_block_decompressed", count=0
    ),
    rocksdb_number_block_not_compressed=MacroStats(
        name="rocksdb_number_block_not_compressed", count=0
    ),
    rocksdb_merge_operation_time_nanos=MacroStats(
        name="rocksdb_merge_operation_time_nanos", count=0
    ),
    rocksdb_filter_operation_time_nanos=MacroStats(
        name="rocksdb_filter_operation_time_nanos", count=0
    ),
    rocksdb_row_cache_hit=MacroStats(name="rocksdb_row_cache_hit", count=0),
    rocksdb_row_cache_miss=MacroStats(name="rocksdb_row_cache_miss", count=0),
    rocksdb_read_amp_estimate_useful_bytes=MacroStats(
        name="rocksdb_read_amp_estimate_useful_bytes", count=0
    ),
    rocksdb_read_amp_total_read_bytes=MacroStats(
        name="rocksdb_read_amp_total_read_bytes", count=0
    ),
    rocksdb_number_rate_limiter_drains=MacroStats(
        name="rocksdb_number_rate_limiter_drains", count=0
    ),
    rocksdb_number_iter_skip=MacroStats(
        name="rocksdb_number_iter_skip", count=22104044
    ),
    rocksdb_blobdb_num_put=MacroStats(name="rocksdb_blobdb_num_put", count=0),
    rocksdb_blobdb_num_write=MacroStats(name="rocksdb_blobdb_num_write", count=0),
    rocksdb_blobdb_num_get=MacroStats(name="rocksdb_blobdb_num_get", count=0),
    rocksdb_blobdb_num_multiget=MacroStats(name="rocksdb_blobdb_num_multiget", count=0),
    rocksdb_blobdb_num_seek=MacroStats(name="rocksdb_blobdb_num_seek", count=0),
    rocksdb_blobdb_num_next=MacroStats(name="rocksdb_blobdb_num_next", count=0),
    rocksdb_blobdb_num_prev=MacroStats(name="rocksdb_blobdb_num_prev", count=0),
    rocksdb_blobdb_num_keys_written=MacroStats(
        name="rocksdb_blobdb_num_keys_written", count=0
    ),
    rocksdb_blobdb_num_keys_read=MacroStats(
        name="rocksdb_blobdb_num_keys_read", count=0
    ),
    rocksdb_blobdb_bytes_written=MacroStats(
        name="rocksdb_blobdb_bytes_written", count=0
    ),
    rocksdb_blobdb_bytes_read=MacroStats(name="rocksdb_blobdb_bytes_read", count=0),
    rocksdb_blobdb_write_inlined=MacroStats(
        name="rocksdb_blobdb_write_inlined", count=0
    ),
    rocksdb_blobdb_write_inlined_ttl=MacroStats(
        name="rocksdb_blobdb_write_inlined_ttl", count=0
    ),
    rocksdb_blobdb_write_blob=MacroStats(name="rocksdb_blobdb_write_blob", count=0),
    rocksdb_blobdb_write_blob_ttl=MacroStats(
        name="rocksdb_blobdb_write_blob_ttl", count=0
    ),
    rocksdb_blobdb_blob_file_bytes_written=MacroStats(
        name="rocksdb_blobdb_blob_file_bytes_written", count=0
    ),
    rocksdb_blobdb_blob_file_bytes_read=MacroStats(
        name="rocksdb_blobdb_blob_file_bytes_read", count=0
    ),
    rocksdb_blobdb_blob_file_synced=MacroStats(
        name="rocksdb_blobdb_blob_file_synced", count=0
    ),
    rocksdb_blobdb_blob_index_expired_count=MacroStats(
        name="rocksdb_blobdb_blob_index_expired_count", count=0
    ),
    rocksdb_blobdb_blob_index_expired_size=MacroStats(
        name="rocksdb_blobdb_blob_index_expired_size", count=0
    ),
    rocksdb_blobdb_blob_index_evicted_count=MacroStats(
        name="rocksdb_blobdb_blob_index_evicted_count", count=0
    ),
    rocksdb_blobdb_blob_index_evicted_size=MacroStats(
        name="rocksdb_blobdb_blob_index_evicted_size", count=0
    ),
    rocksdb_blobdb_gc_num_files=MacroStats(name="rocksdb_blobdb_gc_num_files", count=0),
    rocksdb_blobdb_gc_num_new_files=MacroStats(
        name="rocksdb_blobdb_gc_num_new_files", count=0
    ),
    rocksdb_blobdb_gc_failures=MacroStats(name="rocksdb_blobdb_gc_failures", count=0),
    rocksdb_blobdb_gc_num_keys_overwritten=MacroStats(
        name="rocksdb_blobdb_gc_num_keys_overwritten", count=0
    ),
    rocksdb_blobdb_gc_num_keys_expired=MacroStats(
        name="rocksdb_blobdb_gc_num_keys_expired", count=0
    ),
    rocksdb_blobdb_gc_num_keys_relocated=MacroStats(
        name="rocksdb_blobdb_gc_num_keys_relocated", count=0
    ),
    rocksdb_blobdb_gc_bytes_overwritten=MacroStats(
        name="rocksdb_blobdb_gc_bytes_overwritten", count=0
    ),
    rocksdb_blobdb_gc_bytes_expired=MacroStats(
        name="rocksdb_blobdb_gc_bytes_expired", count=0
    ),
    rocksdb_blobdb_gc_bytes_relocated=MacroStats(
        name="rocksdb_blobdb_gc_bytes_relocated", count=0
    ),
    rocksdb_blobdb_fifo_num_files_evicted=MacroStats(
        name="rocksdb_blobdb_fifo_num_files_evicted", count=0
    ),
    rocksdb_blobdb_fifo_num_keys_evicted=MacroStats(
        name="rocksdb_blobdb_fifo_num_keys_evicted", count=0
    ),
    rocksdb_blobdb_fifo_bytes_evicted=MacroStats(
        name="rocksdb_blobdb_fifo_bytes_evicted", count=0
    ),
    rocksdb_txn_overhead_mutex_prepare=MacroStats(
        name="rocksdb_txn_overhead_mutex_prepare", count=0
    ),
    rocksdb_txn_overhead_mutex_old_commit_map=MacroStats(
        name="rocksdb_txn_overhead_mutex_old_commit_map", count=0
    ),
    rocksdb_txn_overhead_duplicate_key=MacroStats(
        name="rocksdb_txn_overhead_duplicate_key", count=0
    ),
    rocksdb_txn_overhead_mutex_snapshot=MacroStats(
        name="rocksdb_txn_overhead_mutex_snapshot", count=0
    ),
    rocksdb_txn_get_tryagain=MacroStats(name="rocksdb_txn_get_tryagain", count=0),
    rocksdb_number_multiget_keys_found=MacroStats(
        name="rocksdb_number_multiget_keys_found", count=0
    ),
    rocksdb_num_iterator_created=MacroStats(
        name="rocksdb_num_iterator_created", count=270766
    ),
    rocksdb_num_iterator_deleted=MacroStats(
        name="rocksdb_num_iterator_deleted", count=270766
    ),
    rocksdb_block_cache_compression_dict_miss=MacroStats(
        name="rocksdb_block_cache_compression_dict_miss", count=0
    ),
    rocksdb_block_cache_compression_dict_hit=MacroStats(
        name="rocksdb_block_cache_compression_dict_hit", count=0
    ),
    rocksdb_block_cache_compression_dict_add=MacroStats(
        name="rocksdb_block_cache_compression_dict_add", count=0
    ),
    rocksdb_block_cache_compression_dict_bytes_insert=MacroStats(
        name="rocksdb_block_cache_compression_dict_bytes_insert", count=0
    ),
    rocksdb_block_cache_compression_dict_bytes_evict=MacroStats(
        name="rocksdb_block_cache_compression_dict_bytes_evict", count=0
    ),
    rocksdb_block_cache_add_redundant=MacroStats(
        name="rocksdb_block_cache_add_redundant", count=0
    ),
    rocksdb_block_cache_index_add_redundant=MacroStats(
        name="rocksdb_block_cache_index_add_redundant", count=0
    ),
    rocksdb_block_cache_filter_add_redundant=MacroStats(
        name="rocksdb_block_cache_filter_add_redundant", count=0
    ),
    rocksdb_block_cache_data_add_redundant=MacroStats(
        name="rocksdb_block_cache_data_add_redundant", count=0
    ),
    rocksdb_block_cache_compression_dict_add_redundant=MacroStats(
        name="rocksdb_block_cache_compression_dict_add_redundant", count=0
    ),
    rocksdb_files_marked_trash=MacroStats(name="rocksdb_files_marked_trash", count=0),
    rocksdb_files_deleted_immediately=MacroStats(
        name="rocksdb_files_deleted_immediately", count=0
    ),
    rocksdb_db_get_micros=MicroStats(
        name="rocksdb_db_get_micros",
        p50=7.588484,
        p95=18.591068,
        p99=21.880181,
        p100=1194.0,
        count=23016590,
        sum=199095631,
    ),
    rocksdb_db_write_micros=MicroStats(
        name="rocksdb_db_write_micros",
        p50=5.230106,
        p95=9.972863,
        p99=20.700972,
        p100=34890.0,
        count=3795643,
        sum=24488900,
    ),
    rocksdb_compaction_times_micros=MicroStats(
        name="rocksdb_compaction_times_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_compaction_times_cpu_micros=MicroStats(
        name="rocksdb_compaction_times_cpu_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_subcompaction_setup_times_micros=MicroStats(
        name="rocksdb_subcompaction_setup_times_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_table_sync_micros=MicroStats(
        name="rocksdb_table_sync_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_compaction_outfile_sync_micros=MicroStats(
        name="rocksdb_compaction_outfile_sync_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_wal_file_sync_micros=MicroStats(
        name="rocksdb_wal_file_sync_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_manifest_file_sync_micros=MicroStats(
        name="rocksdb_manifest_file_sync_micros",
        p50=3654.0,
        p95=4127.0,
        p99=4127.0,
        p100=4127.0,
        count=2,
        sum=7781,
    ),
    rocksdb_table_open_io_micros=MicroStats(
        name="rocksdb_table_open_io_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_db_multiget_micros=MicroStats(
        name="rocksdb_db_multiget_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_read_block_compaction_micros=MicroStats(
        name="rocksdb_read_block_compaction_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_read_block_get_micros=MicroStats(
        name="rocksdb_read_block_get_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_write_raw_block_micros=MicroStats(
        name="rocksdb_write_raw_block_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_l0_slowdown_count=MicroStats(
        name="rocksdb_l0_slowdown_count",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_memtable_compaction_count=MicroStats(
        name="rocksdb_memtable_compaction_count",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_num_files_stall_count=MicroStats(
        name="rocksdb_num_files_stall_count",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_hard_rate_limit_delay_count=MicroStats(
        name="rocksdb_hard_rate_limit_delay_count",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_soft_rate_limit_delay_count=MicroStats(
        name="rocksdb_soft_rate_limit_delay_count",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_numfiles_in_singlecompaction=MicroStats(
        name="rocksdb_numfiles_in_singlecompaction",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_db_seek_micros=MicroStats(
        name="rocksdb_db_seek_micros",
        p50=8.603318,
        p95=20.348313,
        p99=27.633701,
        p100=746.0,
        count=270766,
        sum=2621269,
    ),
    rocksdb_db_write_stall=MicroStats(
        name="rocksdb_db_write_stall",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_sst_read_micros=MicroStats(
        name="rocksdb_sst_read_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_num_subcompactions_scheduled=MicroStats(
        name="rocksdb_num_subcompactions_scheduled",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_bytes_per_read=MicroStats(
        name="rocksdb_bytes_per_read",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=23016590,
        sum=0,
    ),
    rocksdb_bytes_per_write=MicroStats(
        name="rocksdb_bytes_per_write",
        p50=86.209635,
        p95=186.525127,
        p99=318.204579,
        p100=1058.0,
        count=3795643,
        sum=371664902,
    ),
    rocksdb_bytes_per_multiget=MicroStats(
        name="rocksdb_bytes_per_multiget",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_bytes_compressed=MicroStats(
        name="rocksdb_bytes_compressed",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_bytes_decompressed=MicroStats(
        name="rocksdb_bytes_decompressed",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_compression_times_nanos=MicroStats(
        name="rocksdb_compression_times_nanos",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_decompression_times_nanos=MicroStats(
        name="rocksdb_decompression_times_nanos",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_read_num_merge_operands=MicroStats(
        name="rocksdb_read_num_merge_operands",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_key_size=MicroStats(
        name="rocksdb_blobdb_key_size",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_value_size=MicroStats(
        name="rocksdb_blobdb_value_size",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_write_micros=MicroStats(
        name="rocksdb_blobdb_write_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_get_micros=MicroStats(
        name="rocksdb_blobdb_get_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_multiget_micros=MicroStats(
        name="rocksdb_blobdb_multiget_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_seek_micros=MicroStats(
        name="rocksdb_blobdb_seek_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_next_micros=MicroStats(
        name="rocksdb_blobdb_next_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_prev_micros=MicroStats(
        name="rocksdb_blobdb_prev_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_blob_file_write_micros=MicroStats(
        name="rocksdb_blobdb_blob_file_write_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_blob_file_read_micros=MicroStats(
        name="rocksdb_blobdb_blob_file_read_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_blob_file_sync_micros=MicroStats(
        name="rocksdb_blobdb_blob_file_sync_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_gc_micros=MicroStats(
        name="rocksdb_blobdb_gc_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_compression_micros=MicroStats(
        name="rocksdb_blobdb_compression_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_blobdb_decompression_micros=MicroStats(
        name="rocksdb_blobdb_decompression_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_db_flush_micros=MicroStats(
        name="rocksdb_db_flush_micros",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_sst_batch_size=MicroStats(
        name="rocksdb_sst_batch_size",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_num_index_and_filter_blocks_read_per_level=MicroStats(
        name="rocksdb_num_index_and_filter_blocks_read_per_level",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_num_data_blocks_read_per_level=MicroStats(
        name="rocksdb_num_data_blocks_read_per_level",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
    rocksdb_num_sst_read_per_level=MicroStats(
        name="rocksdb_num_sst_read_per_level",
        p50=0.0,
        p95=0.0,
        p99=0.0,
        p100=0.0,
        count=0,
        sum=0,
    ),
)
