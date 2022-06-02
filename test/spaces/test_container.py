import unittest

from sysgym.boxes import BooleanBox, ParameterContainer


class TestParametersContainer(unittest.TestCase):
    def test_container_values_get_and_set(self):
        test_space = BooleanBox(name="test_container", default=False)
        test_container = ParameterContainer(test_space)
        self.assertEqual(
            test_container.value,
            test_space.default,
            "Assert the default value is propagated into the container",
        )

        new_value = True
        test_container.value = new_value
        self.assertEqual(
            test_container.value,
            new_value,
            "Assert the new value updates the container ",
        )


if __name__ == "__main__":
    unittest.main()
