import unittest

from sysgym.params.boxes import BooleanBox


class TestParametersBox(unittest.TestCase):
    def test_box_values_get_and_set(self):

        test_value = False
        test_space = BooleanBox(default=test_value)
        self.assertEqual(
            test_space.default,
            test_value,
            "Assert the default value is propagated into the container",
        )

        new_value = True
        test_space.value = new_value
        self.assertEqual(
            test_space.value,
            new_value,
            "Assert the new value updates the container ",
        )


if __name__ == "__main__":
    unittest.main()
