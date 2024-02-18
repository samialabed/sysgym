from typing import Callable

import numpy as np
from numpy.random import RandomState

from sysgym.params.boxes.box import ParamBox


class DiscreteBox(ParamBox[int]):
    def __init__(
        self,
        lower_bound: int,
        upper_bound: int,
        default: int = None,
        formula: Callable = lambda x: x,
    ):
        """
        Args:
            formula: Optional formula that applies at inverse transformation.
             Allows expressing log/power transformation and halving search space.
        """
        super().__init__(
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            default=default,
            formula=formula,
        )
        self.formula = formula

    def sample(self, num=1, seed: int = None) -> np.ndarray:
        assert num > 0
        lb = round(self.lower_bound)
        ub = round(self.upper_bound)
        if seed:
            return RandomState(seed).randint(lb, ub + 1, num)
        return np.random.randint(lb, ub + 1, num)

    def transform(self, x: int) -> float:
        return float(x)

    def from_numpy(self, x: np.ndarray) -> int:
        x = int(x.round())
        return x
