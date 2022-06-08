import json
from abc import ABC, abstractmethod
from typing import Callable, Dict, Generic, Optional, Tuple, TypeVar, Union

import numpy as np

SUPPORTED_TYPES = TypeVar("SUPPORTED_TYPES", int, bool, float, str)  # container types


class ParamBox(ABC, Generic[SUPPORTED_TYPES]):
    """
    Box that contains the parameter and stores it.
    It ensures the value stored in the box adheres to the bounds provided.

    """

    def __init__(
        self,
        lower_bound: SUPPORTED_TYPES,
        upper_bound: SUPPORTED_TYPES,
        default: Optional[SUPPORTED_TYPES] = None,
        formula: Callable = lambda x: x,
    ):
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__default = default
        self.formula = formula
        self._value = default

        assert (
            self.lower_bound < self.upper_bound
        ), f"Lower bound {self.lower_bound} >= upper bound: {self.upper_bound}"

    @property
    def value(self) -> SUPPORTED_TYPES:
        """Stored value inside the box, scale it back when surfaced"""
        return self.formula(self._value)

    def reset(self):
        """Reset the parameter to its default value."""
        self.value = self.default

    @value.setter
    def value(self, new_val: SUPPORTED_TYPES):
        """(unscaled) value is used"""
        if new_val in self:  # is in the bounds
            self._value = new_val
        else:
            raise ValueError(
                f"Value ({new_val}) being set outside the bounds({self.bounds})"
            )

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

    def search_space(self) -> int:
        """Assume discrete search size - inaccurate for continuous vars"""
        return len(np.arange(self.lower_bound, self.upper_bound + 1))

    def dict_repr(self) -> Dict[str, Union[str, int]]:
        return {
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound,
        }

    @abstractmethod
    def sample(self, num: int = 1, seed: int = None) -> np.ndarray:
        """Sample the bounded space and return random number in it."""

    @abstractmethod
    def transform(self, x):
        """Transform X to be a ParameterBox"""

    @abstractmethod
    def from_numpy(self, x: np.ndarray):
        """Transform X to be a SystemParameter"""

    def __contains__(self, value: SUPPORTED_TYPES):
        """Check if value in bounds."""
        return self.lower_bound <= value <= self.upper_bound

    def __repr__(self) -> str:
        properties = ", ".join(
            [
                f"lower_bound:{str(self.lower_bound)}",
                f"upper_bound:{str(self.upper_bound)}",
                f"value: {str(self.value)}",
            ]
        )
        return f"{type(self)}:({properties})"

    def __str__(self) -> str:
        return "".join(
            [
                f"{type(self)}: "
                f"lower_bound: {self.lower_bound},"
                f"upper_bound:{self.upper_bound},"
                f"stored_value:{self.value}"
            ]
        )

    def as_json(self) -> str:
        return json.dumps(self.dict_repr())
