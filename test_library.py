"""Unit tests. Run with:  python -m unittest -v

Each test class matches a user story. Add the tests for a story
in the same pull request as its code.
"""

import os
import tempfile
import unittest
from datetime import date

import storage
from storage import sample_data


class LibraryTestCase(unittest.TestCase):
    """Uses a temporary data file so tests never touch real data."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        storage.DATA_FILE = self.tmp.name
        self.db = sample_data()

    def tearDown(self):
        os.remove(self.tmp.name)


class TestBooks(LibraryTestCase):  # US-01 to US-04
    def test_add_book(self):
        from books import add_book
        book = add_book(self.db, "Python Crash Course", "Eric Matthes", "978-1-59327-603-4", "Programming", 2)
        self.assertEqual(book["isbn"], "9781593276034")
        self.assertIn(book, self.db["books"])

    def test_invalid_and_duplicate_isbn_rejected(self):
        from books import add_book
        with self.assertRaises(ValueError):
            add_book(self.db, "X", "Y", "123", "", 1)
        with self.assertRaises(ValueError):
            add_book(self.db, "X", "Y", "9780132350884", "", 1)


class TestMembers(LibraryTestCase):  # US-05
    def test_add_member_and_reject_duplicate_email(self):
        from members import add_member
        add_member(self.db, "Sara Ali", "sara@example.com")
        with self.assertRaises(ValueError):
            add_member(self.db, "Sara Two", "SARA@example.com")

    def test_cannot_remove_member_with_loan(self):
        from loans import issue_book
        from members import remove_member
        issue_book(self.db, "M5", "B2")
        with self.assertRaises(ValueError):
            remove_member(self.db, "M5")


class TestLoans(LibraryTestCase):  # US-06 to US-08
    def test_issue_sets_due_date_and_reduces_copies(self):
        from loans import issue_book
        loan = issue_book(self.db, "M4", "B2", on_date=date(2026, 11, 1))
        self.assertEqual(loan["due_date"], "2026-11-15")
        self.assertEqual(storage.available_copies(self.db, storage.find_book(self.db, "B2")), 1)

    def test_loan_limit(self):
        from loans import issue_book
        for book_id in ["B1", "B2", "B3"]:
            issue_book(self.db, "M4", book_id)
        self.db["books"].append({"id": "B9", "title": "T", "author": "A",
                                 "isbn": "1234567890", "category": "", "copies": 1})
        with self.assertRaises(ValueError):
            issue_book(self.db, "M4", "B9")

    def test_late_return_fine(self):
        from loans import issue_book, return_book
        loan = issue_book(self.db, "M4", "B1", on_date=date(2026, 11, 1))
        fine = return_book(self.db, loan["id"], on_date=date(2026, 11, 20))  # due 15th, 5 days late
        self.assertEqual(fine, 50)


if __name__ == "__main__":
    unittest.main()
