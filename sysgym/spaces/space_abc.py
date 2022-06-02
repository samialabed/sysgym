import json
from abc import ABC, abstractmethod
from typing import Callable, Dict, Generic, Optional, Tuple, TypeVar, Union

import numpy as np

SUPPORTED_TYPES = TypeVar("SUPPORTED_TYPES", int, bool, float, str)  # container types


class ParameterSpace(ABC, Generic[SUPPORTED_TYPES]):
    # TODO: is name needed?
    __slots__ = ["__name", "__lower_bound", "__upper_bound", "__default", "formula"]

    def __init__(
        self,
        name: str,
        lower_bound: SUPPORTED_TYPES,
        upper_bound: SUPPORTED_TYPES,
        default: Optional[SUPPORTED_TYPES] = None,
        formula: Callable = lambda x: x,
    ):
        self.__name = name
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__default = default
        self.formula = formula

        assert (
            self.lower_bound < self.upper_bound
        ), f"Lower bound {self.lower_bound} >= upper bound: {self.upper_bound}"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def bounds(self) -> Tuple[int, int]:
        return self.lower_bound, self.upper_bound

    @property
    def scaled_bounds(self) -> Tuple[int, int]:
        return self.formula(self.lower_bound), self.formula(self.upper_bound)

    @property
    def default(self) -> SUPPORTED_TYPES:
        return self.__default

    @property
    def lower_bound(self) -> int:
        return self.__lower_bound

    @property
    def upper_bound(self) -> int:
        return self.__upper_bound

    @property
    def is_categorical(self):
        return not self.is_numeric and self.is_discrete

    def search_space(self) -> int:
        """Assume discrete search size - inaccurate for continuous vars"""
        return len(np.arange(self.lower_bound, self.upper_bound + 1))

    def dict_repr(self) -> Dict[str, Union[str, int]]:
        return {
            "name": self.name,
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound,
        }

    @abstractmethod
    def sample(self, num: int = 1, seed: int = None) -> np.ndarray:
        """Sample the bounded space and return random number in it."""

    @abstractmethod
    def transform(self, x):
        """Transform X to be a ParameterSpace"""

    @abstractmethod
    def inverse_transform(self, x):
        """Transform X to be a SystemParameter"""

    def __contains__(self, value: SUPPORTED_TYPES):
        """Check if value in bounds."""
        return self.lower_bound <= value <= self.upper_bound

    def __repr__(self) -> str:
        properties = ", ".join(
            [
                str(self.name),
                str(self.lower_bound),
                str(self.upper_bound),
            ]
        )
        return f"{type(self)}:({properties})"

    def __str__(self) -> str:
        return "".join(
            [
                f"{type(self)}: "
                f"(name: {self.name},"
                f"lower_bound: {self.lower_bound},"
                f"upper_bound:{self.upper_bound},"
            ]
        )

    def as_json(self) -> str:
        return json.dumps(self.dict_repr())
