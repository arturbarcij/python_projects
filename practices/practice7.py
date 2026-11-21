"""
Python practice sheet 7.

Each problem states what the code must do. The solution is yours.
Ask for a hint when you want one.

How to use:
  1. Replace each `pass` with your solution.
  2. Run:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice7.py
     One problem:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice7.py 1

Each problem prints PASS or FAIL.
"""
from multiprocessing import Value
import queue
from typing import Any


from abc import ABC, abstractmethod
from collections import deque
import sys
import itertools

# ---------------------------------------------------------------- 1
def shared(a: list, b: list) -> list:
    """Values that appear in both lists.
    Each value appears once, in the order of its first appearance in a.
    shared([1, 2, 2, 3], [3, 2, 4]) is [2, 3].
    shared([], [1]) is []."""
    
    in_b = set(b)
    seen = set()
    result = []
    for n in a:
        if n in in_b and n not in seen:
            result.append(n)
            seen.add(n)
    return result

# ---------------------------------------------------------------- 2
def apply_each(nums: list, fn) -> list:
    """A new list of fn(n) for every n, in the same order.
    The original nums is left unchanged.
    apply_each([1, 2, 3], lambda n: n * 2) is [2, 4, 6].
    apply_each([], lambda n: n) is []."""
    return [fn(n) for n in nums]


# ---------------------------------------------------------------- 3
class Bag:
    """A collection of names. Each name is stored once.
    len(bag) is how many names are stored.
    `name in bag` is True when that name was added."""

    def __init__(self):
        self._names = set()

    def add(self, name: str) -> None:
        self._names.add(name)

    def __len__(self) -> int:
        return len(self._names)

    def __contains__(self, name: str) -> bool:
        return name in self._names


# ---------------------------------------------------------------- 4
class Task:
    """A task with a title and a priority. A smaller priority comes first."""

    def __init__(self, title: str, priority: int):
        self._title = title
        self._priority = priority


def titles_by_priority(tasks: list) -> list:
    """Titles ordered by priority, smallest first.
    Equal priorities stay in their original order.
    titles_by_priority([]) is []."""
    ordered = sorted(tasks, key=lambda task: task._priority)
    return [task._title for task in ordered]


# ---------------------------------------------------------------- 5
class Recorder:
    """Records what a with-block does.
    events starts as an empty list.
    Entering the block appends "enter". The name after `as` is this recorder.
    note(message) appends message.
    Leaving the block appends "exit", including when the block raises.
    An error inside the block still propagates after the block ends."""

    def __init__(self):
        self.events = []

    def note(self, message: str) -> None:
        self.events.append(message)

    def __enter__(self):
        self.events.append("enter")
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.events.append("exit")


# ---------------------------------------------------------------- 6
def flatten(items: list) -> list:
    """One flat list. Nested lists are expanded. Every other value stays whole.
    flatten([1, [2, [3], 4], 5]) is [1, 2, 3, 4, 5].
    flatten([]) is [].
    flatten([[]]) is [].
    flatten(["ab", ["c"]]) is ["ab", "c"]."""
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


# ---------------------------------------------------------------- 7
class Rule(ABC):
    """Decides whether a number is allowed."""

    @abstractmethod
    def allow(self, number: int) -> bool:
        self._number = number


class Positive(Rule):
    """Allows numbers greater than 0."""

    def allow(self, number: int) -> bool:
        return number > 0


class Below(Rule):
    """Allows numbers strictly less than limit."""

    def __init__(self, limit: int):
        self._limit = limit

    def allow(self, number: int) -> bool:
        return number < self._limit


class Gate:
    """Keeps the numbers its rule allows. The gate does not decide the rule."""

    def __init__(self, rule: Rule):
        self._rule = rule

    def keep(self, nums: list) -> list:
        """The allowed numbers, in the same order."""
        kept = []
        for number in nums:
            if self._rule.allow(number):
                kept.append(number)
        return kept


