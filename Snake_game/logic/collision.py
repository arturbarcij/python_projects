'''
Collision class is logic of collision in snake game.
'''
def check_collision_with_walls(x, y, display_width, display_height):
    if x >= display_width or x < 0 or y >= display_height or y < 0:
        return True
    return False

def check_collision_with_self(snake_list):
    snake_head = snake_list[-1]
    if snake_head in snake_list[:-1]:
        return True
    return False
