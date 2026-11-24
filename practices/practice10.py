#Vault

#Shortest path. path_to(x, y) rerutns the steps to that tile.
#This is BFS.
'''
A deque holds the positions still to try, a set holds the ones already
tried, and walls are never entered. The first time you reach the goal
is the shortest path, because every position is expanded one step at a
time.
'''

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

class Play:

    def __init__(self):
        self.Room()
    

room = Room([".#.", "..."], 0, 0)
room.move("right")
print(room.coordinates()) # (0, 0), the title to the right is a wall
room.move("down")
print(room.coordinates()) # (0, 1)
print(room.look())
print(room._rows)

room = Room([".k.", "...", "..D"], 0, 0)
room.move("right")
print(room.inventory())      # ['key']
print(room.look())           # [['.', '@', '.'], ['.', '.', '.'], ['.', '.', 'D']]