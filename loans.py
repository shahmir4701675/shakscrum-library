"""Loans: US-06 issue, US-07 return, US-08 overdue loans and fines."""

from datetime import date, timedelta

from storage import (FINE_PER_DAY, LOAN_DAYS, MAX_LOANS, active_loans, ask, available_copies,
                     find_book, find_member, new_id, print_table, save_data, today)


# =========================================================
# US-06: Issue a book to a member
# =========================================================
def issue_book(db, member_id, book_id, on_date=None):
    member = find_member(db, member_id)
    book = find_book(db, book_id)
    if member is None:
        raise ValueError(f"No member with ID {member_id}.")
    if book is None:
        raise ValueError(f"No book with ID {book_id}.")
    member_loans = [loan for loan in active_loans(db) if loan["member_id"] == member["id"]]
    if len(member_loans) >= MAX_LOANS:
        raise ValueError(f'{member["name"]} already has {MAX_LOANS} books on loan.')
    if any(loan["book_id"] == book["id"] for loan in member_loans):
        raise ValueError(f'{member["name"]} already has a copy of "{book["title"]}".')
    if available_copies(db, book) < 1:
        raise ValueError(f'No copies of "{book["title"]}" are available.')

    issued = on_date or today()
    loan = {"id": new_id(db, "L"), "book_id": book["id"], "member_id": member["id"],
            "issue_date": issued.isoformat(),
            "due_date": (issued + timedelta(days=LOAN_DAYS)).isoformat(),
            "return_date": None}
    db["loans"].append(loan)
    save_data(db)
    return loan


def ui_issue_book(db):
    print("\n--- Issue a book ---")
    member_id = ask("Member ID")
    book_id = ask("Book ID")
    try:
        loan = issue_book(db, member_id, book_id)
        title = find_book(db, loan["book_id"])["title"]
        print(f'"{title}" issued (loan {loan["id"]}). Due {loan["due_date"]}.')
    except ValueError as e:
        print(f"Error: {e}")


# =========================================================
# US-07: Return a book
# =========================================================
def return_book(db, loan_id, on_date=None):
    loan = next((l for l in db["loans"] if l["id"] == loan_id.upper()), None)
    if loan is None:
        raise ValueError(f"No loan with ID {loan_id}.")
    if loan["return_date"] is not None:
        raise ValueError(f'Loan {loan["id"]} was already returned on {loan["return_date"]}.')
    loan["return_date"] = (on_date or today()).isoformat()
    save_data(db)
    return fine_for(loan)


def ui_return_book(db):
    print("\n--- Return a book ---")
    try:
        fine = return_book(db, ask("Loan ID"))
        print(f"Book returned. Fine due: Rs {fine}." if fine else "Book returned on time.")
    except ValueError as e:
        print(f"Error: {e}")


# =========================================================
# US-07 + US-08: Loan list, overdue loans and fines
# =========================================================
def days_late(loan, on_date=None):
    end = date.fromisoformat(loan["return_date"]) if loan["return_date"] else (on_date or today())
    return max(0, (end - date.fromisoformat(loan["due_date"])).days)


def fine_for(loan, on_date=None):
    return days_late(loan, on_date) * FINE_PER_DAY


def is_overdue(loan, on_date=None):
    return loan["return_date"] is None and days_late(loan, on_date) > 0


def loan_rows(db, loans):
    rows = []
    for loan in sorted(loans, key=lambda l: l["due_date"]):
        book = find_book(db, loan["book_id"])
        member = find_member(db, loan["member_id"])
        if loan["return_date"]:
            status = f'Returned {loan["return_date"]}'
        elif is_overdue(loan):
            status = f"OVERDUE by {days_late(loan)} day(s)"
        else:
            status = "On loan"
        rows.append([loan["id"], book["title"] if book else "(deleted book)",
                     member["name"] if member else "(removed member)",
                     loan["issue_date"], loan["due_date"], status, fine_for(loan)])
    return rows


LOAN_HEADERS = ["Loan", "Book", "Member", "Issued", "Due", "Status", "Fine (Rs)"]


def ui_list_loans(db):
    print("\n--- Loans ---")
    include_returned = ask("Include returned loans? (y/n)", required=False).lower() == "y"
    loans = db["loans"] if include_returned else active_loans(db)
    print_table(LOAN_HEADERS, loan_rows(db, loans))


def ui_list_overdue(db):
    print("\n--- Overdue loans ---")
    print_table(LOAN_HEADERS, loan_rows(db, [l for l in active_loans(db) if is_overdue(l)]))
