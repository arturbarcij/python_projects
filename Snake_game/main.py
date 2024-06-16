import pygame
from logic.game_logic import GameLogic

def main():
    pygame.init()  # Initialize pygame
    game = GameLogic()
    game.gameLoop()
    pygame.quit()  # Quit pygame

if __name__ == "__main__":
    main()
