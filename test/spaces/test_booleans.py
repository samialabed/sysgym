import unittest

from sysgym.spaces import BooleanSpace


class TestBooleanSpace(unittest.TestCase):
    def test_default_works(self):
        default_value = False
        test_space = BooleanSpace(name="test_space", default=default_value)
        self.assertEqual(test_space.default, default_value)

    def test_different_default(self):
        default_value = True
        test_space = BooleanSpace(name="test_space", default=default_value)
        self.assertEqual(test_space.default, default_value)

    def test_to_json(self):
        test_space = BooleanSpace(name="test_space", default=True)

        self.assertEqual(
            test_space.as_json(),
            '{"name": "test_space", "categories": [true, false]}',
        )


if __name__ == "__main__":
    unittest.main()
