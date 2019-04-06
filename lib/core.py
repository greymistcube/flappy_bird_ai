import sys
# import random
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

font = pygame.font.Font("./rsc/font/munro.ttf", 10)

def text_to_surface(text):
    return font.render(text, False, BLACK)

class Events:
    def __init__(self):
        self.multiplier = 1
        self.jumps = [[False]]
        return

    def update(self):
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # check for pressed keys and update variables accordingly
        pressed_keys = pygame.key.get_pressed()
        self.jumps = [[pressed_keys[pygame.K_SPACE]]]
        self.multiplier = None
        for i, pressed in enumerate(pressed_keys[pygame.K_0:pygame.K_0 + 10]):
            if pressed:
                self.multiplier = i
                break
        return

class Core:
    _game_count = 0
    def __init__(self):
        self.settings = Settings()
        self.events = Events()
        self.env = None
        return

    def new_game(self):
        self._game_count += 1
        self.env = Environment()

    def update(self):
        self.events.update()
        self.settings.update(self.events)
        self.env.update(self.events)

    def game_over(self):
        return self.env.game_over()

    def draw(self):
        surface = self.env.get_surface()
        surface.blit(self.get_info_surface(), (0, 0))
        return surface

    def get_info_surface(self):
        # list of individual lines
        text_surfaces = [
            text_to_surface(" Game: {}".format(self._game_count)),
            text_to_surface(" Score: {}".format(self.env.score)),
            text_to_surface(" Alive: {}".format(self.env.num_alive))
        ]

        # one big surface to combine all lines
        surface = pygame.Surface(
            (
                max(text_surface.get_width() for text_surface in text_surfaces),
                len(text_surfaces) * 12
            ),
            pygame.SRCALPHA
        )

        for i, text_surface in enumerate(text_surfaces):
            surface.blit(text_surface, (0, 12 * i))
        return surface
