import pygame
import random
from game.interface import Interface
from logic.collision import check_collision_with_walls, check_collision_with_self

class GameLogic:
    def __init__(self):
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        self.display_width = 800
        self.display_height = 600
        self.snake_block = 10
        self.snake_speed = 15
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        self.interface = Interface(self.display_width, self.display_height)

    def your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.black)
        self.interface.display.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.interface.display, self.black, [x[0], x[1], snake_block, snake_block])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.interface.display.blit(mesg, [self.display_width / 6, self.display_height / 3])

    def gameLoop(self):
        game_over = False
        game_close = False

        x1 = self.display_width / 2
        y1 = self.display_height / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, self.display_width - self.snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, self.display_height - self.snake_block) / 10.0) * 10.0

        while not game_over:

            while game_close:
                self.interface.display.fill(self.blue)
                self.message("You Lost! Press Q-Quit or C-Play Again", self.red)
                self.your_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = self.snake_block
                        x1_change = 0

            if check_collision_with_walls(x1, y1, self.display_width, self.display_height):
                game_close = True

            x1 += x1_change
            y1 += y1_change
            self.interface.display.fill(self.white)
            pygame.draw.rect(self.interface.display, self.green, [foodx, foody, self.snake_block, self.snake_block])
            snake_Head = [x1, y1]
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            if check_collision_with_self(snake_List):
                game_close = True

            self.our_snake(self.snake_block, snake_List)
            self.your_score(Length_of_snake - 1)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.display_width - self.snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, self.display_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 1

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()
