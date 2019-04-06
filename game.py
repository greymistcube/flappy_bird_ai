import sys
import random
import pygame

import lib
import neat
from constants import *

# game specific neat interface
class NeatInterface:
    # game specific variables
    _num_inputs = 6
    _num_outputs = 1

    def __init__(self):
        self.core = lib.Core()
        self.population = neat.Population(self._num_inputs, self._num_outputs)
        self.core.settings.set_num_balls(self.population.pop_size)
        return

    # logic is bit complicated here
    # pylint gets bit screwy due to nested lambdas with list comprehension
    def get_inputs(self, env):
        return [
            self.to_input(ball, env.walls) for ball in env.balls
        ]

    def to_input(self, ball, walls):
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
            return [0] * self._num_inputs

    def get_outputs(self, inputs):
        return self.population.predicts(inputs)

    def score_population(self, scores):
        self.population.score_genomes(scores)

    def evolve_population(self):
        self.population.evolve()

    def get_colors(self):
        colors = []
        for genome in self.population.genomes:
            if genome.genome_type == "survived":
                colors.append("blue")
            elif genome.genome_type == "mutated":
                colors.append("green")
            elif genome.genome_type == "bred":
                colors.append("yellow")
            else:
                colors.append("red")
        return colors

def get_color():
    return random.choice(["blue", "green", "yellow", "red"])

if __name__ == "__main__":
    pygame.init()

    # pygame initialization
    screen = pygame.display.set_mode((WIDTH * ZOOM_LEVEL, HEIGHT * ZOOM_LEVEL))
    clock = pygame.time.Clock()
    font = pygame.font.Font("./rsc/font/munro.ttf", 10)

    # aliasing static classes
    ai = ""
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        ai == "neat"
        interface = NeatInterface()
        core = interface.core
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
        # todo: create additional info layer if ai is enabled
