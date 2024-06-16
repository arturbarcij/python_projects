import pygame

class Interface:
    def __init__(self, width, height):
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game')

    def update_display(self):
        pygame.display.update()
