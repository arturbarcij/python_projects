"""
Python practice sheet 6. A step past the bank accounts.

Problems 1-2 reuse encapsulation and inheritance.
Problem 3 adds __eq__ and __repr__.
Problem 4 is a generator.
Problem 5 is a custom exception.
Problem 6 is composition: an object that holds a list and uses it as a stack.
Problem 7 is an iterator.
Problem 8 combines polymorphism and composition.

How to use:
  1. Replace each `pass` with your solution.
  2. Run:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice6.py
     One problem:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice6.py 1

Each problem prints PASS or FAIL.
Rule: try for 2 minutes before reading the hint.
Errors are raised with the keyword raise.
"""
from abc import ABC, abstractmethod
from multiprocessing import current_process
from queue import Empty
import sys
import types


# ---------------------------------------------------------------- 1
class Counter:
    """Starts at start (default 0). tick adds 1. reset sets the value back to 0.
    value can be read and cannot be assigned."""

    def __init__(self, start: int = 0):
        self._value = start
        # hint: store start on self._value

    @property
    def value(self) -> int:
        return self._value
        # hint: return self._value

    def tick(self) -> None:
        self._value += 1
        # hint: add 1 to self._value

    def reset(self) -> None:
        self._value = 0
        # hint: set self._value back to 0


# ---------------------------------------------------------------- 2
class BoundedCounter(Counter):
    """A Counter that refuses to pass limit.
    tick raises ValueError when value is already equal to limit.
    reset is inherited and still sets the value to 0."""

    def __init__(self, limit: int, start: int = 0):
        super().__init__(start)
        self._limit = limit
        # hint: super().__init__(start), then store limit on self

    def tick(self) -> None:
        if self.value == self._limit:
            raise ValueError("amount is already equal to the limit")
        else:
            super().tick()
        # hint: if self.value == self.limit, raise ValueError. otherwise super().tick()


# ---------------------------------------------------------------- 3
class Point:
    """A point with x and y.
    Two points are equal when both numbers match.
    A point is not equal to a tuple or any other type.
    repr(Point(1, 2)) is the string 'Point(1, 2)'."""

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        # hint: store x and y on self

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self._x == other._x and self._y == other._y
        # hint: return False when other is not a Point. compare x and y

    def __repr__(self) -> str:
        return f"Point({self._x}, {self._y})"
        # hint: return f"Point({self.x}, {self.y})"


# ---------------------------------------------------------------- 4
def running_total(nums: list):
    """Yield the cumulative sum after each number.
    running_total([1, 2, 3]) yields 1, then 3, then 6.
    running_total([]) yields nothing.
    This must be a generator: use yield, and do not build a list to return."""
    total = 0
    for n in nums:
        total += n
        yield total 
    # hint: total = 0. for each n, add n to total, then yield total


# ---------------------------------------------------------------- 5
class MissingItem(Exception):
    """Raised by Basket.take when the name is not in the basket.
    This class is complete. Raise it from Basket."""
    pass


