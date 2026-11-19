"""Dashboard: US-09 key numbers at a glance."""

from loans import is_overdue
from storage import active_loans, confirm, sample_data, save_data


# =========================================================
# US-09: Dashboard
# =========================================================
def stats(db):
    loans = active_loans(db)
    return {
        "Book titles": len(db["books"]),
        "Total copies": sum(b["copies"] for b in db["books"]),
        "Members": len(db["members"]),
        "Books on loan": len(loans),
        "Overdue loans": sum(1 for l in loans if is_overdue(l)),
    }


def ui_dashboard(db):
    print("\n--- Dashboard ---")
    for label, value in stats(db).items():
        print(f"  {label:<15} {value}")


def ui_reset(db):
    if confirm("Delete all data and restore the sample data?"):
        db.clear()
        db.update(sample_data())
        save_data(db)
        print("Sample data restored.")
