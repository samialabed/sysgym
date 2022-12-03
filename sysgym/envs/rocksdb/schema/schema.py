from abc import ABC
from dataclasses import dataclass

from sysgym.params import ParamsSpace


@dataclass(init=False, frozen=True)
class RocksDBParamSchema(ParamsSpace, ABC):
    """Interface to allow versioning of rocksdb params."""

    pass
