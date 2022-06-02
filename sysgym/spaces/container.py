from typing import Generic

import numpy as np

from sysgym.spaces.space_abc import SUPPORTED_TYPES, ParameterSpace


class ParameterContainer(Generic[SUPPORTED_TYPES]):
    def __init__(self, space: ParameterSpace):
        self.__space = space
        self.__value = space.default

    def as_numpy(self) -> np.ndarray:
        pass

    def as_sys(self) -> SUPPORTED_TYPES:
        pass

    def from_numpy(self, x: np.ndarray):
        self.value = self.__space.inverse_transform(x)

    @property
    def value(self) -> SUPPORTED_TYPES:
        return self.__value

    def reset(self):
        self.value = self.__space.default

    @value.setter
    def value(self, value: SUPPORTED_TYPES):
        if value in self.__space:
            self.__value = value
        else:
            raise ValueError(
                f"Value ({value}) being set outside the bounds({self.__space.bounds})"
            )

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self) -> str:
        return f"Value: {self.value} of the parameter space: {self.__space}"
