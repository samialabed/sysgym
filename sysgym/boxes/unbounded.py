from typing import Dict, Optional

from sysgym.boxes.box import ParameterBox


class UnboundedBox(ParameterBox):
    def __init__(self, default: Optional[any] = None):
        super().__init__(
            lower_bound=float("-inf"),
            upper_bound=float("inf"),
            default=default,
        )

    def sample(self, num: int = 1, seed: int = None):
        return self.default

    def dict_repr(self) -> Dict:
        return {"value": self.default}

    def transform(self, x):
        return x

    def inverse_transform(self, x):
        return x
