import sys
import pygame

import lib
import neat
from constants import *

# game specific neat interface
class NeatCore(lib.Core):
    # game specific variables
    _num_input = 6
    _num_output = 1

    _genome_to_color = {
        "survived": "blue",
        "mutated": "green",
        "bred": "yellow",
        "diverged": "red"
    }

    # overriden methods
    def __init__(self):
        super().__init__()
        self.population = neat.Population(self._num_input, self._num_output)
        # set num_balls to population size
        self.settings.set_num_balls(self.population.pop_size)
        return

    def new_balls(self):
        colors = self.get_colors()
        return [lib.objects.Ball(color) for color in colors]

    def update(self):
        self.events.update()
        self.settings.update(self.events)
        # this part overrides keyboard evaluated jumps
        # before calling the update for the environment
        self.events.jumps = [
            y[0]
            for y in self.get_Y(self.get_X())
        ]
        self.env.update(self.events)

    def game_over(self):
        if self.env.game_over():
            scores = [ball.score for ball in self.env.balls]
            self.population.score_genomes(scores)
            self.population.evolve_population()
            return True
        else:
            return False

    def get_info_surface(self):
        num_survived = sum([
            ball.color == "blue" and ball.alive
            for ball in self.env.balls
        ])
        num_mutated = sum([
            ball.color == "green" and ball.alive
            for ball in self.env.balls
        ])
        num_bred = sum([
            ball.color == "yellow" and ball.alive
            for ball in self.env.balls
        ])

        texts = [
            " Game: {}".format(self.game_count),
            " Score: {}".format(self.env.score),
            " Alive: {}".format(self.env.num_alive),
            " (Blue) Survived: {}".format(num_survived),
            " (Green) Mutated: {}".format(num_mutated),
            " (Yellow) Bred: {}".format(num_bred)
        ]

        return self.text_renderer.texts_to_surface(texts)

    # extended methods
    def get_x(self, ball, walls):
        if ball.alive:
            return [
                ball.velocity / 100,
                ball.y / HEIGHT,
                walls[0].x / WIDTH,
                walls[0].y / HEIGHT,
                walls[1].x / WIDTH,
                walls[1].y / HEIGHT
            ]
        else:
            return [0] * self._num_input

    def get_X(self):
        return [
            self.get_x(ball, self.env.walls) for ball in self.env.balls
        ]

    def get_Y(self, X):
        return self.population.predicts(X)

    def get_colors(self):
        return [
            self._genome_to_color[genome.genome_type]
            for genome in self.population.genomes
        ]

if __name__ == "__main__":
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * ZOOM_LEVEL, HEIGHT * ZOOM_LEVEL))
    clock = pygame.time.Clock()

    # aliasing static classes
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        core = NeatCore()
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
