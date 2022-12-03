from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from sysgym.envs.rocksdb.benchmarks.dbbench.dbbench_settings import DBBenchSettings


@dataclass_json
@dataclass(frozen=True)
class MixGraphDBBenchOptions(DBBenchSettings):
    keyrange_dist_a: Optional[float] = None
    keyrange_dist_b: Optional[float] = None
    keyrange_dist_c: Optional[float] = None
    keyrange_dist_d: Optional[float] = None
    keyrange_num: Optional[float] = None
    value_k: Optional[float] = None
    value_sigma: Optional[float] = None
    iter_k: Optional[float] = None
    iter_sigma: Optional[float] = None
    mix_get_ratio: Optional[float] = None
    mix_put_ratio: Optional[float] = None
    mix_seek_ratio: Optional[float] = None
    sine_mix_rate_interval_milliseconds: Optional[float] = None
    sine_a: Optional[float] = None
    sine_b: Optional[float] = None
    sine_d: Optional[float] = None
