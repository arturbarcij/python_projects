#Vault

#Shortest path. path_to(x, y) rerutns the steps to that tile.
#This is BFS.
'''
A deque holds the positions still to try, a set holds the ones already
tried, and walls are never entered. The first time you reach the goal
is the shortest path, because every position is expanded one step at a
time.
'''

from collections import deque


class Room:

    def __init__(self, rows, x, y):
        self._rows = [list(row) for row in rows]
        self._inventory = set()
        self._history = []
        self._x = x
        self._y = y

    def move(self, direction):
        steps = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        dx, dy = steps[direction]
        new_x = self._x + dx
        new_y = self._y + dy
        if new_y < 0 or new_y >= len(self._rows):
            return
        if new_x < 0 or new_x >= len(self._rows[new_y]):
            return
        tile = self._rows[new_y][new_x]
        if tile == "#":
            return
        if tile == "D" and "key" not in self._inventory:
            return
        self._history.append((self._x, self._y, set(self._inventory), new_x, new_y, tile))
        if tile == "k":
            self._inventory.add("key")
            self._rows[new_y][new_x] = "."
        self._x = new_x
        self._y = new_y

    def inventory(self):
        return sorted(self._inventory)
    
    def coordinates(self):
        return (self._x, self._y)
    
    def look(self):
        view = [row[:] for row in self._rows]
        view[self._y][self._x] = "@"
        return view
    
    def undo(self):
        if len(self._history) == 0:
            raise ValueError("nothing to undo")
        x, y, inventory, tile_x, tile_y, tile = self._history.pop()
        self._x = x
        self._y = y
        self._inventory = inventory
        self._rows[tile_y][tile_x] = tile

    def path_to(self, x, y):
        #BFS
        start = (self._x, self._y)
        goal = (x, y)
        frontier = deque([start])
        visited = {start}
        came_from = {}
        steps = ((0, -1), (0, 1), (-1, 0), (1, 0))
        while frontier:
            cx, cy = frontier.popleft()
            for dx, dy in steps:
                nx = cx + dx
                ny = cy + dy
                if ny < 0 or ny >= len(self._rows):
                    continue
                if nx < 0 or nx >= len(self._rows[ny]):
                    continue
                if self._rows[ny][nx] == "#":
                    continue
                if self._rows[ny][nx] == "D" and "key" not in self._inventory:
                    continue
                nxt = (nx, ny)
                if nxt in visited:
                    continue
                visited.add(nxt)
                came_from[nxt] = (cx, cy)
                if nxt == goal:
                    path = [nxt]
                    while path[-1] != start:
                        path.append(came_from[path[-1]])
                    path.reverse()
                    return path
                frontier.append(nxt)
        return []
        
    def guard(self, x, y):
        player_x, player_y = self._x, self._y
        self._x, self._y = x, y
        path = self.path_to(player_x, player_y)
        self._x, self._y = player_x, player_y
        if len(path) < 2:
            return (x, y)
        return path[1]

        

class Play:

    def __init__(self, room, guard_x, guard_y):
        self._room = room
        self._guard = (guard_x, guard_y)

    def step(self, key):
        key = key.strip().lower()
        if key == "q":
            return "quit"
        moves = {"w": "up", "a": "left", "s": "down", "d": "right"}
        if key not in moves:
            return "play"
        self._room.move(moves[key])
        x, y = self._room.coordinates()
        if self._room._rows[y][x] == "D":
            return "won"
        self._guard = self._room.guard(self._guard[0], self._guard[1])
        if self._guard == self._room.coordinates():
            return "lost"
        return "play"

    def show(self):
        view = self._room.look()
        gx, gy = self._guard
        if (gx, gy) != self._room.coordinates():
            view[gy][gx] = "G"
        for row in view:
            print("".join(row))

    def run(self):
        while True:
            self.show()
            outcome = self.step(input())
            if outcome == "quit":
                return
            if outcome == "won":
                print("won")
                return
            if outcome == "lost":
                print("lost")
                return


