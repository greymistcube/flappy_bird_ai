import pygame

import lib
from lib.settings import Settings
from lib.constants import WIDTH, HEIGHT
import argparser

import neatinterface

if __name__ == "__main__":
    args = argparser.get_args()

    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * args.z, HEIGHT * args.z))
    clock = pygame.time.Clock()

    settings = Settings(args)
    if args.ai == "neat":
        core = neatinterface.NeatCore()
    else:
        core = lib.Core()
    core.new_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(settings.tickrate)

        # update game state
        core.update()

        if core.game_over():
            core.new_game()
            continue

        # draw screen
        surface = core.draw()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
