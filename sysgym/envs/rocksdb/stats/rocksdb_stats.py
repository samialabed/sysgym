from dataclasses import dataclass
from typing import Union

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.stats.statistics_dao import MacroStats, MicroStats
from sysgym.envs.rocksdb.stats.stats_dao import Statistics

StatisticsType = Union[MacroStats, MicroStats]


@dataclass_json
@dataclass
class RocksDBStatistics(Statistics):
    # all statistics and their explanation is here
    # https://github.com/facebook/rocksdb/blob/master/include/rocksdb/statistics.h
    rocksdb_block_cache_miss: MacroStats
    rocksdb_block_cache_hit: MacroStats
    rocksdb_block_cache_add: MacroStats
    rocksdb_block_cache_add_failures: MacroStats
    rocksdb_block_cache_index_miss: MacroStats
    rocksdb_block_cache_index_hit: MacroStats
    rocksdb_block_cache_index_add: MacroStats
    rocksdb_block_cache_index_bytes_insert: MacroStats
    rocksdb_block_cache_index_bytes_evict: MacroStats
    rocksdb_block_cache_filter_miss: MacroStats
    rocksdb_block_cache_filter_hit: MacroStats
    rocksdb_block_cache_filter_add: MacroStats
    rocksdb_block_cache_filter_bytes_insert: MacroStats
    rocksdb_block_cache_filter_bytes_evict: MacroStats
    rocksdb_block_cache_data_miss: MacroStats
    rocksdb_block_cache_data_hit: MacroStats
    rocksdb_block_cache_data_add: MacroStats
    rocksdb_block_cache_data_bytes_insert: MacroStats
    rocksdb_block_cache_bytes_read: MacroStats
    rocksdb_block_cache_bytes_write: MacroStats
    rocksdb_bloom_filter_useful: MacroStats
    rocksdb_bloom_filter_full_positive: MacroStats
    rocksdb_bloom_filter_full_true_positive: MacroStats
    rocksdb_bloom_filter_micros: MacroStats
    rocksdb_persistent_cache_hit: MacroStats
    rocksdb_persistent_cache_miss: MacroStats
    rocksdb_sim_block_cache_hit: MacroStats
    rocksdb_sim_block_cache_miss: MacroStats
    rocksdb_memtable_hit: MacroStats
    rocksdb_memtable_miss: MacroStats
    rocksdb_l0_hit: MacroStats
    rocksdb_l1_hit: MacroStats
    rocksdb_l2andup_hit: MacroStats
    rocksdb_compaction_key_drop_new: MacroStats
    rocksdb_compaction_key_drop_obsolete: MacroStats
    rocksdb_compaction_key_drop_range_del: MacroStats
    rocksdb_compaction_key_drop_user: MacroStats
    rocksdb_compaction_range_del_drop_obsolete: MacroStats
    rocksdb_compaction_optimized_del_drop_obsolete: MacroStats
    rocksdb_compaction_cancelled: MacroStats
    rocksdb_number_keys_written: MacroStats
    rocksdb_number_keys_read: MacroStats
    rocksdb_number_keys_updated: MacroStats
    rocksdb_bytes_written: MacroStats
    rocksdb_bytes_read: MacroStats
    rocksdb_number_db_seek: MacroStats
    rocksdb_number_db_next: MacroStats
    rocksdb_number_db_prev: MacroStats
    rocksdb_number_db_seek_found: MacroStats
    rocksdb_number_db_next_found: MacroStats
    rocksdb_number_db_prev_found: MacroStats
    rocksdb_db_iter_bytes_read: MacroStats
    rocksdb_no_file_closes: MacroStats
    rocksdb_no_file_opens: MacroStats
    rocksdb_no_file_errors: MacroStats
    rocksdb_l0_slowdown_micros: MacroStats
    rocksdb_memtable_compaction_micros: MacroStats
    rocksdb_l0_num_files_stall_micros: MacroStats
    rocksdb_stall_micros: MacroStats
    rocksdb_db_mutex_wait_micros: MacroStats
    rocksdb_rate_limit_delay_millis: MacroStats
    rocksdb_num_iterators: MacroStats
    rocksdb_number_multiget_get: MacroStats
    rocksdb_number_multiget_keys_read: MacroStats
    rocksdb_number_multiget_bytes_read: MacroStats
    rocksdb_number_deletes_filtered: MacroStats
    rocksdb_number_merge_failures: MacroStats
    rocksdb_bloom_filter_prefix_checked: MacroStats
    rocksdb_bloom_filter_prefix_useful: MacroStats
    rocksdb_number_reseeks_iteration: MacroStats
    rocksdb_getupdatessince_calls: MacroStats
    rocksdb_block_cachecompressed_miss: MacroStats
    rocksdb_block_cachecompressed_hit: MacroStats
    rocksdb_block_cachecompressed_add: MacroStats
    rocksdb_block_cachecompressed_add_failures: MacroStats
    rocksdb_wal_synced: MacroStats
    rocksdb_wal_bytes: MacroStats
    rocksdb_write_self: MacroStats
    rocksdb_write_other: MacroStats
    rocksdb_write_timeout: MacroStats
    rocksdb_write_wal: MacroStats
    rocksdb_compact_read_bytes: MacroStats
    rocksdb_compact_write_bytes: MacroStats
    rocksdb_flush_write_bytes: MacroStats
    rocksdb_compact_read_marked_bytes: MacroStats
    rocksdb_compact_read_periodic_bytes: MacroStats
    rocksdb_compact_read_ttl_bytes: MacroStats
    rocksdb_compact_write_marked_bytes: MacroStats
    rocksdb_compact_write_periodic_bytes: MacroStats
    rocksdb_compact_write_ttl_bytes: MacroStats
    rocksdb_number_direct_load_table_properties: MacroStats
    rocksdb_number_superversion_acquires: MacroStats
    rocksdb_number_superversion_releases: MacroStats
    rocksdb_number_superversion_cleanups: MacroStats
    rocksdb_number_block_compressed: MacroStats
    rocksdb_number_block_decompressed: MacroStats
    rocksdb_number_block_not_compressed: MacroStats
    rocksdb_merge_operation_time_nanos: MacroStats
    rocksdb_filter_operation_time_nanos: MacroStats
    rocksdb_row_cache_hit: MacroStats
    rocksdb_row_cache_miss: MacroStats
    rocksdb_read_amp_estimate_useful_bytes: MacroStats
    rocksdb_read_amp_total_read_bytes: MacroStats
    rocksdb_number_rate_limiter_drains: MacroStats
    rocksdb_number_iter_skip: MacroStats
    rocksdb_blobdb_num_put: MacroStats
    rocksdb_blobdb_num_write: MacroStats
    rocksdb_blobdb_num_get: MacroStats
    rocksdb_blobdb_num_multiget: MacroStats
    rocksdb_blobdb_num_seek: MacroStats
    rocksdb_blobdb_num_next: MacroStats
    rocksdb_blobdb_num_prev: MacroStats
    rocksdb_blobdb_num_keys_written: MacroStats
    rocksdb_blobdb_num_keys_read: MacroStats
    rocksdb_blobdb_bytes_written: MacroStats
    rocksdb_blobdb_bytes_read: MacroStats
    rocksdb_blobdb_write_inlined: MacroStats
    rocksdb_blobdb_write_inlined_ttl: MacroStats
    rocksdb_blobdb_write_blob: MacroStats
    rocksdb_blobdb_write_blob_ttl: MacroStats
    rocksdb_blobdb_blob_file_bytes_written: MacroStats
    rocksdb_blobdb_blob_file_bytes_read: MacroStats
    rocksdb_blobdb_blob_file_synced: MacroStats
    rocksdb_blobdb_blob_index_expired_count: MacroStats
    rocksdb_blobdb_blob_index_expired_size: MacroStats
    rocksdb_blobdb_blob_index_evicted_count: MacroStats
    rocksdb_blobdb_blob_index_evicted_size: MacroStats
    rocksdb_blobdb_gc_num_files: MacroStats
    rocksdb_blobdb_gc_num_new_files: MacroStats
    rocksdb_blobdb_gc_failures: MacroStats
    rocksdb_blobdb_gc_num_keys_overwritten: MacroStats
    rocksdb_blobdb_gc_num_keys_expired: MacroStats
    rocksdb_blobdb_gc_num_keys_relocated: MacroStats
    rocksdb_blobdb_gc_bytes_overwritten: MacroStats
    rocksdb_blobdb_gc_bytes_expired: MacroStats
    rocksdb_blobdb_gc_bytes_relocated: MacroStats
    rocksdb_blobdb_fifo_num_files_evicted: MacroStats
    rocksdb_blobdb_fifo_num_keys_evicted: MacroStats
    rocksdb_blobdb_fifo_bytes_evicted: MacroStats
    rocksdb_txn_overhead_mutex_prepare: MacroStats
    rocksdb_txn_overhead_mutex_old_commit_map: MacroStats
    rocksdb_txn_overhead_duplicate_key: MacroStats
    rocksdb_txn_overhead_mutex_snapshot: MacroStats
    rocksdb_txn_get_tryagain: MacroStats
    rocksdb_number_multiget_keys_found: MacroStats
    rocksdb_num_iterator_created: MacroStats
    rocksdb_num_iterator_deleted: MacroStats
    rocksdb_block_cache_compression_dict_miss: MacroStats
    rocksdb_block_cache_compression_dict_hit: MacroStats
    rocksdb_block_cache_compression_dict_add: MacroStats
    rocksdb_block_cache_compression_dict_bytes_insert: MacroStats
    rocksdb_block_cache_compression_dict_bytes_evict: MacroStats
    rocksdb_block_cache_add_redundant: MacroStats
    rocksdb_block_cache_index_add_redundant: MacroStats
    rocksdb_block_cache_filter_add_redundant: MacroStats
    rocksdb_block_cache_data_add_redundant: MacroStats
    rocksdb_block_cache_compression_dict_add_redundant: MacroStats
    rocksdb_files_marked_trash: MacroStats
    rocksdb_files_deleted_immediately: MacroStats
    rocksdb_db_get_micros: MicroStats
    rocksdb_db_write_micros: MicroStats
    rocksdb_compaction_times_micros: MicroStats
    rocksdb_compaction_times_cpu_micros: MicroStats
    rocksdb_subcompaction_setup_times_micros: MicroStats
    rocksdb_table_sync_micros: MicroStats
    rocksdb_compaction_outfile_sync_micros: MicroStats
    rocksdb_wal_file_sync_micros: MicroStats
    rocksdb_manifest_file_sync_micros: MicroStats
    rocksdb_table_open_io_micros: MicroStats
    rocksdb_db_multiget_micros: MicroStats
    rocksdb_read_block_compaction_micros: MicroStats
    rocksdb_read_block_get_micros: MicroStats
    rocksdb_write_raw_block_micros: MicroStats
    rocksdb_l0_slowdown_count: MicroStats
    rocksdb_memtable_compaction_count: MicroStats
    rocksdb_num_files_stall_count: MicroStats
    rocksdb_hard_rate_limit_delay_count: MicroStats
    rocksdb_soft_rate_limit_delay_count: MicroStats
    rocksdb_numfiles_in_singlecompaction: MicroStats
    rocksdb_db_seek_micros: MicroStats
    rocksdb_db_write_stall: MicroStats
    rocksdb_sst_read_micros: MicroStats
    rocksdb_num_subcompactions_scheduled: MicroStats
    rocksdb_bytes_per_read: MicroStats
    rocksdb_bytes_per_write: MicroStats
    rocksdb_bytes_per_multiget: MicroStats
    rocksdb_bytes_compressed: MicroStats
    rocksdb_bytes_decompressed: MicroStats
    rocksdb_compression_times_nanos: MicroStats
    rocksdb_decompression_times_nanos: MicroStats
    rocksdb_read_num_merge_operands: MicroStats
    rocksdb_blobdb_key_size: MicroStats
    rocksdb_blobdb_value_size: MicroStats
    rocksdb_blobdb_write_micros: MicroStats
    rocksdb_blobdb_get_micros: MicroStats
    rocksdb_blobdb_multiget_micros: MicroStats
    rocksdb_blobdb_seek_micros: MicroStats
    rocksdb_blobdb_next_micros: MicroStats
    rocksdb_blobdb_prev_micros: MicroStats
    rocksdb_blobdb_blob_file_write_micros: MicroStats
    rocksdb_blobdb_blob_file_read_micros: MicroStats
    rocksdb_blobdb_blob_file_sync_micros: MicroStats
    rocksdb_blobdb_gc_micros: MicroStats
    rocksdb_blobdb_compression_micros: MicroStats
    rocksdb_blobdb_decompression_micros: MicroStats
    rocksdb_db_flush_micros: MicroStats
    rocksdb_sst_batch_size: MicroStats
    rocksdb_num_index_and_filter_blocks_read_per_level: MicroStats
    rocksdb_num_data_blocks_read_per_level: MicroStats
    rocksdb_num_sst_read_per_level: MicroStats
