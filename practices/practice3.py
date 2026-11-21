"""
Python practice sheet 3.

Part 1 (problems 1-4): two pointers, then a sliding window.
Part 2 (problems 5-8): a queue, a linked list, binary search inside a class,
and a subclass.

How to use:
  1. Replace each `pass` with your solution.
  2. Run:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice3.py
     One problem:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice3.py 1

Each problem prints PASS or FAIL with the input that broke it.
Rule: no peeking at the hints until you have tried for 2 minutes.
"""
import collections
from collections.abc import Collection
import sys


# ---------------------------------------------------------------- 1
def is_palindrome(s: str) -> bool:
    """True when s reads the same forwards and backwards.
    Do not reverse the string with a slice. Compare from both ends.
    'racecar' and '' and 'a' are palindromes. 'ab' is not."""
    lo = 0
    hi = len(s) - 1
    
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True
    # hint: lo = 0, hi = len(s) - 1, move inward while s[lo] == s[hi]


# ---------------------------------------------------------------- 2
def two_sum_sorted(nums: list, target: int) -> list:
    """nums is sorted ascending. Return [i, j] (i < j) of the two values that add to target.
    Exactly one solution exists. Use two pointers, not a dictionary."""
    lo = 0
    hi = len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return [lo, hi]
        if total < target:
            lo += 1
        else:
            hi -= 1

        # hint: lo at the start, hi at the end. Sum too small: lo += 1. Sum too big: hi -= 1
    return []


# ---------------------------------------------------------------- 3
def merge_sorted(a: list, b: list) -> list:
    """Both lists are sorted ascending. Return one sorted list containing every item.
    [1, 3, 5] and [2, 4, 6] -> [1, 2, 3, 4, 5, 6]. Duplicates stay."""
    i = 0
    j = 0
    merged = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged

    # hint: one index per list. Append the smaller head, then advance that index


# ---------------------------------------------------------------- 4
def longest_unique(s: str) -> int:
    """Length of the longest substring with no repeated character.
    'abcabcbb' -> 3, 'bbbbb' -> 1, '' -> 0."""
    last = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best
    # hint: a window and a dict of character -> last index. When a repeat is inside the window, move the start


# ---------------------------------------------------------------- 5
class Queue:
    """First in, first out. enqueue adds at the back. dequeue removes the front.
    peek looks at the front without removing it. is_empty is True only when nothing is stored."""

    def __init__(self):
        self._items = []
        # hint: self._items = []

    def enqueue(self, item):
        self._items.append(item)
        

    def dequeue(self):
        return self._items.pop(0)
        # hint: pop(0) removes the front of a list

    def peek(self):
        return self._items[0]

    def is_empty(self) -> bool:
        return not self._items


# ---------------------------------------------------------------- 6
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    """append adds a node at the end. to_list returns the values from head to end.
    An empty list returns []."""

    def __init__(self):
        self.head = None
        # hint: self.head = None

    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

        # hint: if head is None, the new node is the head. Otherwise walk .next until it is None

    def to_list(self) -> list:
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values


