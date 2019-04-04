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
        if self.walls[0].out_of_bounds():
            self.remove_wall()
            self.add_wall()

        # kill a ball if necessary
        for ball in self.balls:
            if ball.alive and \
                (ball.out_of_bounds() or GameCore.check_collision(ball, self.walls)):
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
    @staticmethod
    def check_collision(ball, walls):
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

def get_inputs(env):
    inputs = []
    for ball in env.balls:
        # skip dead balls
        if ball.alive:
            # get the next wall
            if env.walls[0].lower.right > ball.rect.left:
                next_wall = env.walls[0]
            else:
                next_wall = env.walls[1]
            # append normalized input
            inputs.append([
                ball.y / HEIGHT,
                ball.velocity / 10,
                next_wall.y / HEIGHT
            ])
        else:
            inputs.append([0, 0, 0])
    return inputs

def get_outputs(population, inputs):
    return population.predicts(inputs)

def get_scores(env):
    scores = []
    for ball in env.balls:
        scores.append(ball.score)
    return scores

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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * ZOOM_LEVEL, HEIGHT * ZOOM_LEVEL))
    clock = pygame.time.Clock()
    font = pygame.font.Font("./munro.ttf", 10)

    # initialize game before starting
    ai = ""
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        ai = "neat"
        population = neat.Population(num_inputs=3, num_outputs=1)
        GameSettings.set_num_balls(num_balls=neat.Population.pop_size)
    env = GameCore.new_game()
    events = EventHandler()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(GameSettings.tickrate)

        # close the game and terminate process
        if events.quit_event():
            sys.exit()

        # update game state
        env.cycle_update()

        # handle key press events
        events.key_events()

        # override inputs if ai is running
        if ai == "neat":
            inputs = get_inputs(env)
            events.jumps = get_outputs(population, inputs)
        env.event_update(events)
        GameSettings.set_tickrate(events.multiplier)

        # check for game over
        if env.check_game_over():
            if ai == "neat":
                # create next generation for the population
                scores = get_scores(env)
                population.score_genomes(scores)
                population.evolve()

                # just some debug info
                print("generation: " + str(population.generation))
                print("final score: " + str(env.score))
            env = GameCore.new_game()
            continue

        # draw screen
        surface = env.draw()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        # todo: create additional info layer if ai is enabled
