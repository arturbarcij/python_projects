"""
Python practice sheet 2.

Part 1 (problems 1-4): same tools as sheet 1, one step harder.
Part 2 (problems 5-8): classes, a subclass, a stack, and an algorithm inside a class.

How to use:
  1. Replace each `pass` with your solution.
  2. Run:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice2.py
     One problem:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice2.py 3

Each problem prints PASS or FAIL with the input that broke it.
Rule: no peeking at the hints until you have tried for 2 minutes.
"""
from abc import ABC, abstractmethod
from functools import singledispatchmethod
import sys


# ---------------------------------------------------------------- 1
def first_unique_char(s: str) -> int:
    """Index of the first character that appears once. -1 if every character repeats.
    'leetcode' -> 0, 'loveleetcode' -> 2, 'aabb' -> -1."""
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
        
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
    # hint: count every character, then scan s again for a count of 1


# ---------------------------------------------------------------- 2
def is_anagram(a: str, b: str) -> bool:
    """True when a and b are anagrams of each other."""
    return sorted(a) == sorted(b)
    # hint: sorted(a) == sorted(b)


# ---------------------------------------------------------------- 3
def binary_search(nums: list, target: int) -> int:
    """nums is sorted ascending. Return the index of target, or -1.
    Do not use list.index."""
    lo = 0
    hi = len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
  
        else:
            hi = mid - 1
    return - 1
    # hint: lo and hi, mid = (lo + hi) // 2, then move lo or hi


