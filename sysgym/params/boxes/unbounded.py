from typing import Dict, Optional

from sysgym.params.boxes.box import ParamBox


class UnboundedBox(ParamBox):
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

    def from_numpy(self, x):
        return x
