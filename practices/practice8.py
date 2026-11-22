# Practice 8. A work desk, in one file.
#
# You add tasks to a waiting line. This first slice only covers arrival:
# the line remembers titles in the order they were added.
#
# Later slices, still in this file:
#   serve the front of the line
#   undo the last serve with a stack
#   list titles by priority
#   tags, matched with a set
#   a rule object that filters tasks
#   a with-block that records the work session
#
# Run:  python practice8.py
#
# Task: title is a non-empty string. priority is an int of 1 or more.
# A smaller priority is more urgent.
# An empty title or a priority below 1 raises ValueError.
#
# Desk: a waiting line of tasks. Titles are unique.
# add puts a task at the back.
# Adding a title that is already waiting raises ValueError.
# waiting returns the titles from the front of the line to the back.
#
# First test, arrival order:
#   a new desk has an empty line
#   add "write" at priority 2, then "fix" at priority 1
#   the line is ["write", "fix"] because this slice is arrival order
#   adding "write" again raises ValueError and the line stays unchanged
#   Task("", 1) raises ValueError
#   Task("read", 0) raises ValueError
from collections import deque

class Task:
    
    def __init__(self, title, priority):
        if len(title) == 0:
            raise ValueError("empty")
        if priority < 1:
            raise ValueError("priority msut be 1 or more")
        self._title = title
        self._priority = priority

class Desk:

    def __init__(self):
        self._line = deque()
    
    def add(self, task):
        for waiting in self._line:
            if waiting._title == task._title:
                raise ValueError("title already waiting")
        self._line.append(task)
    
    def waiting(self):
        return [task._title for task in self._line]


# A unit test builds a situation, calls your code, and checks one result.
# assertEqual fails when the two values differ.
# assertRaises fails when the call does not raise that error.
import unittest


class ArrivalOrderTest(unittest.TestCase):
    def test_line_starts_empty(self):
        desk = Desk()
        self.assertEqual(desk.waiting(), [])

    def test_arrival_order_ignores_priority(self):
        desk = Desk()
        desk.add(Task("write", 2))
        desk.add(Task("fix", 1))
        self.assertEqual(desk.waiting(), ["write", "fix"])

    def test_duplicate_title_leaves_the_line_unchanged(self):
        desk = Desk()
        desk.add(Task("write", 2))
        desk.add(Task("fix", 1))
        with self.assertRaises(ValueError):
            desk.add(Task("write", 3))
        self.assertEqual(desk.waiting(), ["write", "fix"])

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            Task("", 1)

    def test_priority_below_one(self):
        with self.assertRaises(ValueError):
            Task("read", 0)


if __name__ == "__main__":
    unittest.main()