# ---------------------------------------------------------------- 4
def valid_parentheses(s: str) -> bool:
    """True when (), [], and {} are balanced and properly nested.
    '' and '()[]{}' and '{[]}' are valid. '(]' and '([)]' are not."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack[-1] != pairs[ch]:
            return False
        else:
            stack.pop()
    return not stack
    # hint: a list is a stack. push openers, pop when you see a closer


# ---------------------------------------------------------------- 5
class WordCounter:
    """Same word rules as count_words: split on whitespace, lowercase.
    most_common returns the word with the highest count.
    The tests have a single winner. An empty text has counts {} and most_common ''."""

    def __init__(self, text: str):
        self.text = text

    def counts(self) -> dict:
        counts = {}
        for word in self.text.lower().split():
            counts[word] = counts.get(word, 0) + 1
        return counts
        # hint: save text on self, then the count_words loop

    def most_common(self) -> str:
        winner = ""
        highest = 0
        for word, n in self.counts().items():
            if n > highest:
                winner = word
                highest = n
        return winner
        # hint: walk self.counts() and keep the word with the bigger number


# ---------------------------------------------------------------- 6
class Shape(ABC):
    @abstractmethod
    def area(self):
        """Return the area of this shape."""
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
        # hint: width * height, stored on self


class Square(Rectangle):
    """A square is a rectangle whose sides are equal."""

    def __init__(self, side):
        super().__init__(side, side)
        # hint: super().__init__(side, side)


# ---------------------------------------------------------------- 7
class Stack:
    """Last in, first out. peek looks at the top without removing it.
    pop returns the top item. is_empty is True only when nothing is stored."""

    def __init__(self):
        self._items = []
        # hint: self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items


# ---------------------------------------------------------------- 8
class AnagramGrouper:
    """Group words once in __init__. partners(word) returns that word's group.
    A missing word returns []. Group order does not matter; tests sort it."""

    def __init__(self, words: list):
        self.groups = {}
        for word in words:
            key = "".join(sorted(word))
            self.groups.setdefault(key, []).append(word)
        # hint: same sorted-letter key as group_anagrams, saved on self

    def partners(self, word: str) -> list:
        key = "".join(sorted(word))
        return self.groups.get(key, [])


# ================================================================ tests
def _check(name, got, expected):
    if got != expected:
        print(f"FAIL {name}\n      expected {expected!r}\n      got      {got!r}")
        return False
    return True


def _run_word_counter():
    name = "Problem 5"
    cases = [
        ("a b A", {"a": 2, "b": 1}, "a"),
        ("", {}, ""),
        ("x  x   x", {"x": 3}, "x"),
        ("bb aa aa", {"bb": 1, "aa": 2}, "aa"),
    ]
    for text, counts, common in cases:
        counter = WordCounter(text)
        if not _check(f"{name}: WordCounter({text!r}).counts()", counter.counts(), counts):
            return False
        if not _check(f"{name}: WordCounter({text!r}).most_common()", counter.most_common(), common):
            return False
    print(f"PASS {name}: WordCounter")
    return True


def _run_shapes():
    name = "Problem 6"
    rect = Rectangle(3, 4)
    square = Square(5)
    checks = [
        (f"{name}: Rectangle(3, 4).area()", rect.area(), 12),
        (f"{name}: Rectangle(0, 5).area()", Rectangle(0, 5).area(), 0),
        (f"{name}: Square(5).area()", square.area(), 25),
        (f"{name}: isinstance(Square(5), Rectangle)", isinstance(square, Rectangle), True),
        (f"{name}: isinstance(Square(5), Shape)", isinstance(square, Shape), True),
    ]
    for label, got, expected in checks:
        if not _check(label, got, expected):
            return False
    print(f"PASS {name}: Rectangle and Square")
    return True


def _run_stack():
    name = "Problem 7"
    stack = Stack()
    if not _check(f"{name}: new Stack().is_empty()", stack.is_empty(), True):
        return False
    stack.push("a")
    stack.push("b")
    if not _check(f"{name}: peek()", stack.peek(), "b"):
        return False
    if not _check(f"{name}: is_empty() after push", stack.is_empty(), False):
        return False
    if not _check(f"{name}: pop()", stack.pop(), "b"):
        return False
    if not _check(f"{name}: pop()", stack.pop(), "a"):
        return False
    if not _check(f"{name}: is_empty() after pops", stack.is_empty(), True):
        return False
    print(f"PASS {name}: Stack")
    return True


def _run_anagram_grouper():
    name = "Problem 8"
    grouper = AnagramGrouper(["eat", "tea", "tan", "ate", "nat", "bat"])
    cases = [
        ("eat", ["ate", "eat", "tea"]),
        ("tan", ["nat", "tan"]),
        ("bat", ["bat"]),
        ("xyz", []),
    ]
    for word, expected in cases:
        got = grouper.partners(word)
        if got is None or sorted(got) != expected:
            print(f"FAIL {name}: partners({word!r})\n      expected {expected!r}\n      got      {got!r}")
            return False
    empty = AnagramGrouper([""]).partners("")
    if empty is None or sorted(empty) != [""]:
        print(f"FAIL {name}: partners('')\n      expected ['']\n      got      {empty!r}")
        return False
    print(f"PASS {name}: AnagramGrouper")
    return True


TESTS = {
    1: (first_unique_char, [
        (("leetcode",), 0),
        (("loveleetcode",), 2),
        (("aabb",), -1),
        (("a",), 0),
        (("",), -1),
    ]),
    2: (is_anagram, [
        (("eat", "tea"), True),
        (("rat", "car"), False),
        (("a", "ab"), False),
        (("", ""), True),
        (("listen", "silent"), True),
    ]),
    3: (binary_search, [
        (([1, 3, 5, 7, 9], 7), 3),
        (([1, 3, 5, 7, 9], 1), 0),
        (([1, 3, 5, 7, 9], 9), 4),
        (([1, 3, 5, 7, 9], 4), -1),
        (([], 1), -1),
        (([5], 5), 0),
    ]),
    4: (valid_parentheses, [
        (("()",), True),
        (("()[]{}",), True),
        (("{[]}",), True),
        (("",), True),
        (("(]",), False),
        (("([)]",), False),
        (("(",), False),
        (("(((",), False),
    ]),
}

CUSTOM = {
    5: _run_word_counter,
    6: _run_shapes,
    7: _run_stack,
    8: _run_anagram_grouper,
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