# ---------------------------------------------------------------- 7
class SortedList:
    """add inserts a number so the stored values stay sorted ascending.
    contains uses binary search, not the `in` operator."""

    def __init__(self):
        self._nums = []
        # hint: self._nums = []

    def add(self, n):
        for i in range(len(self._nums)):
            if self._nums[i] > n:
                self._nums.insert(i, n)
                return
        self._nums.append(n)
        # hint: find the first index whose value is greater than n, then list.insert

    def contains(self, n) -> bool:
        lo = 0
        hi = len(self._nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self._nums[mid] == n:
                return True
            if self._nums[mid] < n:
                lo = mid + 1
            else:
                hi = mid - 1
        return False

    def values(self) -> list:
        return self._nums


# ---------------------------------------------------------------- 8
class LoggingQueue(Queue):
    """A queue that remembers every value dequeue has returned, in order.
    history starts as []. enqueue does not write to history."""

    def __init__(self):
        super().__init__()
        self.history = []
        # hint: super().__init__(), then self.history = []

    def dequeue(self):
        item = super().dequeue()
        self.history.append(item)
        return item
        # hint: item = super().dequeue(); append it to history; return it


# ================================================================ tests
def _check(name, got, expected):
    if got != expected:
        print(f"FAIL {name}\n      expected {expected!r}\n      got      {got!r}")
        return False
    return True


def _run_queue():
    name = "Problem 5"
    queue = Queue()
    if not _check(f"{name}: new Queue().is_empty()", queue.is_empty(), True):
        return False
    queue.enqueue("a")
    queue.enqueue("b")
    if not _check(f"{name}: peek()", queue.peek(), "a"):
        return False
    if not _check(f"{name}: is_empty() after enqueue", queue.is_empty(), False):
        return False
    if not _check(f"{name}: dequeue()", queue.dequeue(), "a"):
        return False
    if not _check(f"{name}: dequeue()", queue.dequeue(), "b"):
        return False
    if not _check(f"{name}: is_empty() after dequeues", queue.is_empty(), True):
        return False
    print(f"PASS {name}: Queue")
    return True


def _run_linked_list():
    name = "Problem 6"
    empty = LinkedList()
    if not _check(f"{name}: empty to_list()", empty.to_list(), []):
        return False
    linked = LinkedList()
    linked.append(1)
    linked.append(2)
    linked.append(3)
    if not _check(f"{name}: append 1, 2, 3", linked.to_list(), [1, 2, 3]):
        return False
    print(f"PASS {name}: LinkedList")
    return True


def _run_sorted_list():
    name = "Problem 7"
    ordered = SortedList()
    if not _check(f"{name}: empty values()", ordered.values(), []):
        return False
    if not _check(f"{name}: empty contains(1)", ordered.contains(1), False):
        return False
    for n in (5, 1, 3, 3):
        ordered.add(n)
    if not _check(f"{name}: values()", ordered.values(), [1, 3, 3, 5]):
        return False
    if not _check(f"{name}: contains(3)", ordered.contains(3), True):
        return False
    if not _check(f"{name}: contains(4)", ordered.contains(4), False):
        return False
    print(f"PASS {name}: SortedList")
    return True


def _run_logging_queue():
    name = "Problem 8"
    queue = LoggingQueue()
    if not _check(f"{name}: history starts empty", queue.history, []):
        return False
    queue.enqueue(1)
    queue.enqueue(2)
    if not _check(f"{name}: history after enqueue", queue.history, []):
        return False
    if not _check(f"{name}: dequeue()", queue.dequeue(), 1):
        return False
    if not _check(f"{name}: history", queue.history, [1]):
        return False
    if not _check(f"{name}: dequeue()", queue.dequeue(), 2):
        return False
    if not _check(f"{name}: history", queue.history, [1, 2]):
        return False
    if not _check(f"{name}: is_empty()", queue.is_empty(), True):
        return False
    print(f"PASS {name}: LoggingQueue")
    return True


TESTS = {
    1: (is_palindrome, [
        (("racecar",), True),
        (("abba",), True),
        (("ab",), False),
        (("",), True),
        (("a",), True),
        (("abca",), False),
    ]),
    2: (two_sum_sorted, [
        (([2, 7, 11, 15], 9), [0, 1]),
        (([1, 2, 4, 6], 6), [1, 2]),
        (([1, 2, 3], 4), [0, 2]),
        (([-1, 0, 1], 0), [0, 2]),
    ]),
    3: (merge_sorted, [
        (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
        (([], [1, 2]), [1, 2]),
        (([1], []), [1]),
        (([1, 2, 2], [2, 3]), [1, 2, 2, 2, 3]),
    ]),
    4: (longest_unique, [
        (("abcabcbb",), 3),
        (("bbbbb",), 1),
        (("pwwkew",), 3),
        (("",), 0),
        (("au",), 2),
        (("dvdf",), 3),
    ]),
}

CUSTOM = {
    5: _run_queue,
    6: _run_linked_list,
    7: _run_sorted_list,
    8: _run_logging_queue,
}


def run(num):
    name = f"Problem {num}"
    if num in CUSTOM:
        try:
            return CUSTOM[num]()
        except Exception as e:
            print(f"FAIL {name}: raised {type(e).__name__}: {e}")
            return False
    fn, cases = TESTS[num]
    for args, expected in cases:
        try:
            got = fn(*args)
        except Exception as e:
            print(f"FAIL {name}: {fn.__name__}{args} raised {type(e).__name__}: {e}")
            return False
        if got != expected:
            print(f"FAIL {name}: {fn.__name__}{args}\n      expected {expected!r}\n      got      {got!r}")
            return False
    print(f"PASS {name}: {fn.__name__}")
    return True


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or sorted(set(TESTS) | set(CUSTOM))
    results = [run(n) for n in which]
    print(f"\n{sum(results)}/{len(results)} passed")
