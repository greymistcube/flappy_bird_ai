import random
import pygame

from lib.settings import Settings
from lib.environment import Environment
# from lib.objects import Ball, Wall, Buildings

# display
WIDTH, HEIGHT = (320, 240)
RESOLUTION = (WIDTH, HEIGHT)
ZOOM_LEVEL = 3

# game objects
START_POSITION = (80, 80)
WALL_DISTANCE = 240
HOLE_SIZE = 80
HOLE_Y_VARIANCE = 40

# mechenics
JUMP_VELOCITY = -4
GRAVITY = 0.2
MOVE_SPEED = -2

# other settings
TICKRATE = 60
SCROLL_SPEED = -1

# predefined color tuples
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (127, 191, 255)

# variable settings
num_balls = 1
tickrate = TICKRATE

# perhaps no class?

class Events:
    def __init__(self):
        self.multiplier = 1
        self.jumps = [[False]]
        return

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        self.jumps = [[pressed_keys[pygame.K_SPACE]]]
        self.multiplier = None
        for i, pressed in enumerate(pressed_keys[pygame.K_0:pygame.K_0 + 10]):
            if pressed:
                self.multiplier = i
                break
        return
"""
    def quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def key_events(self):
        pressed_keys = pygame.key.get_pressed()
        self.jumps = [[pressed_keys[pygame.K_SPACE]]]
        self.multiplier = None
        for i, pressed in enumerate(pressed_keys[pygame.K_0:pygame.K_0 + 10]):
            if pressed:
                self.multiplier = i
                break
        return
"""
class Core:
    def __init__(self):
        self.settings = Settings()
        self.events = Events()
        return

    def new_game(self):
        self.env = Environment()

    def update(self):
        self.events.update()
        self.settings.update(self.events)
        self.env.update(self.events)

    def game_over(self):
        return self.env.game_over()

    def draw(self):
        return self.env.get_surface()
