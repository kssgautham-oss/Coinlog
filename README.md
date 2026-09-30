# CoinLog: A Command-Line Expense Tracker

> Keep track of where your money goes, straight from the terminal. No installs, no internet, no account.

**Course:** Python Essentials (VITyarthi) | **Institution:** VIT Bhopal
**Author:** Gautham

---

## 1. Project Overview

CoinLog is a small expense tracker that runs entirely in the terminal (PowerShell, cmd, or any Linux/macOS shell). You type in what you spent, pick a category, and CoinLog remembers it. Later you can look things up by category, month or date, and see a report of where the money went. You can also give each category a monthly budget, and CoinLog will tell you when you've gone over it.

**Objectives:**
- Let a user record an expense in a few seconds from the terminal, with no account or setup
- Organise spending by category so patterns are easy to see
- Let a user set a monthly budget per category and know immediately when they go over it
- Keep the data on the user's own machine, readable as plain JSON, with no external service

**The problem it solves:** most of us have a rough idea of what we spend but no real record. Small purchases like snacks, autos and subscriptions add up quietly, and by the end of the month it's hard to say where the money went. Spreadsheets feel like too much effort for a quick entry, and most apps need an account or an internet connection. CoinLog is meant to be the quick option: open the terminal, type a few lines, done.

**Who it's for:** students managing pocket money or a monthly allowance, and anyone who prefers a light offline tool to a heavy app.

---

## 2. Features

CoinLog has 12 features, grouped into three main modules.

