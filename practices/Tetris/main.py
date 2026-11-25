#Tetris Game from Scratch
# Plan to build a Tetris:
'''
1. Board: 10 Columns, 20 rows "." is empty. A locked block is "#".
rows returns a copy, the same idea as look.

2. One piece. Start with the T. It stores sa position and four offsets.
cells adds the position to each offset, so a T at (4, 0) occupies 
(4, 0), (3, 0), (5, 0) and (4, 1). y grows demand as it did in the Vault

3. Move
4. Rotate
5. Collision & lock
6. Line clear
7. The bag
8. Play
'''
# Imports
import pygame
import random
import sys

pygame.init()

#Constant variables
WIDTH, HEIGTH = 300, 500
FPS = 35

CELL = 20
ROWS = (HEIGTH - 120) // 120
COLS = WIDTH // HEIGTH

# Game settings ~ screen, clock, title
SCREEN = pygame.display.set_mode((WIDTH, HEIGTH))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (31, 25, 76)
GRID = (31, 25, 132)
WIN = (50, 230, 50)
LOSE = (252, 91, 122)

# Block images can be loaded here once Assets/1.png and the others exist.
ASSETS = {}

# Fonts
font = pygame.font.SysFont("verdana", 50)
font2 = pygame.font.SysFont("verdana", 15)

# Main Game Loop
def main():
    run = True
    while run:
        SCREEN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

class Tetris:

    class Board:
        pass
    class Piece:
        pass
    class Move:
        pass
    class Rotate:
        pass
    class Collision:
        pass
    class Line_clear:
        pass
    class Bag:
        pass
    class Play:
        pass
