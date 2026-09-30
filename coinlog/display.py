"""
display.py - Terminal output formatting for CoinLog
"""

import os
RESET   = "\033[0m"
BOLD    = "\033[1m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
DIM     = "\033[2m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"

# Plain-text mode: when NO_COLOR is set (or colours are unsupported) drop all colour codes.
if os.environ.get("NO_COLOR"):
    RESET, BOLD, RED, GREEN, YELLOW, CYAN, WHITE, DIM, MAGENTA, BLUE = ("",) * 10


CATEGORY_COLOR = {
    "food":          YELLOW,
    "transport":     CYAN,
    "shopping":      MAGENTA,
    "health":        GREEN,
    "education":     BLUE,
    "entertainment": RED,
    "utilities":     WHITE,
    "other":         DIM,
}


def colorize(text, color):
    return f"{color}{text}{RESET}"


def print_banner():
    print(f"""
{GREEN}{BOLD}
   ██████╗ ██████╗ ██╗███╗   ██╗██╗      ██████╗  ██████╗
  ██╔════╝██╔═══██╗██║████╗  ██║██║     ██╔═══██╗██╔════╝
  ██║     ██║   ██║██║██╔██╗ ██║██║     ██║   ██║██║  ███╗
  ██║     ██║   ██║██║██║╚██╗██║██║     ██║   ██║██║   ██║
  ╚██████╗╚██████╔╝██║██║ ╚████║███████╗╚██████╔╝╚██████╔╝
   ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝  ╚═════╝
{RESET}{DIM}              Track every rupee. Own your finances.{RESET}
""")


def print_separator(char="─", width=70):
    print(colorize(char * width, DIM))


def print_expense_row(expense):
    cat_color  = CATEGORY_COLOR.get(expense.category, WHITE)
    cat_str    = colorize(f"[{expense.category.upper()}]", cat_color + BOLD)
    id_str     = colorize(f"#{expense.expense_id}", CYAN + BOLD)
    amount_str = colorize(f"₹{expense.amount:.2f}", GREEN + BOLD)
    date_str   = colorize(expense.date, DIM)

    print(f"  {id_str}  {amount_str}  {cat_str}  {date_str}")
    if expense.description:
        print(f"       {DIM}{expense.description}{RESET}")
    print()


def print_expense_list(expenses, header="Expenses"):
    print_separator()
    total = sum(e.amount for e in expenses)
    noun = "entry" if len(expenses) == 1 else "entries"
    print(colorize(f"  {header} ({len(expenses)} {noun}) — Total: ₹{total:.2f}", BOLD + WHITE))
    print_separator()
    if not expenses:
        print(colorize("  No expenses found.\n", DIM))
        return
    for expense in expenses:
        print_expense_row(expense)


def print_monthly_summary(year_month, summary):
    print_separator()
    print(colorize(f"  📅  Monthly Report — {year_month}", BOLD + WHITE))
    print_separator()
    grand_total = 0
    for cat, data in summary.items():
        if data["spent"] == 0 and data["budget"] is None:
            continue
        spent  = data["spent"]
        budget = data["budget"]
        over   = data["over"]
        grand_total += spent

        cat_color  = CATEGORY_COLOR.get(cat, WHITE)
        cat_label  = colorize(cat.capitalize().ljust(14), cat_color + BOLD)
        spent_str  = colorize(f"₹{spent:.2f}", RED if over else GREEN)
        budget_str = colorize(f"Budget: ₹{budget:.2f}", DIM) if budget else colorize("No budget set", DIM)
        flag       = colorize(" ⚠ OVER BUDGET", RED) if over else ""

        print(f"  {cat_label}  Spent: {spent_str}  {budget_str}{flag}")

    print_separator()
    print(f"  {colorize('TOTAL SPENT'.ljust(16), BOLD)}  {colorize(f'₹{grand_total:.2f}', BOLD + WHITE)}")
    print_separator()
    print()


def print_overall_summary(summary):
    print_separator()
    print(colorize("  💰  CoinLog Overview", BOLD + WHITE))
    print_separator()
    print(f"  Total Entries       : {colorize(str(summary['count']), BOLD)}")
    all_time   = summary["total_all_time"]
    this_month = summary["total_this_month"]
    print(f"  Total Spent (All)   : {colorize(f'₹{all_time:.2f}', RED + BOLD)}")
    print(f"  Spent This Month    : {colorize(f'₹{this_month:.2f}', YELLOW + BOLD)}")
    print()
    print(colorize("  Breakdown by Category:", BOLD + WHITE))
    biggest = max(summary["by_category"].values(), default=0)
    if biggest == 0:
        print(colorize("  No spending recorded yet.", DIM))
    for cat, total in summary["by_category"].items():
        if total == 0 or biggest == 0:
            continue
        bar_len = max(1, int((total / biggest) * 20))
        bar     = colorize("█" * bar_len, CATEGORY_COLOR.get(cat, WHITE))
        print(f"  {cat.capitalize().ljust(14)} {bar}  ₹{total:.2f}")
    print_separator()
    print()


def print_budget_table(budgets, category_totals, month=None):
    print_separator()
    title = f"  🎯  Budget Status — {month}" if month else "  🎯  Budget Status"
    print(colorize(title, BOLD + WHITE))
    print_separator()
    if not budgets:
        print(colorize("  No budgets set yet. Use option 11 to add one.\n", DIM))
        return
    for cat, budget in budgets.items():
        spent    = category_totals.get(cat, 0)
        over     = spent > budget
        color    = RED if over else GREEN
        pct      = (spent / budget * 100) if budget else 0
        bar_fill = int(min(pct, 100) / 5)
        bar      = colorize("█" * bar_fill, color) + colorize("░" * (20 - bar_fill), DIM)
        flag     = colorize(" OVER!", RED) if over else ""
        print(f"  {cat.capitalize().ljust(14)} [{bar}] ₹{spent:.2f}/₹{budget:.2f}{flag}")
    print_separator()
    print()


def print_success(msg):
    print(colorize(f"\n  ✔  {msg}\n", GREEN))


def print_error(msg):
    print(colorize(f"\n  ✘  Error: {msg}\n", RED))


def print_info(msg):
    print(colorize(f"\n  ℹ  {msg}\n", CYAN))


def print_menu():
    print_separator()
    print(colorize("  MAIN MENU", BOLD + WHITE))
    print_separator()
    options = [
        ("1",  "Add Expense"),
        ("2",  "View All Expenses"),
        ("3",  "View Expenses by Category"),
        ("4",  "View Expenses by Month"),
        ("5",  "View Expenses by Date"),
        ("6",  "View Expenses by Date Range"),
        ("7",  "Update Expense"),
        ("8",  "Delete Expense"),
        ("9",  "Monthly Summary Report"),
        ("10", "Overall Summary & Category Breakdown"),
        ("11", "Set Monthly Budget"),
        ("12", "View Budget Status"),
        ("0",  "Exit"),
    ]
    for key, label in options:
        print(f"  {colorize(key.rjust(2), CYAN + BOLD)}  {label}")
    print_separator()
