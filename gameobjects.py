import pygame
import random
from constants import *

def load_image(file):
    image = pygame.image.load(file)
    return image

class Ball:
    images = {
        "blue_jumping": load_image("./img/blue_ball_jumping.png"),
        "blue_falling": load_image("./img/blue_ball_falling.png"),
        "green_jumping": load_image("./img/green_ball_jumping.png"),
        "green_falling": load_image("./img/green_ball_falling.png"),
        "yellow_jumping": load_image("./img/yellow_ball_jumping.png"),
        "yellow_falling": load_image("./img/yellow_ball_falling.png"),
        "red_jumping": load_image("./img/red_ball_jumping.png"),
        "red_falling": load_image("./img/red_ball_falling.png"),
    }
    image = load_image("./img/blue_ball.png")
    # image_jumping = load_image("./img/blue_ball_jumping.png")
    # image_falling = load_image("./img/blue_ball_falling.png")

    def __init__(self, color="blue"):
        self.rect = self.image.get_rect()
        self.color = color
        self.x, self.y = START_POSITION
        self.y = random.randint(40, 200)
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

    def get_image_key(self):
        if self.velocity < 0:
            state = "jumping"
        else:
            state = "falling"
        key = "{}_{}".format(self.color, state)
        return key

    def get_image(self):
        return self.images[self.get_image_key()]

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
