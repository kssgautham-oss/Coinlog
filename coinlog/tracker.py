"""
tracker.py - Core expense tracking logic for CoinLog
Provides CRUD, filtering, reporting, and budget management.
"""

from coinlog.expense import Expense, CATEGORIES
from coinlog.storage import Storage
from datetime import datetime
from collections import defaultdict


class Tracker:
    """Core tracker managing expenses and budgets."""

    def __init__(self, storage=None):
        self.storage  = storage or Storage()
        self.expenses = self.storage.load_all()
        self.budgets  = self.storage.load_budgets()

    def _save(self):
        self.storage.save_all(self.expenses)

    # ──────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────
    def add_expense(self, amount, category, description="", date=None):
        expense_id = self.storage.get_next_id()
        expense = Expense(expense_id, amount, category, description, date)
        self.expenses.append(expense)
        self._save()
        return expense

    # ──────────────────────────────────────────
    # READ / FILTER
    # ──────────────────────────────────────────
    def get_all(self):
        return sorted(self.expenses, key=lambda e: e.date, reverse=True)

    def get_by_id(self, expense_id):
        for e in self.expenses:
            if e.expense_id == expense_id:
                return e
        return None

    def get_by_category(self, category):
        return [e for e in self.expenses if e.category == category.lower()]

    def get_by_month(self, year_month):
        """Filter by month string in YYYY-MM format."""
        return [e for e in self.expenses if e.date.startswith(year_month)]

    def get_by_date(self, date_str):
        return [e for e in self.expenses if e.date == date_str]

    def get_by_date_range(self, start, end):
        """Return expenses between start and end dates (inclusive, YYYY-MM-DD)."""
        return [e for e in self.expenses if start <= e.date <= end]

    # ──────────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────────
    def update_expense(self, expense_id, **kwargs):
        expense = self.get_by_id(expense_id)
        if expense is None:
            raise LookupError(f"No expense found with ID {expense_id}.")
        expense.update(**kwargs)
        self._save()
        return expense

    # ──────────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────────
    def delete_expense(self, expense_id):
        expense = self.get_by_id(expense_id)
        if expense is None:
            raise LookupError(f"No expense found with ID {expense_id}.")
        self.expenses.remove(expense)
        self._save()
        return expense

    def clear_all(self):
        self.expenses = []
        self.storage.clear_all()

    # ──────────────────────────────────────────
    # BUDGET
    # ──────────────────────────────────────────
    def set_budget(self, category, amount):
        if category not in CATEGORIES:
            raise ValueError(f"Category must be one of: {CATEGORIES}")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Budget amount must be a valid number.")
        if amount <= 0:
            raise ValueError("Budget must be greater than zero.")
        self.budgets[category] = round(amount, 2)
        self.storage.save_budgets(self.budgets)

    def get_budget(self, category):
        return self.budgets.get(category)

    def get_all_budgets(self):
        return self.budgets

    # ──────────────────────────────────────────
    # REPORTING
    # ──────────────────────────────────────────
    def get_total(self, expenses=None):
        src = expenses if expenses is not None else self.expenses
        return round(sum(e.amount for e in src), 2)

    def get_monthly_summary(self, year_month):
        """Return per-category totals and budget status for a given month."""
        expenses = self.get_by_month(year_month)
        totals = defaultdict(float)
        for e in expenses:
            totals[e.category] += e.amount
        result = {}
        for cat in CATEGORIES:
            spent  = round(totals.get(cat, 0.0), 2)
            budget = self.budgets.get(cat)
            result[cat] = {
                "spent":  spent,
                "budget": budget,
                "over":   (spent > budget) if budget else False,
            }
        return result

    def get_category_totals(self, expenses=None):
        """Return total spent per category."""
        src = expenses if expenses is not None else self.expenses
        totals = defaultdict(float)
        for e in src:
            totals[e.category] += e.amount
        return {k: round(v, 2) for k, v in sorted(totals.items())}

    def get_overall_summary(self):
        total    = self.get_total()
        by_cat   = self.get_category_totals()
        count    = len(self.expenses)
        today    = datetime.now().strftime("%Y-%m")
        monthly  = self.get_total(self.get_by_month(today))
        return {
            "total_all_time": total,
            "total_this_month": monthly,
            "count": count,
            "by_category": by_cat,
        }
