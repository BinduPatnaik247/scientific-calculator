import unittest
from decimal import localcontext

from calc_app import CalculationError, calculate


class ArithmeticTests(unittest.TestCase):
    def test_all_operations(self):
        for operation, expected in [("add", "13"), ("subtract", "7"),
                                    ("multiply", "30"), ("divide", "3.333333333333333333333333333")]:
            with self.subTest(operation=operation):
                self.assertEqual(calculate(operation, "10", "3"), expected)

    def test_decimal_precision(self):
        self.assertEqual(calculate("add", "0.1", "0.2"), "0.3")

    def test_negative_operands(self):
        self.assertEqual(calculate("multiply", "-2.5", "4"), "-10")

    def test_scientific_notation(self):
        self.assertEqual(calculate("add", "1e3", "2"), "1002")

    def test_negative_zero(self):
        self.assertEqual(calculate("multiply", "-0", "2"), "0")

    def test_integer_trailing_zeros(self):
        self.assertEqual(calculate("multiply", "10", "10"), "100")

    def test_zero_divisors(self):
        for zero in ["0", "-0", "0.00"]:
            with self.subTest(zero=zero), self.assertRaises(CalculationError):
                calculate("divide", "1", zero)

    def test_bad_numbers(self):
        for value in ["", "hello", "NaN", "Infinity", "1_000", "1e101", "1e-101",
                      "1.00000000000000000000000000001e100", "1" * 201]:
            with self.subTest(value=value), self.assertRaises(CalculationError):
                calculate("add", value, "2")

    def test_unknown_operation(self):
        with self.assertRaises(CalculationError):
            calculate("power", "2", "3")

    def test_independent_precision(self):
        with localcontext() as ctx:
            ctx.prec = 3
            self.assertEqual(calculate("divide", "1", "3"), "0.3333333333333333333333333333")