# ---------------------------------------------------------------- 8
class DequeQueue:
    """A first-in, first-out queue.
    self._items is a collections.deque and holds the elements.
    enqueue(item) adds to the back.
    dequeue() returns the front element.
    dequeue() on an empty queue raises ValueError."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item) -> None:
        self._items.append(item)

    def dequeue(self):
        if len(self._items) == 0:
            raise ValueError("empty")
        return self._items.popleft()


# ================================================================ tests
def _check(name, got, expected):
    if got != expected:
        print(f"FAIL {name}\n      expected {expected!r}\n      got      {got!r}")
        return False
    return True


def _raises(name, fn, error):
    try:
        fn()
    except error:
        return True
    except Exception as e:
        print(f"FAIL {name}: raised {type(e).__name__}, expected {error.__name__}")
        return False
    print(f"FAIL {name}: expected {error.__name__}")
    return False


def _run_shared():
    name = "Problem 1"
    if not _check(f"{name}: both", shared([1, 2, 2, 3], [3, 2, 4]), [2, 3]):
        return False
    if not _check(f"{name}: empty", shared([], [1]), []):
        return False
    if not _check(f"{name}: once", shared([1, 1], [1]), [1]):
        return False
    if not _check(f"{name}: order from a", shared([3, 1, 2], [2, 3]), [3, 2]):
        return False
    if not _check(f"{name}: only from a", shared([1], [1, 2]), [1]):
        return False
    print(f"PASS {name}: shared")
    return True


def _run_apply_each():
    name = "Problem 2"
    nums = [1, 2, 3]
    if not _check(f"{name}: double", apply_each(nums, lambda n: n * 2), [2, 4, 6]):
        return False
    if not _check(f"{name}: unchanged", nums, [1, 2, 3]):
        return False
    if not _check(f"{name}: empty", apply_each([], lambda n: n), []):
        return False
    if not _check(f"{name}: strings", apply_each([1, 2], str), ["1", "2"]):
        return False
    print(f"PASS {name}: apply_each")
    return True


def _run_bag():
    name = "Problem 3"
    bag = Bag()
    if not _check(f"{name}: empty len", len(bag), 0):
        return False
    if not _check(f"{name}: missing", "a" in bag, False):
        return False
    bag.add("a")
    bag.add("a")
    bag.add("b")
    if not _check(f"{name}: len", len(bag), 2):
        return False
    if not _check(f"{name}: has a", "a" in bag, True):
        return False
    if not _check(f"{name}: has b", "b" in bag, True):
        return False
    if not _check(f"{name}: no c", "c" in bag, False):
        return False
    print(f"PASS {name}: Bag")
    return True


def _run_tasks():
    name = "Problem 4"
    tasks = [Task("write", 2), Task("fix", 1), Task("read", 2)]
    if not _check(f"{name}: titles", titles_by_priority(tasks), ["fix", "write", "read"]):
        return False
    if not _check(f"{name}: empty", titles_by_priority([]), []):
        return False
    if not _check(f"{name}: one", titles_by_priority([Task("only", 4)]), ["only"]):
        return False
    print(f"PASS {name}: titles_by_priority")
    return True


def _run_recorder():
    name = "Problem 5"
    recorder = Recorder()
    with recorder as active:
        if active is not recorder:
            print(f"FAIL {name}: the name after as should be the recorder")
            return False
        active.note("work")
    if not _check(f"{name}: events", recorder.events, ["enter", "work", "exit"]):
        return False
    broken = Recorder()
    try:
        with broken:
            raise ValueError("boom")
    except ValueError:
        pass
    else:
        print(f"FAIL {name}: expected ValueError")
        return False
    if not _check(f"{name}: exit after error", broken.events, ["enter", "exit"]):
        return False
    print(f"PASS {name}: Recorder")
    return True


def _run_flatten():
    name = "Problem 6"
    if not _check(f"{name}: nested", flatten([1, [2, [3], 4], 5]), [1, 2, 3, 4, 5]):
        return False
    if not _check(f"{name}: empty", flatten([]), []):
        return False
    if not _check(f"{name}: empty nested", flatten([[]]), []):
        return False
    if not _check(f"{name}: flat", flatten([1, 2]), [1, 2]):
        return False
    if not _check(f"{name}: string stays whole", flatten(["ab", ["c"]]), ["ab", "c"]):
        return False
    print(f"PASS {name}: flatten")
    return True


def _run_gate():
    name = "Problem 7"
    if not _raises(f"{name}: Rule()", lambda: Rule(), TypeError):
        return False
    if not _check(f"{name}: Positive is a Rule", isinstance(Positive(), Rule), True):
        return False
    if not _check(f"{name}: Below is a Rule", isinstance(Below(3), Rule), True):
        return False
    if not _check(f"{name}: positive", Gate(Positive()).keep([-2, 0, 1, 4]), [1, 4]):
        return False
    if not _check(f"{name}: below", Gate(Below(3)).keep([1, 3, 2, 0]), [1, 2, 0]):
        return False
    if not _check(f"{name}: empty", Gate(Positive()).keep([]), []):
        return False
    print(f"PASS {name}: Gate")
    return True


def _run_queue():
    name = "Problem 8"
    queue = DequeQueue()
    if not isinstance(queue._items, deque):
        print(f"FAIL {name}: self._items should be a collections.deque")
        print(f"      got {type(getattr(queue, '_items', None)).__name__}")
        return False
    queue.enqueue("a")
    queue.enqueue("b")
    if not _check(f"{name}: first", queue.dequeue(), "a"):
        return False
    if not _check(f"{name}: second", queue.dequeue(), "b"):
        return False
    if not _raises(f"{name}: empty", queue.dequeue, ValueError):
        return False
    queue.enqueue(1)
    queue.dequeue()
    queue.enqueue(2)
    queue.enqueue(3)
    if not _check(f"{name}: after reuse", queue.dequeue(), 2):
        return False
    if not _check(f"{name}: last", queue.dequeue(), 3):
        return False
    print(f"PASS {name}: DequeQueue")
    return True


CUSTOM = {
    1: _run_shared,
    2: _run_apply_each,
    3: _run_bag,
    4: _run_tasks,
    5: _run_recorder,
    6: _run_flatten,
    7: _run_gate,
    8: _run_queue,
}


def run(num):
    name = f"Problem {num}"
    try:
        return CUSTOM[num]()
    except Exception as e:
        print(f"FAIL {name}: raised {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or sorted(CUSTOM)
    results = [run(n) for n in which]
    print(f"\n{sum(results)}/{len(results)} passed")
