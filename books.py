"""Books: US-01 add, US-02 list, US-03 edit and delete, US-04 search."""

import re

from storage import (ask, ask_int, available_copies, confirm, copies_on_loan,
                     find_book, new_id, print_table, save_data)


# =========================================================
# US-01: Add a book  (validate_book is also used by US-03)
# =========================================================


# =========================================================
# US-02: List all books
# =========================================================
def book_rows(db, books):
    return [[b["id"], b["title"], b["author"], b["isbn"], b["category"] or "-",
             f'{available_copies(db, b)} / {b["copies"]}'] for b in books]


BOOK_HEADERS = ["ID", "Title", "Author", "ISBN", "Category", "Available / Total"]


def ui_list_books(db):
    print("\n--- All books ---")
    books = sorted(db["books"], key=lambda b: b["title"].lower())
    print_table(BOOK_HEADERS, book_rows(db, books))
