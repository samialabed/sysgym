from typing import Dict, List, Optional, Union

import numpy as np
from sklearn.preprocessing import LabelEncoder

from sysgym.boxes.box import ParameterBox


class CategoricalBox(ParameterBox[str]):
    def __init__(self, categories: List[str], default: Optional[str] = None):
        self.categories = categories
        num_cats = len(self.categories)
        super().__init__(
            lower_bound=0,
            upper_bound=num_cats,
            default=default,
            formula=lambda x: x,
        )
        assert num_cats > 0, "Expected Categories to be more than > 0."
        assert len(set(self.categories)) == num_cats, "Detected duplicate categories"
        self.__encoder = LabelEncoder()
        self.__encoder.fit(self.categories)

    def dict_repr(self) -> Dict[str, Union[str, List[str]]]:
        return {
            "categories": self.categories,
        }

    def sample(self, num=1, seed: int = None) -> np.ndarray:
        assert num > 0
        if seed:
            seeded = np.random.RandomState(seed)
            samples = seeded.randint(self.lower_bound, self.upper_bound + 1, num)
        else:
            samples = np.random.randint(self.lower_bound, self.upper_bound + 1, num)

        return self.inverse_transform(samples)

    def transform(self, x: np.ndarray) -> np.ndarray:
        return self.__encoder.transform(x.astype(str).reshape(-1))

    def inverse_transform(self, x: np.ndarray):
        return self.__encoder.inverse_transform(x.round().astype(int).reshape(-1))
