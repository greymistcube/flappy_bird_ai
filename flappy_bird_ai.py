import sys
import random
import pygame

import constants as const

def add_wall(walls):
    walls.append(Wall(walls[-1].rect.left + const.WALL_DISTANCE, 240))
    return

def remove_wall(walls):
    walls.pop(0)
    return

def reset_game():
    global ball
    global walls
    global velocity
    velocity = 0
    ball = Ball()
    walls = [Wall(const.WIDTH, 240)]
    for i in range(5):
        add_wall(walls)

def load_image(file):
    image = pygame.image.load(file)
    image = pygame.transform.scale(image, [x * 2 for x in image.get_size()])
    return image

class Ball:
    image = load_image("blue_ball.png")

    def __init__(self):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(const.START_POSITION)
        return

class Wall:
    image = load_image("brick_wall.png")

    def __init__(self, x, y):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move([x, y])
        return

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(const.SIZE)
    clock = pygame.time.Clock()

    # initialize game before starting
    reset_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        # close game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        ball.rect = ball.rect.move((0, velocity))
        velocity = velocity + const.GRAVITY
        for wall in walls:
            wall.rect = wall.rect.move((-const.MOVE_SPEED, 0))
        
        if walls[0].rect.right < 0:
            remove_wall(walls)
            add_wall(walls)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            velocity = const.JUMP_VELOCITY

        # check if the pc is out of bounds
        if ball.rect.top < 0 or ball.rect.bottom > const.HEIGHT:
            reset_game()
        
        # draw screen
        screen.fill(const.WHITE)
        screen.blit(ball.image, ball.rect)
        for wall in walls:
            screen.blit(wall.image, wall.rect)
        pygame.display.flip()

