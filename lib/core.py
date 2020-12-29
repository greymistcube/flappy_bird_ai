import sys
# import random
import pygame

from lib.settings import Settings
from lib.environment import Environment
from lib.objects import Ball
from lib.constants import BLACK

pygame.init()
settings = Settings()

class TextRenderer:
    __font = pygame.font.Font("./rsc/font/monogram.ttf", 16)
    __line_height = __font.get_linesize()

    # render a single line of text
    def text_to_surface(self, text):
        return self.__font.render(text, False, BLACK)

    # render multiple lines of texts
    def texts_to_surface(self, texts):
        text_surfaces = [self.text_to_surface(text) for text in texts]
        surface = pygame.Surface(
            (
                max(text_surface.get_width() for text_surface in text_surfaces),
                len(text_surfaces) * self.__line_height
            ),
            pygame.SRCALPHA
        )
        for i, text_surface in enumerate(text_surfaces):
            surface.blit(text_surface, (0, self.__line_height * i))
        return surface

class Events:
    def __init__(self):
        self.multiplier = 1
        self.jump = False
        self.info = False
        return

    def update(self):
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.info = not self.info

        # check for pressed keys and update variables accordingly
        pressed_keys = pygame.key.get_pressed()
        self.jump = pressed_keys[pygame.K_SPACE]

        for i in range(10):
            if pressed_keys[pygame.K_0 + i]:
                self.multiplier = i
                break
        return

class Core:
    def __init__(self):
        self.game_count = 0
        self.events = Events()
        self.text_renderer = TextRenderer()

        # empty declarations for linting
        self.balls = None
        self.env = None
        return

    def new_game(self):
        self.game_count += 1
        self.balls = self.new_balls()
        self.env = Environment(self.balls)

    def new_balls(self):
        return [Ball() for _ in range(settings.num_balls)]

    def update(self):
        self.events.update()
        settings.update(self.events)
        # only cycle through balls alive in the environment for optimization
        for ball in self.env.balls:
            ball.update(self.events)
        self.env.update(self.events)

    def game_over(self):
        return self.env.game_over()

    def draw(self):
        surface = self.env.get_surface()
        if self.events.info:
            surface.blit(self.get_info_surface(), (0, 0))
        return surface

    def get_info_surface(self):
        texts = [
            " Game: {}".format(self.game_count),
            " Score: {}".format(self.env.score),
            " Alive: {}".format(self.env.num_alive)
        ]

        return self.text_renderer.texts_to_surface(texts)
