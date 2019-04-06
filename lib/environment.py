import random
import pygame
from lib.objects import Ball, Wall, Buildings

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

pygame.font.init()
font = pygame.font.Font("./rsc/font/munro.ttf", 10)

def out_of_bounds(object):
    if isinstance(object, Ball):
        return (object.rect.top < 0) or (object.rect.bottom > HEIGHT)
    elif isinstance(object, Wall):
        return object.rect.right < 0
    else:
        return False

def collision(ball, walls):
    # for the current setup, we only need to check with the first wall
    wall = walls[0]
    if ball.rect.right >= wall.hole_rect.left and \
        ball.rect.left <= wall.hole_rect.right:
        return ball.rect.bottom >= wall.hole_rect.bottom or \
            ball.rect.top <= wall.hole_rect.top
    else:
        return False

# environment should be oblivious of whether ai is being used or not
class Environment:
    _game_count = 0

    def __init__(self, num_balls=1, num_walls=5, colors=["blue"]):
        Environment._game_count += 1
        self.score = 0
        self.num_alive = num_balls
        self.balls = []
        self.walls = []
        self.surface = pygame.Surface(RESOLUTION)
        self.background_scroll = 0

        for i in range(num_balls):
            self.add_ball(colors[i])
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

    def update(self, events):
        self.cycle_update()
        self.event_update(events)

    def cycle_update(self):
        # move game objects
        for ball in self.balls:
            ball.move()
            ball.accelerate()
        for wall in self.walls:
            wall.move()

        # remove a wall if it gets past the screen and add in a new one
        if out_of_bounds(self.walls[0]):
            self.remove_wall()
            self.add_wall()

        # kill a ball if necessary
        for ball in self.balls:
            if ball.alive and \
                (out_of_bounds(ball) or collision(ball, self.walls)):
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

    def game_over(self):
        return self.num_alive == 0

    def get_scores(self):
        return [ball.score for ball in self.balls]

    def text_renderer(self, text):
        global font
        return font.render(text, False, BLACK)

    def get_surface(self):
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
        game_number_text = self.text_renderer(" Game: {}".format(self._game_count))
        score_text = self.text_renderer(" Score: {}".format(self.score))
        alive_text = self.text_renderer(" Alive: {}".format(self.num_alive))

        self.surface.blit(game_number_text, (0, 0))
        self.surface.blit(score_text, (0, 12))
        self.surface.blit(alive_text, (0, 24))
        return self.surface
