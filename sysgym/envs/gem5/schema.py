from abc import ABC
from dataclasses import dataclass

from sysgym.spaces.schema import ParamSchema


@dataclass(init=False, frozen=True)
class Gem5ParamSchema(ParamSchema, ABC):
    """Interface to allow versioning of Gem5 params."""

    pass
