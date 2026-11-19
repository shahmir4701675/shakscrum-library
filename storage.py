"""SHARED: settings, data storage and helpers used by every feature."""

import json
import os
from datetime import date

# ---------- Settings ----------
DATA_FILE = "library_data.json"
LOAN_DAYS = 14      # a book is due 14 days after it is issued
MAX_LOANS = 3       # a member can borrow at most 3 books at once
FINE_PER_DAY = 10   # Rs 10 for each day a book is late


# ---------- Data storage ----------
def sample_data():
    return {
        "next_id": 6,
        "books": [
            {"id": "B1", "title": "Clean Code", "author": "Robert C. Martin",
             "isbn": "9780132350884", "category": "Programming", "copies": 3},
            {"id": "B2", "title": "Introduction to Algorithms", "author": "Cormen et al.",
             "isbn": "9780262046305", "category": "Algorithms", "copies": 2},
            {"id": "B3", "title": "Software Engineering", "author": "Ian Sommerville",
             "isbn": "9780133943030", "category": "Software Engineering", "copies": 4},
        ],
        "members": [
            {"id": "M4", "name": "Ayesha Khan", "email": "ayesha@example.com", "phone": "0300-1234567"},
            {"id": "M5", "name": "Bilal Ahmed", "email": "bilal@example.com", "phone": ""},
        ],
        "loans": [],
    }


def load_data(path=None):
    """Read the data file, or start with sample data if it does not exist."""
    path = path or DATA_FILE
    if not os.path.exists(path):
        return sample_data()
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: data file could not be read; starting with sample data.")
        return sample_data()


def save_data(db, path=None):
    with open(path or DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def new_id(db, prefix):
    new = f"{prefix}{db['next_id']}"
    db["next_id"] += 1
    return new


# ---------- Lookups ----------
def find_book(db, book_id):
    return next((b for b in db["books"] if b["id"] == book_id.upper()), None)


def find_member(db, member_id):
    return next((m for m in db["members"] if m["id"] == member_id.upper()), None)


def active_loans(db):
    return [loan for loan in db["loans"] if loan["return_date"] is None]


def copies_on_loan(db, book_id):
    return sum(1 for loan in active_loans(db) if loan["book_id"] == book_id)


def available_copies(db, book):
    return book["copies"] - copies_on_loan(db, book["id"])


def today():
    return date.today()


# ---------- Console helpers ----------
def ask(prompt, required=True):
    while True:
        value = input(f"{prompt}: ").strip()
        if value or not required:
            return value
        print("  This field is required.")


def ask_int(prompt, default=None):
    while True:
        raw = input(f"{prompt}{f' [{default}]' if default is not None else ''}: ").strip()
        if not raw and default is not None:
            return default
        if raw.isdigit():
            return int(raw)
        print("  Please enter a whole number.")


def confirm(prompt):
    return input(f"{prompt} (y/n): ").strip().lower() == "y"


def print_table(headers, rows):
    """Print rows as a simple text table."""
    if not rows:
        print("  (nothing to show)")
        return
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * len(line))
    for row in rows:
        print("  ".join(str(x).ljust(w) for x, w in zip(row, widths)))
