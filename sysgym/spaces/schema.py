from abc import ABC
from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Dict, Iterator, List, Tuple, Union

import numpy as np

from sysgym.spaces.space_abc import ParameterSpace

PARAMS_SUPPORTED_TYPE = Union[float, int, bool, str]


@dataclass(frozen=True)
class ParamSchema(ABC, Mapping):
    """Class that contains the schema (bounds) of the parameters to be tuned."""

    @property
    def dimensions(self) -> int:
        return len(fields(self))

    def __post_init__(self):
        # TODO: once add global context add check here to only work when debug on
        all_params = fields(self)
        for f in all_params:
            # Ensure all members subclass ParameterSpace
            assert issubclass(
                f.type, ParameterSpace
            ), f" {f.name} does not subclass ParameterSpace."

    def parameters(self) -> List[ParameterSpace]:
        params = []
        for f in fields(self):
            param_space: ParameterSpace = getattr(self, f.name)
            params.append(param_space)
        return params

    def sample(self, num: int = 1, seed: np.random.RandomState = None) -> np.ndarray:
        """Sample all parameters within their bounds."""
        vals = []
        for f in fields(self):
            field_val: ParameterSpace = getattr(self, f.name)
            vals.append(field_val.sample(num=num, seed=seed))
        return np.array(vals)

    def to_latex(self) -> np.ndarray:
        """Return a ndarry containing tuples of lower and upper bounds."""
        bounds: List[List[str, int, int]] = []  # list of lower, upper bounds
        for f in fields(self):
            param_space: ParameterSpace = getattr(self, f.name)
            lower, upper = param_space.scaled_bounds
            param_name = param_space.name
            bounds.append([param_name, lower, upper])
        return np.array(bounds)

    def bounds(self, use_formula: bool = False) -> np.ndarray:
        """Return a ndarry containing tuples of lower and upper bounds."""
        bounds: List[Tuple[int, int]] = []  # list of lower, upper bounds
        for f in fields(self):
            param_space: ParameterSpace = getattr(self, f.name)
            if use_formula:
                param_bounds = param_space.scaled_bounds
            else:
                param_bounds = param_space.bounds
            bounds.append(param_bounds)
        return np.array(bounds)

    def dict_to_numpy(self, params: Dict[str, PARAMS_SUPPORTED_TYPE]) -> np.ndarray:
        """Transform potential system configuration to numpy."""
        res = []
        for f in fields(self):
            key = f.name
            param_val = params[key]
            param_space: ParameterSpace = getattr(self, key)
            res.append(param_space.transform(param_val))
        return np.array(res)

    def numpy_to_dict(self, Xs: np.ndarray) -> Dict[str, PARAMS_SUPPORTED_TYPE]:
        """Transform potential X to dictionary system compatible."""
        Xs = Xs.squeeze().tolist()
        res = {}
        for (f, x) in zip(fields(self), Xs):
            param_space: ParameterSpace = getattr(self, f.name)
            res[param_space.name] = param_space.inverse_transform(x)
        return res

    @staticmethod
    def spaces_to_json(spaces: Dict[str, ParameterSpace]) -> List[dict]:
        """Used to convert the held spaces to json for dataclasses."""
        all_params = []
        for param in spaces.values():
            all_params.append(param.dict_repr())
        # return json.dumps(all_params)
        return all_params

    def number_of_choices(self) -> int:
        search_sizes = []
        for f in fields(self):
            field_val: ParameterSpace = getattr(self, f.name)
            print(f"{f.name}: Search size is: {field_val.search_space()}")
            print(
                f"{f.name}: Search space is: "
                f"{np.arange(field_val.lower_bound, field_val.upper_bound+1)}"
            )
            search_sizes.append(field_val.search_space())
        return np.product(search_sizes)

    def __getitem__(self, param_name: str) -> ParameterSpace:
        field_val: ParameterSpace = getattr(self, param_name)
        return field_val

    def __len__(self) -> int:
        return len(fields(self))

    def __iter__(self) -> Iterator[Dict[str, ParameterSpace]]:
        return iter({f.name: getattr(self, f.name) for f in fields(self)})