import sys
import unittest


class MoveTest(unittest.TestCase):
    def test_wall_blocks(self):
        room = Room([".#."], 0, 0)
        room.move("right")
        self.assertEqual(room.coordinates(), (0, 0))

    def test_step_down(self):
        room = Room([".#.", "..."], 0, 0)
        room.move("down")
        self.assertEqual(room.coordinates(), (0, 1))

    def test_look_shows_the_player_and_keeps_the_grid(self):
        room = Room([".#.", "..."], 0, 0)
        room.move("down")
        self.assertEqual(room.look(), [[".", "#", "."], ["@", ".", "."]])
        self.assertEqual(room._rows, [[".", "#", "."], [".", ".", "."]])


class KeyTest(unittest.TestCase):
    def test_key_is_picked_up(self):
        room = Room([".k."], 0, 0)
        room.move("right")
        self.assertEqual(room.inventory(), ["key"])
        self.assertEqual(room._rows, [[".", ".", "."]])

    def test_door_blocks_without_the_key(self):
        room = Room([".D"], 0, 0)
        room.move("right")
        self.assertEqual(room.coordinates(), (0, 0))

    def test_door_opens_with_the_key(self):
        room = Room([".kD"], 0, 0)
        room.move("right")
        room.move("right")
        self.assertEqual(room.coordinates(), (2, 0))

    def test_undo_puts_the_key_back(self):
        room = Room([".k."], 0, 0)
        room.move("right")
        room.undo()
        self.assertEqual(room.coordinates(), (0, 0))
        self.assertEqual(room.inventory(), [])
        self.assertEqual(room._rows, [[".", "k", "."]])

    def test_undo_with_no_history_raises(self):
        with self.assertRaises(ValueError):
            Room(["."], 0, 0).undo()


class PathTest(unittest.TestCase):
    def test_path_goes_around_the_wall(self):
        room = Room([".#.", "..."], 0, 0)
        self.assertEqual(room.path_to(2, 1), [(0, 0), (0, 1), (1, 1), (2, 1)])

    def test_wall_is_not_a_goal(self):
        room = Room([".#.", "..."], 0, 0)
        self.assertEqual(room.path_to(1, 0), [])


class GuardTest(unittest.TestCase):
    def test_guard_takes_one_step(self):
        room = Room([".#.", "..."], 0, 0)
        room.move("down")
        self.assertEqual(room.guard(2, 1), (1, 1))

    def test_next_step_lands_on_the_player(self):
        room = Room([".#.", "..."], 0, 0)
        room.move("down")
        self.assertEqual(room.guard(1, 1), (0, 1))
        self.assertEqual(room.coordinates(), (0, 1))


class PlayTest(unittest.TestCase):
    def test_quit_leaves_the_player_in_place(self):
        room = Room(["..."], 0, 0)
        play = Play(room, 2, 0)
        self.assertEqual(play.step("q"), "quit")
        self.assertEqual(room.coordinates(), (0, 0))

    def test_guard_catches_the_player(self):
        room = Room([".#.", "..."], 0, 0)
        play = Play(room, 2, 1)
        self.assertEqual(play.step("s"), "play")
        self.assertEqual(play.step("a"), "lost")

    def test_door_wins_before_the_guard_moves(self):
        room = Room([".kD", "...", "..."], 0, 0)
        play = Play(room, 2, 2)
        self.assertEqual(play.step("d"), "play")
        self.assertEqual(play.step("d"), "won")


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
    if len(sys.argv) > 1 and sys.argv[1] == "play":
        room = Room([".k.", "...", "..D"], 0, 0)
        Play(room, 2, 2).run()
    else:
        suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
        result = Runner(resultclass=Report, verbosity=0).run(suite)
        passed = result.testsRun - len(result.failures) - len(result.errors)
        print(f"\n{passed}/{result.testsRun} passed")