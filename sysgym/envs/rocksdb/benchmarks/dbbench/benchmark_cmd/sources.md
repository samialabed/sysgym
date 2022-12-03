# Workload flags sources

## Point Lookup
**File: point_lookup_(10k/80k)_(load/run).txt**

In this test, whole key is indexed for fast point lookup (i.e. prefix_extractor = NewFixedPrefixTransform(20)). When using this setup, range query is not supported. It provides maximum throughput for point lookup queries.

* [Source](https://github.com/facebook/rocksdb/wiki/RocksDB-In-Memory-Workload-Performance-Benchmarks#test-1-point-lookup)


## Prefix Range Query
**File: **previx_range_query_(10k/80k)_(load/run).txt

In this test, a key prefix size of 12 bytes is indexed (i.e. prefix_extractor = NewFixedPrefixTransform(12)). db_bench is configured to generate approximately 10 keys per unique prefix. In this setting, Seek() can be performed within a given prefix as well as iteration on the returned iterator. However, behavior of scanning beyond the prefix boundary is not defined. This is a fairly common access pattern for graph data. Point lookup throughput is measured under this setting:

* [Source](https://github.com/facebook/rocksdb/wiki/RocksDB-In-Memory-Workload-Performance-Benchmarks#test-2-prefix-range-query)

## writes.txt
This came from the Pipelined Versioning benchmark. [GitHub](https://github.com/facebook/rocksdb/wiki/Pipelined-Write), their results in [Gist](https://gist.github.com/yiwu-arbug/3b5a5727e52f1e58d1c10f2b80cec05d)

## read_modify_write.txt 
The goal of these benchmarks is to demonstrate the benefit of Merge operators on read-modify-write workloads, e.g. counters. Both benchmarks were executed using a single thread.

Using merge operator, we are able to perform read-modify-write using only one operator. In this benchmark, we performed 50.000.000 iterations of:

* Execute "uint64add" merge operator on a random key, which adds 1 to the value associated with the key

As in previous benchmark, each value was 8 bytes and Write Ahead Log was turned off.

Here are the exact benchmark parameters we used:

[Source](https://github.com/facebook/rocksdb/wiki/Read-Modify-Write-Benchmarks)
