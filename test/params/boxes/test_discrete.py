import unittest

from core import TestInput
from parameterized import parameterized

from sysgym.params.boxes import DiscreteBox


class TestDiscreteBox(unittest.TestCase):
    @parameterized.expand(
        [
            TestInput(
                name="Expect updating the box reflected",
                test_input=4,
                expected=4,
            ),
        ]
    )
    def test_discrete_box(self, name: str, box_val: int, expected: int):
        actual = DiscreteBox(lower_bound=0, upper_bound=4, default=2)
        actual.value = box_val

        self.assertEqual(
            expected,
            actual.value,
            f"failed test {name} expected {expected}, actual {actual}",
        )

    @parameterized.expand(
        [
            TestInput(
                name="Expect updating the box reflected",
                test_input=4,
                expected=40,
            ),
        ]
    )
    def test_discrete_box_formula_work(self, name: str, box_val: int, expected: int):
        actual = DiscreteBox(
            lower_bound=0, upper_bound=4, default=2, formula=lambda x: x * 10
        )
        actual.value = box_val

        self.assertEqual(
            expected,
            actual.value,
            f"failed test {name} expected {expected}, actual {actual}",
        )
