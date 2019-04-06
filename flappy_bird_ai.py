import sys
import random
import pygame

import neat
from constants import *
from gameobjects import Ball, Wall, Buildings

# environment should be oblivious of whether ai is being used or not
class GameEnvironment:
    game_number = 0

    def __init__(self, num_balls=1, num_walls=5, colors=["blue"]):
        GameEnvironment.game_number += 1
        self.score = 0
        self.num_alive = num_balls
        self.balls = []
        self.walls = []
        self.surface = pygame.Surface(RESOLUTION)
        self.background_scroll = 0

        for _ in range(num_balls):
            self.add_ball(colors.pop(0))
        for _ in range(num_walls):
            self.add_wall()
        return

    def add_ball(self, color):
        self.balls.append(Ball(color))
        return

    def add_wall(self):
        # if no wall exists, add one at the right end of the screen
        # otherwise, add one some distance away from the right-most one
        if not self.walls:
            # x = WIDTH
            x = 0
        else:
            x = self.walls[-1].x + WALL_DISTANCE

        y = (HEIGHT // 2) + random.randint(-HOLE_Y_VARIANCE, HOLE_Y_VARIANCE)

        self.walls.append(Wall(x, y))
        return

    def remove_wall(self):
        self.walls.pop(0)
        return

    def cycle_update(self):
        # move game objects
        for ball in self.balls:
            ball.move()
            ball.accelerate()
        for wall in self.walls:
            wall.move()

        # remove a wall if it gets past the screen and add in a new one
        if GameCore.out_of_bounds(self.walls[0]):
            self.remove_wall()
            self.add_wall()

        # kill a ball if necessary
        for ball in self.balls:
            if ball.alive and \
                (GameCore.out_of_bounds(ball) or GameCore.collision(ball, self.walls)):
                # assign score to the ball before killing it off
                ball.score = self.score
                ball.alive = False
                self.num_alive -= 1

        self.score += 1
        return

    def event_update(self, events):
        if len(events.jumps) != len(self.balls):
            raise Exception("number of inputs doesn't match number of balls")
        # jump event
        for i, jump in enumerate(events.jumps):
            if self.balls[i].alive and jump[0]:
                self.balls[i].jump()
        return

    def check_game_over(self):
        return self.num_alive == 0

    def get_scores(self):
        return [ball.score for ball in self.balls]

    def text_renderer(self, text):
        return font.render(text, False, BLACK)

    def draw(self):
        self.surface.fill(SKY_BLUE)

        # render background first
        tile = Buildings()
        tile_size = tile_width, tile_height = tile.get_surface().get_size()
        surface_size = self.surface.get_size()
        for i in range((WIDTH // tile_width) + 2):
            self.surface.blit(tile.get_surface(), (
                i * tile_width + self.background_scroll,
                HEIGHT - tile_height
            ))
        self.background_scroll -= 1
        if self.background_scroll < -tile_width:
            self.background_scroll += tile_width

        # render game objects
        for ball in self.balls:
            if ball.alive:
                self.surface.blit(ball.get_surface(), ball.rect)
        for wall in self.walls:
        #    self.surface.blit(wall.image, wall.lower)
        #    self.surface.blit(wall.image, wall.upper)
            self.surface.blit(wall.get_surface(), wall.rect)

        # render info text
        game_number_text = self.text_renderer(" Game: {}".format(self.game_number))
        score_text = self.text_renderer(" Score: {}".format(self.score))
        alive_text = self.text_renderer(" Alive: {}".format(self.num_alive))

        self.surface.blit(game_number_text, (0, 0))
        self.surface.blit(score_text, (0, 12))
        self.surface.blit(alive_text, (0, 24))
        return self.surface

class GameSettings:
    tickrate = TICKRATE
    num_balls = 1

    @classmethod
    def set_num_balls(cls, num_balls):
        cls.num_balls = num_balls

    @classmethod
    def set_tickrate(cls, multiplier):
        if multiplier is not None:
            cls.tickrate = TICKRATE * multiplier

class GameCore:
    @staticmethod
    def out_of_bounds(game_object):
        if isinstance(game_object, Ball):
            return (game_object.rect.top < 0) or (game_object.rect.bottom > HEIGHT)
        elif isinstance(game_object, Wall):
            return game_object.rect.right < 0
        else:
            return False

    @staticmethod
    def collision(ball, walls):
        # for the current setup, we only need to check with the first wall
        wall = walls[0]
        if ball.rect.right >= wall.hole_rect.left and \
            ball.rect.left <= wall.hole_rect.right:
            return ball.rect.bottom >= wall.hole_rect.bottom or \
                ball.rect.top <= wall.hole_rect.top
        else:
            return False

    @staticmethod
    def new_game(colors):
        return GameEnvironment(num_balls=GameSettings.num_balls, colors=colors)

class EventHandler:
    def __init__(self):
        self.multiplier = 1
        self.jumps = [[False]]
        return

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

# game specific neat interface
class NeatInterface:
    # game specific variables
    _num_inputs = 6
    _num_outputs = 1

    def __init__(self):
        self.population = neat.Population(self._num_inputs, self._num_outputs)
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
    settings = GameSettings
    core = GameCore

    # initialize game before startings
    ai = ""
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        ai = "neat"
        interface = NeatInterface()
        settings.set_num_balls(num_balls=neat.Population.pop_size)
        env = core.new_game(interface.get_colors())
    else:
        env = core.new_game(colors=[get_color()])
    events = EventHandler()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(settings.tickrate)

        # close the game and terminate process
        if events.quit_event():
            sys.exit()

        # update game state
        env.cycle_update()

        # handle key press events
        events.key_events()

        # override inputs if ai is running
        if ai == "neat":
            inputs = interface.get_inputs(env)
            events.jumps = interface.get_outputs(inputs)
        env.event_update(events)
        settings.set_tickrate(events.multiplier)

        # check for game over
        if env.check_game_over():
            if ai == "neat":
                # create next generation for the population
                scores = env.get_scores()
                interface.score_population(scores)
                interface.evolve_population()
                env = GameCore.new_game(colors=interface.get_colors())
            else:
                env = GameCore.new_game(colors=[get_color()])
            continue

        # draw screen
        surface = env.draw()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        # todo: create additional info layer if ai is enabled
