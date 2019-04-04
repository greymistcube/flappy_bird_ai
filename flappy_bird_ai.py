import sys
import random
import pygame
import neat

from constants import *
from gameobjects import Ball, Wall

# the environment should be oblivious of whether ai is being used or not
class GameEnvironment:
    def __init__(self, num_balls=1, num_walls=5):
        self.score = 0
        self.num_alive = num_balls
        self.balls = []
        self.walls = []
        self.surface = pygame.Surface(RESOLUTION)
        for _ in range(num_balls):
            self.add_ball()
        for _ in range(num_walls):
            self.add_wall()
        return

    def add_ball(self):
        self.balls.append(Ball())
        return

    def add_wall(self):
        # if no wall exists, add one at the right end of the screen
        # otherwise, add one some distance away from the right-most one
        if not self.walls:
            x = WIDTH
        else:
            x = self.walls[-1].x + WALL_DISTANCE

        variance = random.randint(-HOLE_Y_VARIANCE, HOLE_Y_VARIANCE)
        y = (HEIGHT // 2) + variance

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
        # jump event
        for i, jump in enumerate(events.jumps):
            if self.balls[i].alive and jump[0]:
                self.balls[i].jump()
        return

    def check_game_over(self):
        return self.num_alive == 0

    def get_scores(self):
        return [ball.score for ball in self.balls]

    def draw(self):
        # render game objects
        self.surface.fill(WHITE)
        for ball in self.balls:
            if ball.alive:
                self.surface.blit(ball.get_image(), ball.rect)
        for wall in self.walls:
            self.surface.blit(wall.image, wall.lower)
            self.surface.blit(wall.image, wall.upper)

        # render info text
        score_text = font.render(" Score: " + str(self.score), False, BLACK)
        alive_text = font.render(" Alive: " + str(self.num_alive), False, BLACK)
        self.surface.blit(score_text, (0, 0))
        self.surface.blit(alive_text, (0, 12))
        return self.surface

class GameCore:
    def __init__(self):
        return

    @staticmethod
    def out_of_bounds(game_object):
        if isinstance(game_object, Ball):
            return (game_object.rect.top < 0) or (game_object.rect.bottom > HEIGHT)
        elif isinstance(game_object, Wall):
            return game_object.lower.right < 0
        else:
            return False

    @staticmethod
    def collision(ball, walls):
        # for the current setup, we only need to check with the first wall
        wall = walls[0]
        if ball.rect.right >= wall.lower.left and \
            ball.rect.left <= wall.lower.right:
            return ball.rect.bottom >= wall.lower.top or \
                ball.rect.top <= wall.upper.bottom
        else:
            return False

    @staticmethod
    def new_game():
        return GameEnvironment(num_balls=GameSettings.num_balls)

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
    def __init__(self, num_inputs, num_outputs):
        self.population = neat.Population(
            num_inputs=num_inputs,
            num_outputs=num_outputs
        )
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        return

    # logic is bit complicated here
    # pylint gets bit screwy due to nested lambdas with list comprehension
    def get_inputs(self, env):
        to_input = lambda ball, wall: [
            ball.velocity / 10,
            ball.y / HEIGHT,
            wall.y / HEIGHT
        ] if ball.alive else [0] * self.num_inputs

        next_wall = lambda ball, walls: walls[
            (walls[0].lower.right < ball.rect.left) * 1
        ]

        return [
            to_input(ball, next_wall(ball, env.walls)) for ball in env.balls
        ]

    def get_outputs(self, inputs):
        return self.population.predicts(inputs)

    def score_population(self, scores):
        self.population.score_genomes(scores)

    def evolve_population(self):
        self.population.evolve()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * ZOOM_LEVEL, HEIGHT * ZOOM_LEVEL))
    clock = pygame.time.Clock()
    font = pygame.font.Font("./munro.ttf", 10)

    # aliasing static classes
    settings = GameSettings
    core = GameCore

    # initialize game before starting
    ai = ""
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        ai = "neat"
        interface = NeatInterface(num_inputs=3, num_outputs=1)
        settings.set_num_balls(num_balls=neat.Population.pop_size)
    env = core.new_game()
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

                # just some debug info
                print("generation: " + str(interface.population.generation))
                print("final score: " + str(env.score))
            env = GameCore.new_game()
            continue

        # draw screen
        surface = env.draw()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        # todo: create additional info layer if ai is enabled
