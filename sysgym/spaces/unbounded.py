from typing import Dict, Optional

from sysgym.spaces.space_abc import ParameterSpace


class UnboundedSpace(ParameterSpace):
    def __init__(self, name: str, default: Optional[any] = None):
        super().__init__(
            name=name,
            lower_bound=float("-inf"),
            upper_bound=float("inf"),
            default=default,
        )

    def sample(self, num: int = 1, seed: int = None):
        return self.default

    def dict_repr(self) -> Dict:
        return {
            "name": self.name,
            "value": self.default,
        }

    def transform(self, x):
        return x

    def inverse_transform(self, x):
        return x


def print_dict_unbounded_space(d: Dict) -> None:
    """Helper method to get parmascheme of unbounded space quickly"""
    # TODO: sorta a hack around using env_dict everywhere
    for (param, value) in d.items():
        print(
            f"{param}: UnboundedSpace = UnboundedSpace(name='{param}', default={value})"
        )
