import json
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from typing import Iterator, List

import numpy as np

from sysgym.spaces.container import ParameterContainer
from sysgym.spaces.schema import PARAMS_SUPPORTED_TYPE, ParamSchema

# TODO: I don't like this one


class EnvParamsDict(ABC, MutableMapping):
    """Class acting as dictionary that enforces the
    values stored in it to confront to the defined schema"""

    def __init__(self, schema: ParamSchema):
        self.__container = {}
        self._schema = schema

        for param_space in schema.parameters():
            self.__container[param_space.name] = ParameterContainer(space=param_space)

    def to_json(self) -> str:
        """Return json representation of the values stored."""
        return json.dumps(dict(self))

    def update_from_numpy(self, Xs: np.ndarray) -> None:
        """Create EnvParams values from numpy."""
        Xs = Xs.squeeze().tolist()
        for (param, x) in zip(self.__container, Xs):
            self.__container[param].from_numpy(x)

    def reset(self) -> None:
        """Reset all values held in this container to default"""
        for value in self.__container.values():
            value.reset()

    def as_numpy(self) -> np.ndarray:
        """Return the stored value as numpy."""
        res = list(self.values())
        return np.array(res)

    @abstractmethod
    def as_sys(self) -> List[str]:
        pass

    def __setitem__(self, k: str, v: PARAMS_SUPPORTED_TYPE) -> None:
        """Set a parameter to the value specified."""
        try:
            self.__container[k].value = v
        except KeyError:
            raise KeyError(f"{k} is not a parameter in {list(self)}")

    def __delitem__(self, k: str) -> None:
        """Reset a value to its default."""
        try:
            parameter = self.__container[k]
            parameter.reset()
        except KeyError:
            raise KeyError(f"{k} is not a parameter in {list(self)}")

    def __getitem__(self, k: str) -> PARAMS_SUPPORTED_TYPE:
        """Retrieve the stored value in the parameter container."""
        try:
            return self._schema[k].formula(self.__container[k].value)
        except KeyError:
            raise KeyError(f"{k} is not a parameter in {list(self)}")

    def __len__(self) -> int:
        """Number of dimensions/parameters in this container."""
        return len(self.__container)

    def __iter__(self) -> Iterator[str]:
        """Iterator over the stored key values."""
        return iter(self.__container)

    def __repr__(self):
        return repr(self.__container)

    def __str__(self):
        return str(self.as_sys())
