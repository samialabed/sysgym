from typing import Dict, List, Optional, Union

import numpy as np

from sysgym.spaces.space_abc import ParameterSpace


class BooleanSpace(ParameterSpace[bool]):
    def __init__(self, name: str, default: Optional[bool] = None):
        super().__init__(name=name, lower_bound=0, upper_bound=1, default=default)

    def sample(self, num: int = 1, seed: int = None) -> np.ndarray:
        assert num > 0
        if seed:
            seeded = np.random.RandomState(seed)
            return seeded.choice([True, False], num, replace=True)
        return np.random.choice([True, False], num, replace=True)

    def dict_repr(self) -> Dict[str, Union[str, List[bool]]]:
        return {
            "name": self.name,
            "categories": [True, False],
        }

    def transform(self, x: bool) -> float:
        """Return 0 for False and 1 for True."""
        return float(x)

    def inverse_transform(self, x: float) -> bool:
        """Assign True to floats over 0.5"""
        return x > 0.5
