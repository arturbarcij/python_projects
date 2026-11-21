"""
Python practice sheet.

How to use:
  1. Save this file anywhere, open it in your editor (VS Code, Notepad, whatever).
  2. Replace each `pass` with your solution.
  3. Run:  python practice.py
     Run one problem only:  python practice.py 3

Each problem prints PASS or FAIL with the input that broke it.
Rule: no peeking at the hints until you have tried for 2 minutes.
"""
import sys


# ---------------------------------------------------------------- 1
def is_even(n: int) -> bool:
    """Return True if n is even. Works for negatives too."""
    return n % 2 == 0
    # hint: n % 2


# ---------------------------------------------------------------- 2
def reverse_string(s: str) -> str:
    """Return s reversed."""
    return s[::-1]
    # start:stop:step return s[start:stop:-1]
    # hint: slicing with a step of -1


# ---------------------------------------------------------------- 3
def ceil_div(a: int, b: int) -> int:
    """Divide a by b and round UP. b > 0. Do not use the math module."""
    q, r = divmod(a, b)
    return q + (r != 0)
    # hint: // floors, so negate, floor, negate


# ---------------------------------------------------------------- 4
def sum_digits(n: int) -> int:
    """Sum of the digits of a non-negative integer. 493 -> 16."""
    return sum(int(ch) for ch in str(n))
    # hint: n % 10 is the last digit, n // 10 drops it


# ---------------------------------------------------------------- 5
def add_item(item, items=None):
    """Append item to items and return the list.
    If items is not given, start a NEW list every call (watch the mutable default trap)."""
    if items is None:
        items = []
    items.append(item)
    return items
    


# ---------------------------------------------------------------- 6
def count_words(text: str) -> dict:
    """Count how often each word appears. Words are split on whitespace, lowercase them.
    'a b A' -> {'a': 2, 'b': 1}"""
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
    # hint: d.get(word, 0) + 1


# ---------------------------------------------------------------- 7
def two_sum(nums: list, target: int) -> list:
    """Return the indices [i, j] (i < j) of the two numbers that add up to target.
    Exactly one solution exists. Aim for O(n) time."""
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i

    # hint: dict of value -> index as you scan


# ---------------------------------------------------------------- 8
def group_anagrams(words: list) -> list:
    """Group words that are anagrams of each other. Group order does not matter."""
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
    # hint: sorted(word) is the same for anagrams


# ================================================================ tests
def _norm_groups(groups):
    return sorted(sorted(g) for g in groups)


TESTS = {
    1: (is_even, [((4,), True), ((7,), False), ((0,), True), ((-3,), False), ((-4,), True)]),
    2: (reverse_string, [(("abc",), "cba"), (("",), ""), (("a",), "a"), (("hello world",), "dlrow olleh")]),
    3: (ceil_div, [((7, 2), 4), ((8, 2), 4), ((1, 5), 1), ((0, 3), 0), ((-7, 2), -3)]),
    4: (sum_digits, [((493,), 16), ((0,), 0), ((10,), 1), ((99999,), 45)]),
    5: (None, None),  # custom test below
    6: (count_words, [(("a b A",), {"a": 2, "b": 1}), (("",), {}), (("x  x   x",), {"x": 3})]),
    7: (two_sum, [(([2, 7, 11, 15], 9), [0, 1]), (([3, 2, 4], 6), [1, 2]), (([3, 3], 6), [0, 1])]),
    8: (group_anagrams, [
        ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
        (([""],), [[""]]),
        ((["a"],), [["a"]]),
    ]),
}


def run(num):
    fn, cases = TESTS[num]
    name = f"Problem {num}"
    if num == 5:
        a = add_item(1)
        b = add_item(2)
        if a == [1] and b == [2]:
            print(f"PASS {name}: add_item")
        else:
            print(f"FAIL {name}: add_item(1) then add_item(2) gave {a} and {b}, expected [1] and [2]")
        return a == [1] and b == [2]
    for args, expected in cases:
        try:
            got = fn(*args)
        except Exception as e:
            print(f"FAIL {name}: {fn.__name__}{args} raised {type(e).__name__}: {e}")
            return False
        if num == 8:
            ok = got is not None and _norm_groups(got) == _norm_groups(expected)
        else:
            ok = got == expected
        if not ok:
            print(f"FAIL {name}: {fn.__name__}{args}\n      expected {expected!r}\n      got      {got!r}")
            return False
    print(f"PASS {name}: {fn.__name__}")
    return True


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or sorted(TESTS)
    results = [run(n) for n in which]
    print(f"\n{sum(results)}/{len(results)} passed")
