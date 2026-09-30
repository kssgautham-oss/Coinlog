"""
expense.py - Expense model for CoinLog
Defines the Expense class representing a single expense entry.
"""

from datetime import datetime

CATEGORIES = [
    "food", "transport", "shopping", "health",
    "education", "entertainment", "utilities", "other"
]


class Expense:
    """Represents a single expense record."""

    def __init__(self, expense_id, amount, category, description="",
                 date=None, created_at=None):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a valid number.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if category.lower() not in CATEGORIES:
            raise ValueError(f"Category must be one of: {CATEGORIES}")
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format.")

        self.expense_id  = expense_id
        self.amount      = round(amount, 2)
        self.category    = category.lower()
        self.description = description.strip()
        self.date        = date or datetime.now().strftime("%Y-%m-%d")
        self.created_at  = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update(self, amount=None, category=None, description=None, date=None):
        if amount is not None:
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                raise ValueError("Amount must be a valid number.")
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            self.amount = round(amount, 2)
        if category is not None:
            if category.lower() not in CATEGORIES:
                raise ValueError(f"Category must be one of: {CATEGORIES}")
            self.category = category.lower()
        if description is not None:
            self.description = description.strip()
        if date is not None:
            if date != "":
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Date must be in YYYY-MM-DD format.")
            self.date = date if date != "" else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "expense_id":  self.expense_id,
            "amount":      self.amount,
            "category":    self.category,
            "description": self.description,
            "date":        self.date,
            "created_at":  self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            expense_id  = data["expense_id"],
            amount      = data["amount"],
            category    = data["category"],
            description = data.get("description", ""),
            date        = data.get("date"),
            created_at  = data.get("created_at"),
        )

    def __repr__(self):
        return (f"Expense(id={self.expense_id}, amount=₹{self.amount}, "
                f"category={self.category}, date={self.date})")
