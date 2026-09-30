"""test_storage_and_cli.py - Storage recovery, import checks and CLI flow tests for CoinLog"""

import importlib
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

from coinlog.storage import Storage
from coinlog.tracker import Tracker
from coinlog import display


class TestImports(unittest.TestCase):
    """Every module must import cleanly (this would have caught the f-string SyntaxError)."""

    def test_all_modules_import(self):
        for name in ("expense", "storage", "tracker", "display", "utils", "cli"):
            with self.subTest(module=name):
                importlib.import_module(f"coinlog.{name}")


class TestStorageRecovery(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "expenses.json")

    def test_corrupted_file_is_backed_up_and_reset(self):
        with open(self.path, "w") as f:
            f.write("{ broken")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(Storage(filepath=self.path).load_all(), [])
        self.assertEqual(len([n for n in os.listdir(self.dir) if ".corrupt-" in n]), 1)

    def test_data_and_budgets_persist(self):
        t1 = Tracker(storage=Storage(filepath=self.path))
        t1.add_expense(120, "food", "x", "2030-01-05")
        t1.set_budget("food", 500)
        t2 = Tracker(storage=Storage(filepath=self.path))
        self.assertEqual(len(t2.get_all()), 1)
        self.assertEqual(t2.get_budget("food"), 500.0)


class TestDisplaySmoke(unittest.TestCase):
    """Render every screen with real data and with empty data - must never raise."""

    def setUp(self):
        d = tempfile.mkdtemp()
        self.tracker = Tracker(storage=Storage(filepath=os.path.join(d, "e.json")))

    def _render(self):
        with redirect_stdout(io.StringIO()) as buf:
            display.print_banner()
            display.print_menu()
            display.print_expense_list(self.tracker.get_all())
            display.print_overall_summary(self.tracker.get_overall_summary())
            display.print_monthly_summary("2030-01", self.tracker.get_monthly_summary("2030-01"))
            display.print_budget_table(self.tracker.get_all_budgets(),
                                       self.tracker.get_category_totals(), month="2030-01")
        return buf.getvalue()

    def test_render_with_no_data(self):
        self.assertIn("No spending recorded yet", self._render())

    def test_render_with_data(self):
        self.tracker.add_expense(300, "food", "Lunch", "2030-01-05")
        self.tracker.set_budget("food", 200)
        out = self._render()
        self.assertIn("300.00", out)
        self.assertIn("OVER", out)


def run_cli(inputs, path):
    from coinlog import cli
    out = io.StringIO()
    with mock.patch("builtins.input", side_effect=inputs), \
         mock.patch("coinlog.storage.DEFAULT_DATA_FILE", path), \
         redirect_stdout(out):
        cli.run()
    return out.getvalue()


class TestCLIFlows(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "expenses.json")

    def test_add_and_view(self):
        out = run_cli(["1", "250", "food", "Lunch", "", "2", "0"], self.path)
        self.assertIn("added", out)
        self.assertIn("Lunch", out)

    def test_non_numeric_amount_reprompts(self):
        out = run_cli(["1", "abc", "50", "other", "", "", "0"], self.path)
        self.assertIn("valid number", out)
        self.assertIn("added", out)

    def test_update_with_bad_amount_reprompts_not_crashes(self):
        out = run_cli(["1", "100", "food", "x", "", "7", "1", "abc", "75", "", "", "", "0"], self.path)
        self.assertIn("valid number", out)
        self.assertIn("updated successfully", out)

    def test_monthly_report_blank_month_uses_current(self):
        out = run_cli(["9", "", "0"], self.path)
        self.assertIn("Monthly Report", out)

    def test_budget_status_uses_current_month_only(self):
        # an old-month expense must NOT count against this month's budget
        out = run_cli(["1", "900", "food", "old", "2020-01-01",
                       "11", "food", "100", "12", "0"], self.path)
        self.assertNotIn("OVER!", out)

    def test_closed_input_exits_cleanly(self):
        out = run_cli(["zzz", EOFError], self.path)
        self.assertIn("Input closed", out)



class TestPlainMode(unittest.TestCase):
    """Non-terminal output must contain no colour escape codes (keeps cmd/old consoles readable)."""

    def test_no_escape_codes_when_not_a_terminal(self):
        import subprocess, sys
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        res = subprocess.run([sys.executable, "main.py"], input="0\n", text=True,
                             capture_output=True, cwd=root, env=env)
        self.assertEqual(res.returncode, 0)
        self.assertNotIn("\x1b[", res.stdout)


@unittest.skipIf(os.name == "nt", "pseudo-terminal test only runs on Linux/macOS")
class TestRealTerminalColours(unittest.TestCase):
    """On a real terminal colours appear; with NO_COLOR they do not."""

    def _run_in_pty(self, extra_env):
        import pty, select, subprocess, sys
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env = {k: v for k, v in os.environ.items() if k != "NO_COLOR"}
        env.update(extra_env)
        master, slave = pty.openpty()
        proc = subprocess.Popen([sys.executable, "main.py"], stdin=slave, stdout=slave,
                                stderr=slave, cwd=root, env=env, close_fds=True)
        os.write(master, b"0\n")
        out = b""
        while select.select([master], [], [], 2)[0]:
            try:
                chunk = os.read(master, 4096)
            except OSError:
                break
            if not chunk:
                break
            out += chunk
        proc.wait(timeout=5)
        os.close(master)
        os.close(slave)
        return out

    def test_colours_on_terminal(self):
        self.assertIn(b"\x1b[", self._run_in_pty({}))

    def test_no_color_variable_disables_colours(self):
        self.assertNotIn(b"\x1b[", self._run_in_pty({"NO_COLOR": "1"}))


if __name__ == "__main__":
    unittest.main()
