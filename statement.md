# statement.md — CoinLog

## Problem Statement

Most people have a rough sense of what they spend but no actual record of it. Small everyday purchases — food, transport, a subscription — add up quietly over a month, and by the time a bill or a low balance draws attention to it, the details are already forgotten. Spreadsheets can track this but take more effort than a quick entry deserves, and most dedicated expense apps expect an account and an internet connection for something that does not need either. CoinLog is a terminal-based expense tracker built to close that gap: a lightweight tool that lets someone log a purchase in a few seconds, see it grouped by category, and compare their spending against a monthly budget, all stored privately on their own machine.

## Scope

CoinLog covers:
- Adding, viewing, updating and deleting expense entries, each with an amount, a category, an optional description, and a date
- Filtering expenses by category, by month, by an exact date, or by a date range
- A monthly report showing spending per category compared against that category's budget
- An overall summary showing total spending and a breakdown by category
- Setting a monthly budget per category, with a warning once spending crosses it
- Automatic saving to a local JSON file, with recovery if that file is ever damaged

CoinLog does not cover multiple currencies, multiple users on one data file, custom or user-defined categories, or a graphical interface — it is a single-user, terminal-only tool by design.

## Target Users

- Students managing pocket money or a monthly allowance
- Anyone who wants a fast, offline way to track spending without setting up an account or a spreadsheet

## High-Level Features

1. **Expense management** — add, update, delete and view entries
2. **Filtering** — by category, month, exact date, or date range
3. **Reporting** — a monthly report and an overall summary with a category breakdown
4. **Budgeting** — a monthly limit per category, with a clear warning when it is exceeded
5. **Reliable storage** — data is saved after every change and recovered automatically if the file is ever corrupted
