import random
import pygame

from lib.constants import *

def load_image(file):
    image = pygame.image.load(file)
    return image

class Ball:
    # default image for size reference
    _image = load_image("./rsc/img/blue_ball_falling.png")
    # lazy implementation of colored balls
    _images = {
        "blue_jumping": load_image("./rsc/img/blue_ball_jumping.png"),
        "blue_falling": load_image("./rsc/img/blue_ball_falling.png"),
        "green_jumping": load_image("./rsc/img/green_ball_jumping.png"),
        "green_falling": load_image("./rsc/img/green_ball_falling.png"),
        "yellow_jumping": load_image("./rsc/img/yellow_ball_jumping.png"),
        "yellow_falling": load_image("./rsc/img/yellow_ball_falling.png"),
        "red_jumping": load_image("./rsc/img/red_ball_jumping.png"),
        "red_falling": load_image("./rsc/img/red_ball_falling.png"),
    }

    def __init__(self, color="blue"):
        self.rect = self._image.get_rect()
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

    def get_surface(self):
        if self.velocity < 0:
            state = "jumping"
        else:
            state = "falling"
        key = "{}_{}".format(self.color, state)

        return self._images[key]

class Wall:
    # class initialization
    _image = load_image("./rsc/img/brick_wall.png")

    _width, _height = _image.get_size()
    _y_offset = (HOLE_SIZE + _height) // 2

    _surface = pygame.Surface((_width, _height * 2 + HOLE_SIZE), pygame.SRCALPHA)
    _surface.blit(_image, (0, 0))
    _surface.blit(_image, (0, _height + HOLE_SIZE))

    _speed = MOVE_SPEED

    # here, (x, y) correspond to the center of the hole in a wall
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = self._surface.get_rect()
        self.hole_rect = pygame.Rect(0, 0, self._surface.get_width(), HOLE_SIZE)
        self.rect.center = self.hole_rect.center = (self.x, self.y)
        return

    def move(self):
        self.x = self.x + self._speed
        self.rect.center = self.hole_rect.center = (self.x, self.y)
        return

    def get_surface(self):
        return self._surface

class Buildings:
    _image = load_image("./rsc/img/buildings.png")

    def __init__(self):
        self.rect = self._image.get_rect()
        return
    
    def get_surface(self):
        return self._image
