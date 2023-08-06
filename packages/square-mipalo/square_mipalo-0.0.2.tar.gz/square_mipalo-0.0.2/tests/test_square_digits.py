import unittest

from src.square_mipalo import square_digits


class TestSquareTwoDigits(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(square_digits.squared(3, 3), 36)
        self.assertEqual(square_digits.squared(3, 5), 64)

    def test_negative_numbers(self):
        self.assertEqual(square_digits.squared(-2, -3), 25)
        self.assertEqual(square_digits.squared(-4, -2), 36)

    def test_mixed_numbers(self):
        self.assertEqual(square_digits.squared(-2, 3), 1)
        self.assertEqual(square_digits.squared(4, -2), 4)


if __name__ == '__main__':
    unittest.main()