class Basket:
    """Stores item names and quantities.
    add(name, qty) requires qty > 0, otherwise ValueError. Adding the same name sums.
    count(name) is 0 when the name is absent.
    take(name, qty) requires qty > 0, otherwise ValueError.
    take raises MissingItem when the name is absent.
    take raises ValueError when qty is larger than the stored amount, and the count stays unchanged.
    When a take brings the count to 0, the name is gone. The next take raises MissingItem."""

    def __init__(self):
        self._items = {}
        # hint: self._items = {}

    def add(self, name: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("enter positive value of qty")
        else:
            self._items[name] = self._items.get(name, 0) + qty
        # hint: qty <= 0 raises ValueError. otherwise add qty to the current count

    def count(self, name: str) -> int:
        return self._items.get(name, 0)
        # hint: dict.get(name, 0)

    def take(self, name: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("enter positive value of qty")
        if name not in self._items:
            raise MissingItem(name)
        if qty > self._items[name]:
            raise ValueError("not enough")
        self._items[name] -= qty
        if self._items[name] == 0:
            del self._items[name]
        # hint: qty <= 0 raises ValueError. missing name raises MissingItem.
        # hint: qty larger than the count raises ValueError before you change the dict.
        # hint: subtract, and delete the name when the count reaches 0


# ---------------------------------------------------------------- 6
class History:
    """Starts with text (default '').
    text can be read and cannot be assigned.
    write(s) appends s and remembers the previous text.
    undo() restores the previous text.
    undo raises ValueError when there is nothing to undo.
    The starting text is not an undo step."""

    def __init__(self, text: str = ""):
        self._text = text
        self._undo = []
        # hint: self._text = text, and self._undo = []

    @property
    def text(self) -> str:
        return self._text
        # hint: return self._text

    def write(self, s: str) -> None:
        self._undo.append(self.text)
        self._text += s
        # hint: append the current text to self._undo, then add s onto self._text

    def undo(self) -> None:
        if len(self._undo) == 0:
            raise ValueError("empty")
        else:
            self._text = self._undo.pop()

        # hint: an empty self._undo raises ValueError. otherwise pop and store it as self._text


# ---------------------------------------------------------------- 7
class Countdown:
    """Iterating counts down from start through 1.
    list(Countdown(3)) is [3, 2, 1]. list(Countdown(0)) is [].
    A countdown is empty the second time you iterate the same object."""

    def __init__(self, start: int):
        self._start = start
        # hint: remember the next number to hand out. that number starts at start

    def __iter__(self):
        return self
        # hint: return self

    def __next__(self) -> int:
        if self._start < 1:
            raise StopIteration("next element is below 1")
        
        current = self._start
        self._start -= 1
        return current
        # hint: when the next number is below 1, raise StopIteration.
        # hint: otherwise return it and move the remembered number down by 1


# ---------------------------------------------------------------- 8
class Step(ABC):
    """One change applied to a string. Subclasses implement apply."""

    @abstractmethod
    def apply(self, text: str) -> str:
        pass
        # hint: class Step(ABC), and this method stays abstract


class Trim(Step):
    """Removes whitespace from both ends."""

    def apply(self, text: str) -> str:
        return text.strip()
        # hint: text.strip()


class Upper(Step):
    """Returns the uppercased string."""

    def apply(self, text: str) -> str:
        return text.upper()
        # hint: text.upper()


class Wrap(Step):
    """Wraps the string in square brackets. 'hi' becomes '[hi]'."""

    def apply(self, text: str) -> str:
        return "[" + text + "]"
        # hint: return "[" + text + "]"


def run_pipeline(text: str, steps: list) -> str:
    """Apply each step in order. The next step sees the previous step's result.
    No steps leaves text unchanged.
    run_pipeline('  hi  ', [Trim(), Upper()]) is 'HI'.
    run_pipeline('  hi  ', [Trim(), Wrap()]) is '[hi]'.
    run_pipeline('  hi  ', [Wrap(), Trim()]) is '[  hi  ]'."""
    for step in steps:
        text = step.apply(text)
    return text
    # hint: for each step, text = step.apply(text). return text


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


def _run_counter():
    name = "Problem 1"
    counter = Counter()
    if not _check(f"{name}: start", counter.value, 0):
        return False
    counter.tick()
    counter.tick()
    if not _check(f"{name}: two ticks", counter.value, 2):
        return False
    counter.reset()
    if not _check(f"{name}: reset", counter.value, 0):
        return False
    started = Counter(5)
    started.tick()
    if not _check(f"{name}: start at 5", started.value, 6):
        return False
    if not _raises(f"{name}: assign value", lambda: setattr(counter, "value", 1), AttributeError):
        return False
    if not _check(f"{name}: value unchanged", counter.value, 0):
        return False
    print(f"PASS {name}: Counter")
    return True


def _run_bounded():
    name = "Problem 2"
    counter = BoundedCounter(2)
    if not _check(f"{name}: isinstance", isinstance(counter, Counter), True):
        return False
    counter.tick()
    counter.tick()
    if not _check(f"{name}: at limit", counter.value, 2):
        return False
    if not _raises(f"{name}: past limit", counter.tick, ValueError):
        return False
    if not _check(f"{name}: stays at limit", counter.value, 2):
        return False
    counter.reset()
    counter.tick()
    if not _check(f"{name}: after reset", counter.value, 1):
        return False
    full = BoundedCounter(1, 1)
    if not _raises(f"{name}: already full", full.tick, ValueError):
        return False
    if not _check(f"{name}: full unchanged", full.value, 1):
        return False
    print(f"PASS {name}: BoundedCounter")
    return True


def _run_point():
    name = "Problem 3"
    if not _check(f"{name}: equal", Point(1, 2) == Point(1, 2), True):
        return False
    if not _check(f"{name}: different", Point(1, 2) == Point(2, 1), False):
        return False
    if not _check(f"{name}: not a tuple", Point(1, 2) == (1, 2), False):
        return False
    if not _check(f"{name}: zero", Point(0, 0) == Point(0, 0), True):
        return False
    if not _check(f"{name}: repr", repr(Point(1, 2)), "Point(1, 2)"):
        return False
    print(f"PASS {name}: Point")
    return True


def _run_running_total():
    name = "Problem 4"
    gen = running_total([1, 2, 3])
    if not isinstance(gen, types.GeneratorType):
        print(f"FAIL {name}: running_total([1, 2, 3]) should be a generator")
        print(f"      got {type(gen).__name__}")
        return False
    if not _check(f"{name}: sums", list(gen), [1, 3, 6]):
        return False
    if not _check(f"{name}: empty", list(running_total([])), []):
        return False
    if not _check(f"{name}: one", list(running_total([5])), [5]):
        return False
    if not _check(f"{name}: negative", list(running_total([-1, 4])), [-1, 3]):
        return False
    print(f"PASS {name}: running_total")
    return True


def _run_basket():
    name = "Problem 5"
    basket = Basket()
    if not _check(f"{name}: missing count", basket.count("apple"), 0):
        return False
    basket.add("apple", 2)
    basket.add("apple", 1)
    if not _check(f"{name}: summed", basket.count("apple"), 3):
        return False
    basket.take("apple", 1)
    if not _check(f"{name}: after take", basket.count("apple"), 2):
        return False
    if not _raises(f"{name}: missing take", lambda: basket.take("pear", 1), MissingItem):
        return False
    if not _raises(f"{name}: too many", lambda: basket.take("apple", 5), ValueError):
        return False
    if not _check(f"{name}: unchanged after too many", basket.count("apple"), 2):
        return False
    if not _raises(f"{name}: add 0", lambda: basket.add("apple", 0), ValueError):
        return False
    if not _raises(f"{name}: take 0", lambda: basket.take("apple", 0), ValueError):
        return False
    basket.take("apple", 2)
    if not _check(f"{name}: gone", basket.count("apple"), 0):
        return False
    if not _raises(f"{name}: take after gone", lambda: basket.take("apple", 1), MissingItem):
        return False
    print(f"PASS {name}: Basket")
    return True


def _run_history():
    name = "Problem 6"
    history = History()
    if not _check(f"{name}: start", history.text, ""):
        return False
    if not _raises(f"{name}: undo empty", history.undo, ValueError):
        return False
    history.write("ab")
    history.write("c")
    if not _check(f"{name}: written", history.text, "abc"):
        return False
    history.undo()
    if not _check(f"{name}: undo once", history.text, "ab"):
        return False
    history.undo()
    if not _check(f"{name}: undo twice", history.text, ""):
        return False
    if not _raises(f"{name}: undo past start", history.undo, ValueError):
        return False
    started = History("hi")
    if not _check(f"{name}: given start", started.text, "hi"):
        return False
    if not _raises(f"{name}: start is not a step", started.undo, ValueError):
        return False
    started.write("!")
    started.undo()
    if not _check(f"{name}: undo to start", started.text, "hi"):
        return False
    again = History()
    again.write("a")
    again.write("b")
    again.undo()
    again.write("c")
    if not _check(f"{name}: write after undo", again.text, "ac"):
        return False
    again.undo()
    if not _check(f"{name}: undo that write", again.text, "a"):
        return False
    if not _raises(f"{name}: assign text", lambda: setattr(again, "text", "nope"), AttributeError):
        return False
    if not _check(f"{name}: text unchanged", again.text, "a"):
        return False
    print(f"PASS {name}: History")
    return True


def _run_countdown():
    name = "Problem 7"
    if not _check(f"{name}: three", list(Countdown(3)), [3, 2, 1]):
        return False
    if not _check(f"{name}: one", list(Countdown(1)), [1]):
        return False
    if not _check(f"{name}: zero", list(Countdown(0)), []):
        return False
    countdown = Countdown(2)
    if not _check(f"{name}: first pass", list(countdown), [2, 1]):
        return False
    if not _check(f"{name}: second pass", list(countdown), []):
        return False
    if not _raises(f"{name}: empty next", lambda: next(Countdown(0)), StopIteration):
        return False
    print(f"PASS {name}: Countdown")
    return True


def _run_pipeline():
    name = "Problem 8"
    if not _raises(f"{name}: Step()", lambda: Step(), TypeError):
        return False
    if not _check(f"{name}: Trim is a Step", isinstance(Trim(), Step), True):
        return False
    if not _check(f"{name}: Upper is a Step", isinstance(Upper(), Step), True):
        return False
    if not _check(f"{name}: Wrap is a Step", isinstance(Wrap(), Step), True):
        return False
    if not _check(f"{name}: no steps", run_pipeline("  hi  ", []), "  hi  "):
        return False
    if not _check(f"{name}: trim upper", run_pipeline("  hi  ", [Trim(), Upper()]), "HI"):
        return False
    if not _check(f"{name}: trim wrap", run_pipeline("  hi  ", [Trim(), Wrap()]), "[hi]"):
        return False
    if not _check(f"{name}: wrap trim", run_pipeline("  hi  ", [Wrap(), Trim()]), "[  hi  ]"):
        return False
    print(f"PASS {name}: pipeline")
    return True


CUSTOM = {
    1: _run_counter,
    2: _run_bounded,
    3: _run_point,
    4: _run_running_total,
    5: _run_basket,
    6: _run_history,
    7: _run_countdown,
    8: _run_pipeline,
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
