# statement.md: CoinLog

## Problem Statement
Small everyday purchases add up, and without a record it is hard to say where the money went at the end of the month. Spreadsheets take effort for a quick entry and many apps need an account or an internet connection. CoinLog is a simple terminal-based expense tracker that lets a user log spending, group it by category, and compare it against monthly budgets.

## Scope
- Add, view, update and delete expense entries (amount, category, description, date)
- Filter expenses by category, month, exact date, or date range
- Monthly report with per-category totals and budget comparison
- Overall summary with a category breakdown bar chart
- A monthly budget per category, with an over-budget warning
- Data stored in a local JSON file; no database and no internet needed
- Runs from the command line (PowerShell, cmd, or a Linux/macOS terminal) using only the Python standard library

Not included: multiple users, currencies other than rupees, custom categories, and a graphical interface.

## Target Users
- Students tracking pocket money or a monthly allowance
- Anyone who wants a quick, offline, no-setup expense log

## High-Level Features
1. Expense management: add, update, delete and view entries
2. Filtering: by category, month, date, or date range
3. Reports: monthly report and overall summary
4. Budgets: set a limit per category and see the status for the current month
5. Automatic saving to a local JSON file, with recovery if the file is damaged
6. Input validation with clear messages instead of crashes
