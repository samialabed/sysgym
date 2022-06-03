from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Dict, Iterator, List, NamedTuple, Tuple

import numpy as np

from sysgym.params.boxes import ParamBox


class ParameterInfo(NamedTuple):
    name: str
    box: ParamBox


@dataclass(frozen=True)
class ParamsSpace(Mapping):
    """Class that contains the space (bounds) of the parameters to be tuned."""

    @property
    def dimensions(self) -> int:
        return len(fields(self))

    def __post_init__(self):
        # TODO(global context): add check here to only evaluate paramspace when debug on
        for field in fields(self):
            # Ensure all members subclass ParamBox
            assert issubclass(
                field.type, ParamBox
            ), f"{field.name} does not subclass ParamBox."

    def parameters(self) -> List[ParameterInfo]:
        params = []
        for field in fields(self):
            param_name = field.name
            param_box: ParamBox = getattr(self, param_name)
            params.append(ParameterInfo(name=param_name, box=param_box))
        return params

    def sample(self, num: int = 1, seed: int = None) -> np.ndarray:
        """Sample all parameters within their bounds."""
        vals = []
        for field in fields(self):
            field_val: ParamBox = getattr(self, field.name)
            vals.append(field_val.sample(num=num, seed=seed))
        return np.array(vals)

    def to_latex(self) -> np.ndarray:
        """Return a np.ndarray containing tuples of lower and upper bounds."""
        bounds: List[List[str, int, int]] = []  # list of lower, upper bounds
        for field in fields(self):
            param_space: ParamBox = getattr(self, field.name)
            lower, upper = param_space.scaled_bounds
            param_name = field.name
            bounds.append([param_name, lower, upper])
        return np.array(bounds)

    def bounds(self, use_formula: bool = False) -> np.ndarray:
        """Return a ndarray containing tuples of lower and upper bounds."""
        bounds: List[Tuple[int, int]] = []  # list of lower, upper bounds
        for field in fields(self):
            param_space: ParamBox = getattr(self, field.name)
            if use_formula:
                param_bounds = param_space.scaled_bounds
            else:
                param_bounds = param_space.bounds
            bounds.append(param_bounds)
        return np.array(bounds)

    def dict_to_numpy(self, params: Dict[str, any]) -> np.ndarray:
        """Transform potential system configuration to numpy."""
        res = []
        for field in fields(self):
            param_name = field.name
            param_val = params[param_name]
            param_space: ParamBox = getattr(self, param_name)
            res.append(param_space.transform(param_val))
        return np.array(res)

    def numpy_to_dict(self, values: np.ndarray) -> Dict[str, any]:
        """Transform potential X to dictionary system compatible."""
        values = values.squeeze().tolist()
        res = {}
        for (field, numpy_values) in zip(fields(self), values):
            param_space: ParamBox = getattr(self, field.name)
            res[field.name] = param_space.from_numpy(numpy_values)
        return res

    @staticmethod
    def spaces_to_json(spaces: Dict[str, ParamBox]) -> List[Dict]:
        """Used to convert the held spaces to json for dataclasses."""
        all_params = []
        for (param_name, param_space) in spaces.items():
            all_params.append({param_name: param_space.dict_repr()})
        # return json.dumps(all_params)
        return all_params

    def number_of_choices(self) -> int:
        search_sizes = []
        for field in fields(self):
            field_val: ParamBox = getattr(self, field.name)
            print(f"{field.name}: Search size is: {field_val.search_space()}")
            print(
                f"{field.name}: Search space is: "
                f"{np.arange(field_val.lower_bound, field_val.upper_bound+1)}"
            )
            search_sizes.append(field_val.search_space())
        return np.product(search_sizes)

    def __getitem__(self, param_name: str) -> ParamBox:
        field_val: ParamBox = getattr(self, param_name)
        return field_val

    def __setitem__(self, param_name: str, value):
        field_val: ParamBox = getattr(self, param_name)
        field_val.value = value

    def __len__(self) -> int:
        return len(fields(self))

    def __iter__(self) -> Iterator[Dict[str, ParamBox]]:
        return iter({f.name: getattr(self, f.name) for f in fields(self)})
