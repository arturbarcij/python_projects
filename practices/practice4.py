"""
Python practice sheet 4.

Part 1 (problems 1-4): two pointers again, then intervals, a small dynamic
programming loop, and reversing a linked list.
Part 2 (problems 5-8): a binary search tree, a stack that tracks its minimum,
a graph search that uses a queue, and a subclass of the tree.

How to use:
  1. Replace each `pass` with your solution.
  2. Run:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice4.py
     One problem:  python c:\\Users\\artur\\IdeaProjects\\Python\\python_projects\\practices\\practice4.py 1

Each problem prints PASS or FAIL with the input that broke it.
Rule: no peeking at the hints until you have tried for 2 minutes.
"""
from socket import setdefaulttimeout
import sys
from tkinter import N


# ---------------------------------------------------------------- 1
def dedupe_sorted(nums: list) -> list:
    """nums is sorted ascending. Return a new list with consecutive duplicates removed.
    [1, 1, 2, 2, 3] -> [1, 2, 3]. [] -> []."""
    result = []
    for n in nums:
        if not result or n != result[-1]:
            result.append(n)
    return result
    # hint: keep a result list. Append nums[i] only when it differs from the last appended value


# ---------------------------------------------------------------- 2
def merge_intervals(intervals: list) -> list:
    """Each interval is [start, end]. Merge the ones that overlap or touch.
    [[1, 3], [2, 6], [8, 10]] -> [[1, 6], [8, 10]]. Input may be unsorted."""
    if not intervals:
        return []
    intervals = sorted(intervals)
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
    # hint: sort by start. If this start <= the previous end, extend that end. Otherwise append a new pair


