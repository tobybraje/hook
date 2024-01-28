import unittest

from question_1 import increment_dictionary_values


class TestIncrementDictionaryValues(unittest.TestCase):
    def test_increment_dcitionary_values(self):
        d = {"a": 1}
        dd = increment_dictionary_values(d, 1)
        ddd = increment_dictionary_values(d, -1)
        self.assertEqual(dd["a"], 2)
        self.assertEqual(ddd["a"], 0)


if __name__ == "__main__":
    unittest.main()
