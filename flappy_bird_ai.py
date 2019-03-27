import sys
import random
import pygame

import constants

def reset_game():
    global ball
    global wall
    global velocity
    velocity = 0
    ball = Ball()
    wall = Wall()

def load_image(file):
    image = pygame.image.load(file)
    image = pygame.transform.scale(image, [x * 2 for x in image.get_size()])
    return image

class Ball:
    image = load_image("blue_ball.png")

    def __init__(self):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(constants.START_POSITION)
        return

class Wall:
    image = load_image("brick_wall.png")

    def __init__(self):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move([480,240])
        return

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(constants.SIZE)
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
        velocity = velocity + constants.GRAVITY

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            velocity = constants.JUMP_VELOCITY

        # check if the pc is out of bounds
        if ball.rect.top < 0 or ball.rect.bottom > constants.HEIGHT:
            reset_game()
        
        # draw screen
        screen.fill(constants.WHITE)
        screen.blit(ball.image, ball.rect)
        screen.blit(wall.image, wall.rect)
        pygame.display.flip()

