import pygame
from constants import *

def load_image(file):
    image = pygame.image.load(file)
    return image

class Ball:
    image = load_image("./img/blue_ball.png")
    image_jumping = load_image("./img/blue_ball_jumping.png")
    image_falling = load_image("./img/blue_ball_falling.png")

    def __init__(self):
        self.rect = self.image.get_rect()
        self.x, self.y = START_POSITION
        self.rect.center = (self.x, self.y)
        self.velocity = 0.0
        self.score = 0
        self.alive = True
        return

    def move(self):
        # huge pain caused by using move instead of center
        self.y = self.y + self.velocity
        self.rect.center = (self.x, self.y)
        return

    def accelerate(self):
        self.velocity = self.velocity + GRAVITY
        return

    def jump(self):
        self.velocity = JUMP_VELOCITY

    def get_image(self):
        if self.velocity < 0:
            return self.image_jumping
        else:
            return self.image_falling

class Wall:
    image = load_image("./img/brick_wall.png")

    # here, (x, y) correspond to the center of a wall
    def __init__(self, x, y):
        self.lower = self.image.get_rect()
        self.upper = self.image.get_rect()
        y_offset = (HOLE_SIZE + self.image.get_height()) // 2
        self.lower.center = (x, y + y_offset)
        self.upper.center = (x, y - y_offset)
        self.x = x
        self.y = y
        self.speed = MOVE_SPEED
        return

    def move(self):
        self.lower = self.lower.move((self.speed, 0))
        self.upper = self.upper.move((self.speed, 0))
        self.x = self.x + self.speed
        return
