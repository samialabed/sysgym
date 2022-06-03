import json
from collections.abc import MutableMapping
from typing import Dict, Iterator

import numpy as np

from sysgym.params import ParamsSpace
from sysgym.params.boxes import ParamBox


class EnvParamsDict(MutableMapping):
    """Class acting as dictionary that enforces the
    values stored in it to confront to the defined schema.
    Allows updating from numpy, to numpy, storing to disk, and other helpful utils.
    """

    def __init__(self, params_space: ParamsSpace):
        self._container: Dict[str, ParamBox] = {}
        self._schema = params_space
        for parameter_info in params_space.parameters():
            self._container[parameter_info.name] = parameter_info.box

    def to_json(self) -> str:
        """Return json representation of the values stored."""
        return json.dumps(dict(self))

    def update_from_numpy(self, values: np.ndarray) -> None:
        """Create EnvParams values from numpy."""
        values = values.squeeze().tolist()
        for (param, x) in zip(self._container, values):
            self._container[param].from_numpy(x)

    def reset(self) -> None:
        """Reset all values held in this container to default"""
        for value in self._container.values():
            value.reset()

    def as_numpy(self) -> np.ndarray:
        """Return the stored value as numpy."""
        res = list(self.values())
        return np.array(res)

    def __setitem__(self, k: str, v: any) -> None:
        """Set a parameter to the value specified."""
        try:
            self._container[k].value = v
        except KeyError:
            raise KeyError(f"{k} is not a parameter in {list(self)}")

    def __delitem__(self, k: str) -> None:
        """Reset a value to its default."""
        try:
            parameter = self._container[k]
            parameter.reset()
        except KeyError:
            raise KeyError(f"{k} is not a parameter in {list(self)}")

    def __getitem__(self, k: str) -> any:
        """Retrieve the stored value in the parameter container."""
        try:
            return self._schema[k].formula(self._container[k].value)
        except KeyError:
            raise KeyError(f"{k} is not a parameter in {list(self)}")

    def __len__(self) -> int:
        """Number of dimensions/parameters in this container."""
        return len(self._container)

    def __iter__(self) -> Iterator[str]:
        """Iterator over the stored key values."""
        return iter(self._container)

    def __repr__(self):
        return repr(self._container)
