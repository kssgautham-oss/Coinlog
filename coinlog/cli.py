"""
cli.py - CLI interface for CoinLog
Handles all user interaction and menu routing.
"""

from coinlog.tracker import Tracker
from coinlog.display import (
    print_banner, print_menu, print_expense_list,
    print_monthly_summary, print_overall_summary,
    print_budget_table, print_success, print_error, print_info
)
from coinlog import utils
from datetime import datetime


def run():
    tracker = Tracker()
    print_banner()

    while True:
        print_menu()
        try:
            choice = input("  Enter your choice: ").strip()
        except EOFError:
            print_info("Input closed. Exiting CoinLog.")
            break
        except KeyboardInterrupt:
            print_info("Exiting CoinLog. Goodbye!")
            break
        print()

        try:
            if choice == "1":
                _add_expense(tracker)

            elif choice == "2":
                print_expense_list(tracker.get_all(), header="All Expenses")

            elif choice == "3":
                cat = utils.prompt_category()
                expenses = tracker.get_by_category(cat)
                print_expense_list(expenses, header=f"{cat.capitalize()} Expenses")

            elif choice == "4":
                month = utils.prompt_month()
                expenses = tracker.get_by_month(month)
                print_expense_list(expenses, header=f"Expenses in {month}")

            elif choice == "5":
                date = utils.prompt_date("Date (YYYY-MM-DD)")
                if date:
                    expenses = tracker.get_by_date(date)
                    print_expense_list(expenses, header=f"Expenses on {date}")

            elif choice == "6":
                print("  Enter date range:")
                start = utils.prompt_date("  Start date (YYYY-MM-DD)")
                end   = utils.prompt_date("  End date   (YYYY-MM-DD)")
                if start and end:
                    if start > end:
                        print_error("Start date must be before end date.")
                    else:
                        expenses = tracker.get_by_date_range(start, end)
                        print_expense_list(expenses, header=f"Expenses {start} → {end}")

            elif choice == "7":
                _update_expense(tracker)

            elif choice == "8":
                _delete_expense(tracker)

            elif choice == "9":
                month = utils.prompt_month(default=datetime.now().strftime("%Y-%m"))
                summary = tracker.get_monthly_summary(month)
                print_monthly_summary(month, summary)

            elif choice == "10":
                summary = tracker.get_overall_summary()
                print_overall_summary(summary)

            elif choice == "11":
                _set_budget(tracker)

            elif choice == "12":
                this_month = datetime.now().strftime("%Y-%m")
                budgets = tracker.get_all_budgets()
                cat_totals = tracker.get_category_totals(tracker.get_by_month(this_month))
                print_budget_table(budgets, cat_totals, month=this_month)

            elif choice == "0":
                print_info("Thanks for using CoinLog. Stay financially sharp!")
                break

            else:
                print_error("Invalid choice. Please select a valid menu option.")

        except KeyboardInterrupt:
            print_info("\nReturning to main menu...")
        except Exception as e:
            print_error(str(e))


def _add_expense(tracker):
    print("\n  ── Add New Expense ──")
    amount      = utils.prompt_float("Amount (₹)")
    category    = utils.prompt_category()
    description = utils.prompt("Description (optional)", required=False, default="") or ""
    date        = utils.prompt_date()
    expense     = tracker.add_expense(amount, category, description, date)
    print_success(f"Expense #{expense.expense_id} — ₹{expense.amount:.2f} [{expense.category}] added.")


def _update_expense(tracker):
    expenses = tracker.get_all()
    if not expenses:
        print_info("No expenses to update.")
        return
    print_expense_list(expenses, header="Select Expense to Update")
    eid     = utils.prompt_int("Enter Expense ID to update")
    expense = tracker.get_by_id(eid)
    if not expense:
        print_error(f"Expense #{eid} not found.")
        return
    print(f"\n  Updating Expense #{eid} — leave blank to keep current value.\n")
    amount      = utils.prompt_optional_float("New Amount (₹)", expense.amount)
    category    = utils.prompt_category(default=expense.category)
    description = utils.prompt("New Description", required=False, default=expense.description)
    date        = utils.prompt_date(f"New Date (current: {expense.date})")
    tracker.update_expense(
        eid,
        amount      = amount,
        category    = category,
        description = description,
        date        = date or expense.date,
    )
    print_success(f"Expense #{eid} updated successfully.")


def _delete_expense(tracker):
    expenses = tracker.get_all()
    if not expenses:
        print_info("No expenses to delete.")
        return
    print_expense_list(expenses, header="Select Expense to Delete")
    eid     = utils.prompt_int("Enter Expense ID to delete")
    expense = tracker.get_by_id(eid)
    if not expense:
        print_error(f"Expense #{eid} not found.")
        return
    if utils.confirm(f"Delete ₹{expense.amount} [{expense.category}]?"):
        tracker.delete_expense(eid)
        print_success(f"Expense #{eid} deleted.")
    else:
        print_info("Deletion cancelled.")


def _set_budget(tracker):
    print("\n  ── Set Monthly Budget ──")
    category = utils.prompt_category()
    amount   = utils.prompt_float(f"Budget amount for '{category}' (₹)")
    tracker.set_budget(category, amount)
    print_success(f"Budget for '{category}' set to ₹{amount:.2f}.")
