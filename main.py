"""SHARED: Library Management System - main menu.

Run with:  python main.py
Each menu option points to a feature function. If a story has not been
built yet, its option prints "Not built yet" instead of crashing.
"""

import importlib
from storage import load_data

MENU = [
    ("Dashboard",           "dashboard", "ui_dashboard"),      # US-09
    ("Add a book",          "books",     "ui_add_book"),       # US-01
    ("List all books",      "books",     "ui_list_books"),     # US-02
    ("Edit a book",         "books",     "ui_edit_book"),      # US-03
    ("Delete a book",       "books",     "ui_delete_book"),    # US-03
    ("Search books",        "books",     "ui_search_books"),   # US-04
    ("Register a member",   "members",   "ui_add_member"),     # US-05
    ("List members",        "members",   "ui_list_members"),    # US-05
    ("Remove a member",     "members",   "ui_remove_member"),  # US-05
    ("Issue a book",        "loans",     "ui_issue_book"),     # US-06
    ("Return a book",       "loans",     "ui_return_book"),    # US-07
    ("List loans",          "loans",     "ui_list_loans"),     # US-07
    ("List overdue loans",  "loans",     "ui_list_overdue"),   # US-08
    ("Reset sample data",   "dashboard", "ui_reset"),          # US-09
]


def get_feature(module_name, function_name):
    """Return the feature function, or None if it is not built yet."""
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return None
    return getattr(module, function_name, None)


def main():
    db = load_data()
    while True:
        print("\n===== Library Management System =====")
        for number, (label, _, _) in enumerate(MENU, start=1):
            print(f"{number:>2}. {label}")
        print(" 0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break
        if not choice.isdigit() or not 1 <= int(choice) <= len(MENU):
            print("Please enter a number from the menu.")
            continue

        label, module_name, function_name = MENU[int(choice) - 1]
        feature = get_feature(module_name, function_name)
        if feature is None:
            print(f'"{label}" is not built yet.')
        else:
            feature(db)


if __name__ == "__main__":
    main()
