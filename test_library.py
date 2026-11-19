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


if __name__ == "__main__":
    unittest.main()
