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
