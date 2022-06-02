import numpy as np

from sysgym.boxes.box import ParameterBox


class ContinuousBox(ParameterBox[float]):
    def sample(self, num=1, seed: int = None) -> np.ndarray:
        assert num > 0
        if seed:
            seeded = np.random.RandomState(seed)
            return seeded.uniform(self.lower_bound, self.upper_bound, num)
        return np.random.uniform(self.lower_bound, self.upper_bound, num)

    def transform(self, x: float) -> float:
        return x

    def inverse_transform(self, x: float) -> float:
        return x

    def __contains__(self, value: float):
        """Check if value in bounds."""
        error_tolerance = (
            0.001  # hacky way to allow tolerance of floating point operations
        )
        return (
            self.lower_bound - error_tolerance
            <= value
            <= (self.upper_bound + error_tolerance)
        )
