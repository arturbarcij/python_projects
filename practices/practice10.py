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
    
    def undo(self, direction):
        if len(self._history) == 0:
            raise ValueError("nothing to undo")
        x, y, inventory, tile_x, tile_y = self._history.pop()
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
        

class Play:

    def __init__(self):
        key = input()
        if key == "w":
            room.move("up")
        elif key == "a":
            room.move("left")
        elif key == "s":
            room.move("down")
        elif key == "d":
            room.move("right")
        print(room.look())
    
room = Room([".#.", "..."], 0, 0)
print(room.path_to(2, 1))  # [(0, 0), (0, 1), (1, 1), (2, 1)]
print(room.path_to(1, 0))  # []
room.move("right")
print(room.coordinates()) # (0, 0), the title to the right is a wall
room.move("down")
print(room.coordinates()) # (0, 1)
print(room.look())
print(room._rows)

room = Room([".k.", "...", "..D"], 0, 0)
room.move("right")
print(room.inventory()) # ['key']
print(room.look()) # [['.', '@', '.'], ['.', '.', '.'], ['.', '.', 'D']]