import pygame
'''
Class Interface represents front-end/screen as interface of snake game and
is made of two classes: __init__() and update_dsiplay().
'''
class Interface:
    #initialize size of display with width and height
    def __init__(self, width, height):
        self.display = pygame.display.set_mode(width, height)
        pygame.display.set_caption("Snake game")

    #update display
    def update_display(self):
        pygame.display.update()

