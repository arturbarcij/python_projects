from collections import deque

class Book:
    def __init__(self, title, year, tag) -> None:
        self._title = title
        self._year = year
        self._tag = tag
    
class Member:
    def __init__(self, name: str):
        pass

class Library:
    def __init__(self) -> None:
        self._book_list = deque()

    def add(self, book: Book) -> None:
        for current in self._book_list:
            if current._title == book._title:
                raise ValueError("title is already in the library")
        self._book_list.append(book)

    def titles(self) -> list:
        return [book._title for book in self._book_list]

    def checkout(self, member: Member, title: str) -> None:
        for book in self._book_list:
            if book._title == title:
                self._book_list.remove(book)
                member._loans.append(book)
                return
        raise ValueError("book is not on the shelf")

    def return_book(self, member: Member) -> None:
        if len(member._loans) == 0:
            raise ValueError("nothing to return")
        self._book_list.append(member._loans.pop())


#################################################################
# Unit tests
from multiprocessing import Value
import sys
import unittest

class ShelfTest(unittest.TestCase):
    def test_shelf_starts_empty(self):
        library = Library()
        self.assertEqual(library.titles(), [])
    
    def test_books_stay_in_arrival_order(self):
        library = Library()
        library.add(Book("Dune", 1965, "fiction"))
        library.add(Book("Emma", 1815, "fiction"))
        self.assertEqual(library.titles(), ["Dune", "Emma"])
    
    def test_duplicate_title_leaves_the_shelf_unchanged(self):
        library = Library()
        library.add(Book("Dune", 1965, "fiction"))
        with self.assertRaises(ValueError):
            library.add(Book("Dune", 2000, "fiction"))
        self.assertEqual(library.titles(), ["Dune"])


class CheckoutTest(unittest.TestCase):
    def test_checkout_moves_the_book_to_the_member(self):
        library = Library()
        member = Member("Ana")
        library.add(Book("Dune", 1965, "fiction"))
        library.add(Book("Emma", 1815, "fiction"))
        library.checkout(member, "Dune")
        self.assertEqual(library.titles(), ["Emma"])
        self.assertEqual(member.holding(), ["Dune"])

    def test_missing_book_stays_on_the_shelf(self):
        library = Library()
        library.add(Book("Dune", 1965, "fiction"))
        with self.assertRaises(ValueError):
            library.checkout(Member("Ana"), "Emma")
        self.assertEqual(library.titles(), ["Dune"])

    def test_return_puts_the_last_book_back(self):
        library = Library()
        member = Member("Ana")
        library.add(Book("Dune", 1965, "fiction"))
        library.add(Book("Emma", 1815, "fiction"))
        library.checkout(member, "Dune")
        library.checkout(member, "Emma")
        library.return_book(member)
        self.assertEqual(member.holding(), ["Dune"])
        self.assertEqual(library.titles(), ["Emma"])

    def test_return_with_no_loan_raises(self):
        with self.assertRaises(ValueError):
            Library().return_book(Member("Ana"))

class Report(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.total = 0

    def _mark(self, test, label):
        print(f"{label} ({self.testsRun}/{self.total}) {test._testMethodName}")

    def addSuccess(self, test):
        super().addSuccess(test)
        self._mark(test, "PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._mark(test, "FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        self._mark(test, "FAIL")


class Runner(unittest.TextTestRunner):
    def run(self, test):
        result = self._makeResult()
        result.total = test.countTestCases()
        test(result)
        result.printErrors()
        return result


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = Runner(resultclass=Report, verbosity=0).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"\n{passed}/{result.testsRun} passed")