### Module 1: Expense Management
- **Add** an expense with an amount, a category, an optional note, and a date (leave the date blank for today)
- **View** every expense, newest first, with a running total
- **Update** any field of an existing expense
- **Delete** an expense (it asks you to confirm first, so a stray keypress can't wipe anything)

### Module 2: Search and Filtering
- Filter by **category**, for example just "food"
- Filter by **month** (`2026-09`)
- Filter by an **exact date**
- Filter by a **date range**, for example the first half of a month

### Module 3: Reports and Budgets
- **Monthly report:** spending per category for a chosen month (press Enter to use the current month)
- **Overall summary:** total spent, this month's total, and a small bar chart by category
- **Set a budget** for any category
- **Budget status:** progress bars showing this month's spending against each budget, with an `OVER!` flag when you cross the limit

### Things that make it dependable
- **Input checking everywhere.** A wrong amount, an impossible date or an unknown category never crashes the program. It explains the problem and asks again.
- **Your data is saved automatically** after every change, so closing the window loses nothing.
- **Corrupted data file recovery.** If the data file is ever damaged, CoinLog keeps a backup copy of it (named `expenses.json.corrupt-<time>`) and starts fresh instead of crashing.
- **Works in PowerShell and cmd.** Colours are used where the terminal supports them. If it doesn't, CoinLog quietly falls back to plain text. You can also force plain text by setting the `NO_COLOR` environment variable.

---

## 3. Technologies Used

CoinLog is written in **Python 3** (developed and tested on Python 3.12 and 3.13) and uses **only the standard library**. There is nothing to `pip install`, which keeps setup simple and means it should behave the same on any machine with Python.

| Module | What CoinLog uses it for |
|---|---|
| `json` | Saving and loading expenses and budgets in `data/expenses.json`, a plain text file you can open and read |
| `os` | Building file paths that work on Windows and Linux, and creating the `data` folder on first run |
| `datetime` | Checking that dates and months are real (`2026-02-30` gets rejected) and finding "today" and "this month" |
| `collections` | `defaultdict`, which makes adding up totals per category short and tidy |
| `shutil` | Copying a damaged data file to a backup before starting fresh |
| `sys` and `ctypes` | Setting up the console at startup (UTF-8 output, and colour support on Windows) |
| `unittest` | The automated test suite |
| `unittest.mock`, `tempfile`, `io`, `contextlib`, `importlib`, `subprocess`, `pty` | Supporting the tests: faking keyboard input, using throwaway data files, capturing output, and launching the real program |

**Python ideas this project practises:** classes and methods, a `classmethod`, lists and dictionaries, list comprehensions, `sorted()` with a key, f-strings, `try` / `except`, reading and writing files, and splitting a program into modules.

---

## 4. Project Structure

```
coinlog/
├── main.py                  # Entry point: run this to start the app
├── requirements.txt         # Empty on purpose (standard library only)
├── README.md
├── statement.md             # Problem statement, scope, target users
├── .gitignore
├── data/
│   └── expenses.json        # Created automatically on first run
├── docs/
│   └── diagrams/            # Architecture, use case, workflow, sequence, class and ER diagrams
├── coinlog/
│   ├── __init__.py
│   ├── expense.py           # Expense class: one record, with validation
│   ├── tracker.py           # Tracker class: add/update/delete, filters, budgets, reports
│   ├── storage.py           # Storage class: reads and writes the JSON file
│   ├── display.py           # Everything printed: tables, reports, colours
│   ├── utils.py             # Input helpers that re-ask until the answer is valid
│   └── cli.py               # The menu and the flow of each feature
└── tests/
    ├── test_expense.py
    ├── test_tracker.py
    └── test_storage_and_cli.py
```

The code is split so each file has one job. `cli.py` handles the conversation with the user, `tracker.py` holds the rules, and `storage.py` is the only file that touches the data file. That way changing one part rarely breaks another.

---

## 5. Setup and Run

You need **Python 3** (tested on 3.12 and 3.13). Nothing else.

### Step 1: Check that Python is installed
Open **PowerShell** or **cmd** and type:
```
python --version
```
You should see something like `Python 3.13.x`. If Windows says Python isn't recognised, try `py --version`. If that fails too, install Python from [python.org](https://www.python.org/downloads/) and **tick "Add python.exe to PATH"** on the first installer screen. Then close and reopen your terminal.

### Step 2: Get the project
Pick one:

**Option A: download the ZIP.** On the GitHub page click **Code → Download ZIP**, then right-click the file and choose **Extract All**.

**Option B: clone with Git.** On the GitHub page click the green **Code** button, copy the HTTPS link, then run:
```
git clone <the link you copied>
```

### Step 3: Open a terminal in the project folder
Move into the folder that contains `main.py`. For example:

PowerShell:
```
cd ~\Desktop\coinlog
```
cmd:
```
cd %USERPROFILE%\Desktop\coinlog
```
Type `dir` to check. You should see `main.py`, `README.md`, and the `coinlog` and `tests` folders. (If your Desktop is synced with OneDrive, the path may be `OneDrive\Desktop\coinlog` instead.)

### Step 4: Run it
```
python main.py
```
On Windows, `py main.py` works too. You'll see the CoinLog banner and the main menu. Type a number and press Enter. Type `0` to quit.

There's no configuration to do. The `data` folder and `expenses.json` file are created the first time you run it.

### Using it: a quick walkthrough
| Option | What it does |
|:--:|---|
| 1 | Add an expense |
| 2 | View all expenses |
| 3 | View expenses by category |
| 4 | View expenses by month |
| 5 | View expenses by date |
| 6 | View expenses by date range |
| 7 | Update an expense |
| 8 | Delete an expense |
| 9 | Monthly summary report |
| 10 | Overall summary and category breakdown |
| 11 | Set a monthly budget for a category |
| 12 | View budget status |
| 0 | Exit |

Valid categories: `food`, `transport`, `shopping`, `health`, `education`, `entertainment`, `utilities`, `other`.
Dates are typed as `YYYY-MM-DD` and months as `YYYY-MM`.

---

## 6. Testing Instructions

The project comes with **37 automated tests**. From the project folder (the one containing `main.py`), run:

```
python -m unittest discover
```

You should see a line like `Ran 37 tests` followed by `OK`. This takes a few seconds. For a detailed list of every test as it runs, add `-v`:

```
python -m unittest discover -v
```

**What the tests cover:**

| File | Tests | What it checks |
|---|:--:|---|
| `tests/test_expense.py` | 10 | An expense rejects bad amounts, dates and categories, and survives being saved and loaded |
| `tests/test_tracker.py` | 13 | Adding, updating, deleting, filtering, totals, budgets and reports |
| `tests/test_storage_and_cli.py` | 14 | Every module imports cleanly, a damaged data file is recovered, data survives a restart, screens render with and without data, the real menu handles bad input, and colours turn off when they should |

The tests use temporary files, so **running them never touches your real expense data.**

---

## 7. Screenshots

Below is output from a real run of CoinLog. The answers you type are shown after each prompt. (Colours don't show in plain text, but they appear in the terminal.)

**Adding an expense**
```
  ── Add New Expense ──
  Amount (₹): 250
  Category ['food', 'transport', 'shopping', 'health', 'education', 'entertainment', 'utilities', 'other']: food
  Description (optional) []: Lunch at canteen
  Date (YYYY-MM-DD, leave blank for today): 2026-09-10

  ✔  Expense #1 — ₹250.00 [food] added.
```

**Viewing all expenses**
```
──────────────────────────────────────────────────────────────────────
  All Expenses (3 entries) — Total: ₹1510.00
──────────────────────────────────────────────────────────────────────
  #3  ₹60.00  [TRANSPORT]  2026-09-14
       Auto to campus

  #2  ₹1200.00  [SHOPPING]  2026-09-12
       Headphones

  #1  ₹250.00  [FOOD]  2026-09-10
       Lunch at canteen
```

**Monthly report with a budget warning**
```
──────────────────────────────────────────────────────────────────────
  📅  Monthly Report — 2026-09
──────────────────────────────────────────────────────────────────────
  Food            Spent: ₹250.00  Budget: ₹200.00 ⚠ OVER BUDGET
  Transport       Spent: ₹60.00  No budget set
  Shopping        Spent: ₹1200.00  No budget set
──────────────────────────────────────────────────────────────────────
  TOTAL SPENT       ₹1510.00
──────────────────────────────────────────────────────────────────────
```

**Budget status**
```
──────────────────────────────────────────────────────────────────────
  🎯  Budget Status — 2026-09
──────────────────────────────────────────────────────────────────────
  Food           [████████████████████] ₹250.00/₹200.00 OVER!
──────────────────────────────────────────────────────────────────────
```

**Test run**
```
Ran 37 tests in 4.119s

OK
```

---

## 8. Design Diagrams

These diagrams were drawn from the actual code and are in `docs/diagrams/`.

**System architecture**

![System architecture](docs/diagrams/architecture.png)

**Use case diagram**

![Use case diagram](docs/diagrams/usecase.png)

**Workflow diagram**

![Workflow diagram](docs/diagrams/workflow.png)

**Sequence diagram (adding an expense)**

![Sequence diagram](docs/diagrams/sequence.png)

**Class diagram**

![Class diagram](docs/diagrams/classes.png)

**Data storage (ER) diagram**

![ER diagram](docs/diagrams/er.png)

## Schema Design

CoinLog stores data as JSON rather than a database, so there are no formal tables — but the
JSON has a fixed shape, described below exactly as the code builds it (see `expense.py` and
`storage.py`).

**`data/expenses.json` — top-level object**

| Key | Type | Description |
|---|---|---|
| `expenses` | array of objects | every expense record (see below) |
| `budgets` | object (map) | category name → budget limit |
| `next_id` | integer | counter used to give each new expense a unique id |

**Each object inside `expenses`**

| Field | Type | Constraints |
|---|---|---|
| `expense_id` | integer | unique, auto-assigned, never reused even after a delete |
| `amount` | float | must be greater than 0; stored rounded to 2 decimal places |
| `category` | string | must be one of: food, transport, shopping, health, education, entertainment, utilities, other |
| `description` | string | optional, defaults to `""` |
| `date` | string | format `YYYY-MM-DD`; defaults to today if left blank |
| `created_at` | string | format `YYYY-MM-DD HH:MM:SS`, set automatically when the entry is added |

**Each entry inside `budgets`**

| Field | Type | Constraints |
|---|---|---|
| key | string | a category name (same fixed list as above) |
| value | float | must be greater than 0 |

**Example record**
```json
{
  "expense_id": 1,
  "amount": 250.0,
  "category": "food",
  "description": "Lunch at canteen",
  "date": "2026-09-10",
  "created_at": "2026-09-10 13:42:07"
}
```


---

## 9. Known Limitations and Future Ideas

- Amounts are in rupees (₹) and there is a single user with a single data file.
- The list of categories is fixed at eight.
- Budgets are monthly and apply to one category at a time.

Ideas for later: export to CSV, search by description, recurring expenses, editing budgets from the report screen, and a graphical interface.

---

## Author

**Gautham**, VIT Bhopal
Built for the Python Essentials course on VITyarthi.
