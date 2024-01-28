import random
import unittest

from question_2 import get_largest_possible_loss


class TestQuestion2(unittest.TestCase):
    def test_empty_list(self):
        prices = []
        result = get_largest_possible_loss(prices)

        self.assertEqual(result["Biggest Loss"], 0)
        self.assertEqual(result["Index 1"], None)
        self.assertEqual(result["Index 2"], None)

    def test_list_in_order(self):
        prices = [1, 2.98, 3.56]
        result = get_largest_possible_loss(prices)

        self.assertEqual(result["Biggest Loss"], 0)
        self.assertEqual(result["Index 1"], None)
        self.assertEqual(result["Index 2"], None)

    def test_list_in_reverse_order(self):
        prices = [3.56, 2.98, 1.37]
        result = get_largest_possible_loss(prices)

        self.assertEqual(result["Biggest Loss"], 2.19)
        self.assertEqual(result["Index 1"], 0)
        self.assertEqual(result["Index 2"], 2)

    def test_unordered_list(self):
        prices = [2.98, 3.56, 1.37]
        result = get_largest_possible_loss(prices)

        self.assertEqual(result["Biggest Loss"], 2.19)
        self.assertEqual(result["Index 1"], 1)
        self.assertEqual(result["Index 2"], 2)

    def test_wrong_type(self):
        prices = [2.98, "not a float or an int!", 1.37]
        result = get_largest_possible_loss(prices)

        self.assertEqual(result["Error"], "The supplied prices are of the wrong type")

    def test_too_many_decimal_places(self):
        prices = [
            3.43543045,
            6.4981561348468489,
            4.8494984949,
            800.156909800,
            95.5165165,
            2.788915,
        ]

        result = get_largest_possible_loss(prices)

        self.assertEqual(result["Biggest Loss"], 797.37)
        self.assertEqual(result["Index 1"], 3)
        self.assertEqual(result["Index 2"], 5)

    def test_indexes_always_correct_order(self):
        for i in range(1, 1000):
            prices = [random.uniform(0, 1000000000) for i in range(1, 100)]
            result = get_largest_possible_loss(prices)

            self.assertTrue(result["Index 2"] > result["Index 1"])


if __name__ == "__main__":
    unittest.main()
