"""Members: US-05 register, list and remove members."""

import re

from storage import (active_loans, ask, confirm, find_member, new_id,
                     print_table, save_data)


# =========================================================
# US-05: Register and manage members
# =========================================================
def add_member(db, name, email, phone=""):
    email = email.strip().lower()
    if not name or not email:
        raise ValueError("Name and email are required.")
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Please enter a valid email address.")
    if any(m["email"] == email for m in db["members"]):
        raise ValueError("A member with this email already exists.")
    member = {"id": new_id(db, "M"), "name": name, "email": email, "phone": phone}
    db["members"].append(member)
    save_data(db)
    return member


def remove_member(db, member_id):
    member = find_member(db, member_id)
    if member is None:
        raise ValueError(f"No member with ID {member_id}.")
    if any(loan["member_id"] == member["id"] for loan in active_loans(db)):
        raise ValueError(f'{member["name"]} still has books on loan and cannot be removed.')
    db["members"].remove(member)
    save_data(db)
    return member


def ui_add_member(db):
    print("\n--- Register a member ---")
    name = ask("Full name")
    email = ask("Email")
    phone = ask("Phone (optional)", required=False)
    try:
        member = add_member(db, name, email, phone)
        print(f'{member["name"]} registered with ID {member["id"]}.')
    except ValueError as e:
        print(f"Error: {e}")


def ui_list_members(db):
    print("\n--- Members ---")
    rows = []
    for m in sorted(db["members"], key=lambda m: m["name"].lower()):
        loans = sum(1 for loan in active_loans(db) if loan["member_id"] == m["id"])
        rows.append([m["id"], m["name"], m["email"], m["phone"] or "-", loans])
    print_table(["ID", "Name", "Email", "Phone", "Active loans"], rows)


def ui_remove_member(db):
    print("\n--- Remove a member ---")
    member = find_member(db, ask("Member ID"))
    if member is None:
        print("Error: no member with that ID.")
        return
    if not confirm(f'Remove {member["name"]}?'):
        print("Cancelled.")
        return
    try:
        remove_member(db, member["id"])
        print(f'{member["name"]} removed.')
    except ValueError as e:
        print(f"Error: {e}")
