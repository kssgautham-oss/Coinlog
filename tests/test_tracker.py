"""test_tracker.py - Unit tests for CoinLog Tracker"""

import unittest
import tempfile
import os
from coinlog.tracker import Tracker
from coinlog.storage import Storage


def temp_tracker():
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.close()
    os.unlink(tmp.name)
    storage = Storage(filepath=tmp.name)
    return Tracker(storage=storage), tmp.name


class TestTracker(unittest.TestCase):

    def setUp(self):
        self.tracker, self.tmp = temp_tracker()

    def tearDown(self):
        if os.path.exists(self.tmp):
            os.unlink(self.tmp)

    def test_add_expense(self):
        e = self.tracker.add_expense(100, "food", "Lunch")
        self.assertEqual(e.amount, 100.0)
        self.assertEqual(len(self.tracker.get_all()), 1)

    def test_get_by_id(self):
        e = self.tracker.add_expense(200, "transport")
        found = self.tracker.get_by_id(e.expense_id)
        self.assertIsNotNone(found)

    def test_get_missing_id(self):
        self.assertIsNone(self.tracker.get_by_id(999))

    def test_update_expense(self):
        e = self.tracker.add_expense(100, "food")
        self.tracker.update_expense(e.expense_id, amount=200)
        self.assertEqual(self.tracker.get_by_id(e.expense_id).amount, 200.0)

    def test_delete_expense(self):
        e = self.tracker.add_expense(100, "food")
        self.tracker.delete_expense(e.expense_id)
        self.assertIsNone(self.tracker.get_by_id(e.expense_id))

    def test_filter_by_category(self):
        self.tracker.add_expense(100, "food")
        self.tracker.add_expense(200, "transport")
        food = self.tracker.get_by_category("food")
        self.assertEqual(len(food), 1)

    def test_get_total(self):
        self.tracker.add_expense(100, "food")
        self.tracker.add_expense(200, "transport")
        self.assertEqual(self.tracker.get_total(), 300.0)

    def test_budget_set_and_get(self):
        self.tracker.set_budget("food", 1000)
        self.assertEqual(self.tracker.get_budget("food"), 1000.0)

    def test_budget_invalid_category(self):
        with self.assertRaises(ValueError):
            self.tracker.set_budget("luxury", 500)

    def test_monthly_summary(self):
        self.tracker.add_expense(300, "food", date="2025-09-01")
        self.tracker.add_expense(150, "transport", date="2025-09-10")
        summary = self.tracker.get_monthly_summary("2025-09")
        self.assertEqual(summary["food"]["spent"], 300.0)
        self.assertEqual(summary["transport"]["spent"], 150.0)

    def test_overall_summary(self):
        self.tracker.add_expense(500, "shopping")
        s = self.tracker.get_overall_summary()
        self.assertEqual(s["count"], 1)
        self.assertGreater(s["total_all_time"], 0)

    def test_delete_missing_raises(self):
        with self.assertRaises(LookupError):
            self.tracker.delete_expense(999)

    def test_update_missing_raises(self):
        with self.assertRaises(LookupError):
            self.tracker.update_expense(999, amount=100)


if __name__ == "__main__":
    unittest.main()
