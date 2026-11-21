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

def Task():
    
    def __init__(self, title):
        self._title = title


def Desk():

    def __init__(self, desk):
    
    
