"""
utils.py - Input helpers and validators for CoinLog
"""

from datetime import datetime
from coinlog.expense import CATEGORIES


def prompt(label, required=True, default=None):
    hint = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"  {label}{hint}: ").strip()
        if not value and default is not None:
            return default
        if not value and required:
            print("  This field is required.")
            continue
        return value if value else None


def prompt_float(label, min_val=0.01):
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            val = float(raw)
            if val < min_val:
                print(f"  Value must be greater than {min_val}.")
                continue
            return val
        except ValueError:
            print("  Please enter a valid number (e.g. 150 or 49.99).")


def prompt_int(label):
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a valid integer.")


def prompt_category(default=None):
    while True:
        hint = f" [{default}]" if default else f" {CATEGORIES}"
        val = input(f"  Category{hint}: ").strip().lower()
        if not val and default:
            return default
        if val in CATEGORIES:
            return val
        print(f"  Choose from: {CATEGORIES}")


def prompt_date(label="Date (YYYY-MM-DD, leave blank for today)", required=False):
    while True:
        val = input(f"  {label}: ").strip()
        if not val:
            return None
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("  Use YYYY-MM-DD format (e.g. 2025-09-15).")


def prompt_month(label="Month (YYYY-MM)", default=None):
    """Prompt for a YYYY-MM month. Blank returns `default` when one is given."""
    hint = f" [default: {default}]" if default else ""
    while True:
        val = input(f"  {label}{hint}: ").strip()
        if not val and default:
            return default
        try:
            datetime.strptime(val, "%Y-%m")
            return val
        except ValueError:
            print("  Use YYYY-MM format (e.g. 2025-09).")


def prompt_optional_float(label, current):
    """Prompt for a positive number; blank keeps `current`."""
    while True:
        raw = input(f"  {label} (current: {current:.2f}, blank=keep): ").strip()
        if not raw:
            return current
        try:
            val = float(raw)
        except ValueError:
            print("  Please enter a valid number (e.g. 150 or 49.99).")
            continue
        if val <= 0:
            print("  Amount must be greater than zero.")
            continue
        return val


def confirm(prompt_text="Are you sure?"):
    val = input(f"  {prompt_text} (y/n): ").strip().lower()
    return val == "y"
