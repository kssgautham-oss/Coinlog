"""test_expense.py - Unit tests for CoinLog Expense model"""

import unittest
from coinlog.expense import Expense


class TestExpense(unittest.TestCase):

    def test_valid_creation(self):
        e = Expense(1, 150.0, "food", "Lunch")
        self.assertEqual(e.amount, 150.0)
        self.assertEqual(e.category, "food")

    def test_invalid_amount_zero(self):
        with self.assertRaises(ValueError):
            Expense(1, 0, "food")

    def test_invalid_amount_negative(self):
        with self.assertRaises(ValueError):
            Expense(1, -50, "food")

    def test_invalid_amount_string(self):
        with self.assertRaises(ValueError):
            Expense(1, "abc", "food")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            Expense(1, 100, "luxury")

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            Expense(1, 100, "food", date="15-09-2025")

    def test_to_dict_roundtrip(self):
        e = Expense(2, 200.0, "transport", "Cab", date="2025-09-10")
        restored = Expense.from_dict(e.to_dict())
        self.assertEqual(restored.amount, 200.0)
        self.assertEqual(restored.category, "transport")

    def test_update_amount(self):
        e = Expense(1, 100, "food")
        e.update(amount=250)
        self.assertEqual(e.amount, 250.0)

    def test_update_invalid_category(self):
        e = Expense(1, 100, "food")
        with self.assertRaises(ValueError):
            e.update(category="luxury")

    def test_amount_rounded(self):
        e = Expense(1, 99.9999, "other")
        self.assertEqual(e.amount, 100.0)


if __name__ == "__main__":
    unittest.main()
