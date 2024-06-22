import pygame

class Display:
    def __init__(self, width, height):
        self.display = pygame.display.set_mode(width, height)
        pygame.display.set_caption("Tic Tac Toe")
    
    def update_display(self):
        pygame.display.update()