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

    def __init__(self, param_space: ParamsSpace):
        self._container: Dict[str, ParamBox] = {}
        for parameter_info in param_space.parameters():
            self._container[parameter_info.name] = parameter_info.box

    def to_json(self) -> str:
        """Return json representation of the values stored."""
        return json.dumps(dict(self))

    def update_from_numpy(self, values: np.ndarray) -> None:
        """Create EnvParams values from numpy."""
        values = values.squeeze().tolist()
        for (param, numpy_val) in zip(self._container, values):
            self._container[param].from_numpy(numpy_val)

    def reset(self) -> None:
        """Reset all values held in this container to default"""
        for param_box in self._container.values():
            param_box.reset()

    def as_numpy(self) -> np.ndarray:
        """Return the stored value as numpy."""
        res = list(self.values())
        return np.array(res)

    def __setitem__(self, k: str, v: any) -> None:
        """Set a parameter to the value specified."""
        try:
            self._container[k].value = v
        except KeyError as exc:
            raise KeyError(f"{k} is not a parameter in {list(self)}") from exc

    def __delitem__(self, k: str) -> None:
        """Reset a value to its default."""
        try:
            parameter = self._container[k]
            parameter.reset()
        except KeyError as exc:
            raise KeyError(f"{k} is not a parameter in {list(self)}") from exc

    def __getitem__(self, k: str) -> any:
        """Retrieve the stored value in the parameter box."""
        try:
            return self._container[k].value
        except KeyError as exc:
            raise KeyError(f"{k} is not a parameter in {list(self)}") from exc

    def __len__(self) -> int:
        """Number of dimensions/parameters in this container."""
        return len(self._container)

    def __iter__(self) -> Iterator[str]:
        """Iterator over the stored key values."""
        return iter(self._container)

    def __repr__(self):
        return repr(self._container)
