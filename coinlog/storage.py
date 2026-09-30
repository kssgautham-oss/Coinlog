"""
storage.py - File I/O layer for CoinLog
Handles reading/writing expense data and budgets to JSON.
"""

import json
import os
import shutil
from datetime import datetime
from coinlog.expense import Expense

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "expenses.json")


class Storage:
    def __init__(self, filepath=None):
        self.filepath = filepath or DEFAULT_DATA_FILE
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(self.filepath):
            self._write_raw({"expenses": [], "budgets": {}, "next_id": 1})

    def _read_raw(self):
        """Read the JSON file. If it is corrupted, back it up and start fresh."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Top-level JSON must be an object.")
            return data
        except (json.JSONDecodeError, ValueError):
            self._backup_corrupted_file()
            fresh = {"expenses": [], "budgets": {}, "next_id": 1}
            self._write_raw(fresh)
            return fresh
        except OSError as e:
            raise RuntimeError(f"Could not read data file: {e}")

    def _backup_corrupted_file(self):
        """Keep the unreadable file as <name>.corrupt-<timestamp> so no data is lost."""
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = f"{self.filepath}.corrupt-{stamp}"
        try:
            shutil.copy2(self.filepath, backup)
            print(f"  [warning] Data file was unreadable. Backup saved to: {os.path.basename(backup)}")
        except OSError:
            pass

    def _write_raw(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            raise RuntimeError(f"Failed to write data file: {e}")

    def load_all(self):
        raw = self._read_raw()
        expenses = []
        for item in raw.get("expenses", []):
            try:
                expenses.append(Expense.from_dict(item))
            except (KeyError, ValueError):
                continue
        return expenses

    def load_budgets(self):
        raw = self._read_raw()
        return raw.get("budgets", {})

    def save_budgets(self, budgets):
        raw = self._read_raw()
        raw["budgets"] = budgets
        self._write_raw(raw)

    def get_next_id(self):
        raw = self._read_raw()
        next_id = raw.get("next_id", 1)
        raw["next_id"] = next_id + 1
        self._write_raw(raw)
        return next_id

    def save_all(self, expenses):
        raw = self._read_raw()
        raw["expenses"] = [e.to_dict() for e in expenses]
        self._write_raw(raw)

    def clear_all(self):
        self._write_raw({"expenses": [], "budgets": {}, "next_id": 1})
