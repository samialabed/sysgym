import unittest

from sysgym.params.boxes import BooleanBox


class TestBooleanSpace(unittest.TestCase):
    def test_default_works(self):
        default_value = False
        test_space = BooleanBox(default=default_value)
        self.assertEqual(test_space.default, default_value)

    def test_different_default(self):
        default_value = True
        test_space = BooleanBox(default=default_value)
        self.assertEqual(test_space.default, default_value)

    def test_to_json(self):
        test_space = BooleanBox(default=True)

        actual = test_space.as_json()
        expected = '{"categories": [true, false]}'
        self.assertEqual(
            expected,
            actual,
        )


if __name__ == "__main__":
    unittest.main()
