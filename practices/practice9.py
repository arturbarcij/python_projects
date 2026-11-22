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
        pass

    def return_book(self, member: Member) -> None:
        pass


#################################################################
# Unit tests
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