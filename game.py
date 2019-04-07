import sys
import pygame

import lib
import neatinterface
from constants import *

if __name__ == "__main__":
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * ZOOM_LEVEL, HEIGHT * ZOOM_LEVEL))
    clock = pygame.time.Clock()

    # aliasing static classes
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        core = neatinterface.NeatCore()
    else:
        core = lib.Core()

    core.new_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(core.settings.tickrate)

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
