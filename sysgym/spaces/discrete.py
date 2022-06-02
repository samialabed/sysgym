from typing import Callable

import numpy as np

from sysgym.spaces.space_abc import ParameterSpace


class DiscreteSpace(ParameterSpace[int]):
    def __init__(
        self,
        name: str,
        lower_bound: int,
        upper_bound: int,
        default: int = None,
        formula: Callable = lambda x: x,
    ):
        """

        Args:
            name:
            lower_bound:
            upper_bound:
            formula: Optional formula that applies at inverse transformation.
             Allows expressing log/power transformation and halving search space.
        """
        super().__init__(
            name=name,
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
            return np.random.RandomState(seed).randint(lb, ub + 1, num)
        return np.random.randint(lb, ub + 1, num)

    def transform(self, x: int) -> float:
        return float(x)

    def inverse_transform(self, x: float) -> int:
        x = int(round(x))
        return x

    # def numpy_to_dict(self, x: float) -> int:
    #     x = int(round(x))
    #     if self.formula:
    #         x = self.formula(x)
    #     return x
    #
    # def __contains__(self, value: int) -> bool:
    #     """ Check if value in bounds."""
    #     if self.formula:
    #         return (
    #             self.formula(self.lower_bound)
    #             <= value
    #             <= self.formula(self.upper_bound)
    #         )
    #
    #     return self.lower_bound <= value <= self.upper_bound
