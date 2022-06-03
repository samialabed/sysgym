import unittest
from typing import Callable, Dict, NamedTuple

from parameterized import parameterized

from sysgym.wrappers import repeat_env_wrapper


class MovingAverageTestInput(NamedTuple):
    name: str
    prev_val: float
    new_val: float
    n: int
    expected: float


class MapNestedDictTestInput(NamedTuple):
    name: str
    existing_map: Dict
    func: Callable
    func_input: Dict
    expected_output: Dict


class TestMapFunctionToNestedMap(unittest.TestCase):
    @parameterized.expand(
        [
            MapNestedDictTestInput(
                name="Expect to maintain structure and visit all nodes.",
                existing_map={},
                func=lambda _, __: "Visited",
                func_input={
                    "Sad": 4.0,
                    "Family": {
                        "Raad": 2,
                        "Blue": None,
                        "Children": {"Ham": 1.0, "Me": 2},
                    },
                },
                expected_output={
                    "Sad": "Visited",
                    "Family": {
                        "Raad": "Visited",
                        "Blue": "Visited",
                        "Children": {"Ham": "Visited", "Me": "Visited"},
                    },
                },
            ),
            MapNestedDictTestInput(
                name="Expect to apply function and average result",
                existing_map={
                    "Sad": 6.0,
                    "Family": {
                        "Raad": None,
                        "Blue": 2.0,
                        "Children": {"Ham": 2.0, "Me": 2},
                    },
                },
                func=lambda prev_val, new_val: repeat_env_wrapper.moving_avg_func(
                    prev_val, new_val, n=2
                ),
                func_input={
                    "Sad": 4.0,
                    "Family": {
                        "Raad": 2,
                        "Blue": None,
                        "Children": {"Ham": 1.0, "Me": 2},
                    },
                },
                expected_output={
                    "Sad": 5.0,
                    "Family": {
                        "Raad": 1.0,
                        "Blue": 1.0,
                        "Children": {"Ham": 1.5, "Me": 2.0},
                    },
                },
            ),
        ]
    )
    def test_dictionary_structure_is_preserved(
        self,
        name: str,
        existing_map: Dict,
        func: Callable,
        func_input: Dict,
        expected_output: Dict,
    ):
        repeat_env_wrapper.map_nested_dicts_modify(
            mutable_ob=existing_map, new_observations=func_input, func=func
        )
        self.assertEqual(
            expected_output,
            existing_map,
            f"failed test {name} expected {expected_output}, actual {existing_map}",
        )


class TestMovingAverage(unittest.TestCase):
    @parameterized.expand(
        [
            MovingAverageTestInput(
                name="Simple average of (3+1)/2",
                prev_val=3,
                new_val=1,
                n=2,
                expected=2.0,
            ),
            MovingAverageTestInput(
                name="Complicated average of ((3+1)/2 + 5)/3. i.e. 3+1+5/3",
                prev_val=2.0,
                new_val=5,
                n=3,
                expected=3.0,  # (average of 3 + 1)/2
            ),
            MovingAverageTestInput(
                name="Handle missing value average of ((3+1)/2 + None)/3. i.e. 3+1+0/3",
                prev_val=2.0,
                new_val=None,
                n=3,
                expected=1.3333333333333333,  # (average of 3 + 1+0)/3
            ),
        ]
    )
    def test_moving_average_calculating_avg(
        self, name: str, prev_val: float, new_val: float, n: int, expected: float
    ):
        actual = repeat_env_wrapper.moving_avg_func(
            prev_avg=prev_val, new_val=new_val, n=n
        )
        self.assertEqual(
            expected,
            actual,
            f"failed test {name} expected {expected}, actual {actual}",
        )
