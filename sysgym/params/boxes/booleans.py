from typing import Dict, List, Optional, Union

import numpy as np
from numpy.random import RandomState

from sysgym.params.boxes.box import ParamBox


class BooleanBox(ParamBox[bool]):
    def __init__(self, default: Optional[bool] = None):
        super().__init__(lower_bound=0, upper_bound=1, default=default)

    def sample(self, num: int = 1, seed: int = None) -> np.ndarray:
        assert num > 0
        if seed:
            return RandomState(seed).choice([True, False], num, replace=True)
        return np.random.choice([True, False], num, replace=True)

    def dict_repr(self) -> Dict[str, Union[str, List[bool]]]:
        return {
            "categories": [True, False],
        }

    def transform(self, x: bool) -> float:
        """Return 0 for False and 1 for True."""
        return float(x)

    def from_numpy(self, x: float) -> bool:
        """Assign True to floats over 0.5"""
        return x > 0.5