# ---------------------------------------------------------------- 3
def climb_stairs(n: int) -> int:
    """Ways to climb n stairs, taking 1 or 2 stairs at a time.
    0 -> 1, 1 -> 1, 2 -> 2, 3 -> 3, 4 -> 5."""
    if n == 0:
        return 1
    ways = [0] * (n + 1)
    ways[1] = 1
    if n == 1:
        return ways[1]
    ways[2] = 2
    for i in range(3, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    return ways[n]
    # hint: ways[i] = ways[i - 1] + ways[i - 2]. Fill a list from 1 up to n


# ---------------------------------------------------------------- 4
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def reverse_list(head):
    """Reverse the linked list and return the new head. None stays None."""
    prev = None
    current = head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev

    # hint: prev = None, current = head. Point current.next at prev, then step both forward


# ---------------------------------------------------------------- 5
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    """Binary search tree. Smaller values go left, larger values go right.
    inorder returns values from smallest to largest.
    height is the number of nodes on the longest root-to-leaf path. An empty tree has height 0."""

    def __init__(self):
        self.root = None
        # hint: self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            return
        node = self.root
        while True:
            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(value)
                    return
                node = node.right
        # hint: walk left when value < node.value, right otherwise, and attach a TreeNode at the empty child

    def contains(self, value) -> bool:
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def inorder(self) -> list:
        values = []
        # hint: visit left, then append the node value, then visit right
        def visit(node):
            if node is None:
                return
            visit(node.left)
            values.append(node.value)
            visit(node.right)
        
        visit(self.root)
        return values

    def height(self) -> int:
        def measure(node):
            if node is None:
                return 0
            return 1 + max(measure(node.left), measure(node.right))
        
        return measure(self.root)
        # hint: an empty node is 0. A node is 1 + the taller child


# ---------------------------------------------------------------- 6
class MinStack:
    """A stack whose minimum can be read without scanning every item.
    push and pop behave like a normal stack. minimum returns the smallest value still stored."""

    def __init__(self):
        self._items = []
        self._mins = []
        # hint: two lists, items and mins. The top of mins is the minimum of the whole stack

    def push(self, value):
        self._items.append(value)
        if not self._mins or value < self._mins[-1]:
            self._mins.append(value)
        else:
            self._mins.append(self._mins[-1])

    def pop(self):
        self._mins.pop()
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def minimum(self):
        return self._mins[-1]


# ---------------------------------------------------------------- 7
class Graph:
    """Undirected graph. add_edge(a, b) connects a and b in both directions.
    Neighbors stay in the order they were added.
    bfs(start) returns nodes in visit order. A missing start returns []."""

    def __init__(self):
        self._neighbours = {}
        # hint: self._neighbors = {}

    def add_edge(self, a, b):
        self._neighbours.setdefault(a, []).append(b)
        self._neighbours.setdefault(b, []).append(a)
        # hint: append b to as's list and a to b's list. setdefault(node, []) creates the list

    def bfs(self, start) -> list:
        if start not in self._neighbours:
            return []
        seen = {start}
        queue = [start]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbour in self._neighbours[node]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return order
        # hint: a queue and a seen set. Pop the front, then enqueue unseen neighbors in stored order


# ---------------------------------------------------------------- 8
class AuditedBST(BST):
    """A BST that remembers every value passed to insert, in call order.
    inserted starts as []. contains and inorder stay inherited."""

    def __init__(self):
        super().__init__()
        self.inserted = []
        # hint: super().__init__(), then self.inserted = []

    def insert(self, value):
        super().insert(value)
        self.inserted.append(value)
        # hint: super().insert(value), then append value to self.inserted


# ================================================================ tests
def _check(name, got, expected):
    if got != expected:
        print(f"FAIL {name}\n      expected {expected!r}\n      got      {got!r}")
        return False
    return True


def _chain(values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def _walk(head):
    values = []
    while head is not None:
        values.append(head.value)
        head = head.next
    return values


def _run_reverse():
    name = "Problem 4"
    if not _check(f"{name}: empty", _walk(reverse_list(None)), []):
        return False
    if not _check(f"{name}: one node", _walk(reverse_list(_chain([1]))), [1]):
        return False
    if not _check(f"{name}: 1, 2, 3", _walk(reverse_list(_chain([1, 2, 3]))), [3, 2, 1]):
        return False
    print(f"PASS {name}: reverse_list")
    return True


def _run_bst():
    name = "Problem 5"
    tree = BST()
    if not _check(f"{name}: empty inorder", tree.inorder(), []):
        return False
    if not _check(f"{name}: empty height", tree.height(), 0):
        return False
    if not _check(f"{name}: empty contains", tree.contains(1), False):
        return False
    for value in (5, 1, 7, 3):
        tree.insert(value)
    if not _check(f"{name}: inorder", tree.inorder(), [1, 3, 5, 7]):
        return False
    if not _check(f"{name}: contains 3", tree.contains(3), True):
        return False
    if not _check(f"{name}: contains 4", tree.contains(4), False):
        return False
    if not _check(f"{name}: height", tree.height(), 3):
        return False
    print(f"PASS {name}: BST")
    return True


def _run_min_stack():
    name = "Problem 6"
    stack = MinStack()
    stack.push(3)
    stack.push(5)
    if not _check(f"{name}: minimum after 3, 5", stack.minimum(), 3):
        return False
    if not _check(f"{name}: peek", stack.peek(), 5):
        return False
    stack.push(1)
    if not _check(f"{name}: minimum after push 1", stack.minimum(), 1):
        return False
    if not _check(f"{name}: pop", stack.pop(), 1):
        return False
    if not _check(f"{name}: minimum after pop", stack.minimum(), 3):
        return False
    if not _check(f"{name}: pop", stack.pop(), 5):
        return False
    if not _check(f"{name}: minimum left", stack.minimum(), 3):
        return False
    print(f"PASS {name}: MinStack")
    return True


def _run_graph():
    name = "Problem 7"
    graph = Graph()
    if not _check(f"{name}: missing start", graph.bfs(1), []):
        return False
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    if not _check(f"{name}: bfs(1)", graph.bfs(1), [1, 2, 3, 4]):
        return False
    if not _check(f"{name}: bfs(4)", graph.bfs(4), [4, 2, 1, 3]):
        return False
    print(f"PASS {name}: Graph")
    return True


def _run_audited():
    name = "Problem 8"
    tree = AuditedBST()
    if not _check(f"{name}: inserted starts empty", tree.inserted, []):
        return False
    tree.insert(2)
    tree.insert(1)
    if not _check(f"{name}: inserted", tree.inserted, [2, 1]):
        return False
    if not _check(f"{name}: inorder", tree.inorder(), [1, 2]):
        return False
    if not _check(f"{name}: contains 1", tree.contains(1), True):
        return False
    print(f"PASS {name}: AuditedBST")
    return True


TESTS = {
    1: (dedupe_sorted, [
        (([1, 1, 2, 2, 3],), [1, 2, 3]),
        (([],), []),
        (([1, 1, 1],), [1]),
        (([1, 2, 3],), [1, 2, 3]),
    ]),
    2: (merge_intervals, [
        (([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]),
        (([[1, 4], [4, 5]],), [[1, 5]]),
        (([[1, 4], [0, 4]],), [[0, 4]]),
        (([[1, 4]],), [[1, 4]]),
        (([],), []),
    ]),
    3: (climb_stairs, [
        ((0,), 1),
        ((1,), 1),
        ((2,), 2),
        ((3,), 3),
        ((4,), 5),
        ((5,), 8),
    ]),
}

CUSTOM = {
    4: _run_reverse,
    5: _run_bst,
    6: _run_min_stack,
    7: _run_graph,
    8: _run_audited,
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
