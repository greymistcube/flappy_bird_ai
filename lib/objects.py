import random
import pygame

from lib.settings import Settings
from lib.constants import WIDTH, HEIGHT
from lib.constants import START_POSITION, GRAVITY, MOVE_SPEED
from lib.constants import HOLE_SIZE
from lib.constants import WALL_SPEED, CLOUD_SPEED

pygame.init()
settings = Settings()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Ball:
    # default image for size reference
    __image = load_image("./rsc/img/blue_ball_falling.png")
    # lazy implementation of colored balls
    __images = {
        "blue_jumping": load_image("./rsc/img/blue_ball_jumping.png"),
        "blue_falling": load_image("./rsc/img/blue_ball_falling.png"),
        "green_jumping": load_image("./rsc/img/green_ball_jumping.png"),
        "green_falling": load_image("./rsc/img/green_ball_falling.png"),
        "yellow_jumping": load_image("./rsc/img/yellow_ball_jumping.png"),
        "yellow_falling": load_image("./rsc/img/yellow_ball_falling.png"),
        "red_jumping": load_image("./rsc/img/red_ball_jumping.png"),
        "red_falling": load_image("./rsc/img/red_ball_falling.png"),
    }
    __colors = ["blue", "green", "yellow", "red"]

    def __init__(self, color=None):
        self.rect = self.__image.get_rect()
        # randomize color if it is not given
        if color is None:
            self.color = random.choice(self.__colors)
        else:
            self.color = color
        self.x, self.y = START_POSITION
        self.rect.center = (self.x, self.y)
        self.velocity = 0.0
        self.score = 0
        self.alive = True
        self.jump_state = False
        return

    def update(self, events):
        if events.jump:
            self.jump()
        return

    def move(self):
        # center should be used instead of move method
        # otherwise misalignment becomes a problem down the line
        self.y = self.y + self.velocity
        self.rect.center = (self.x, self.y)
        return

    def accelerate(self):
        self.velocity += + GRAVITY
        return

    def jump(self):
        self.velocity = settings.jump_velocity

    def get_surface(self):
        if self.velocity < 0:
            state = "jumping"
        else:
            state = "falling"
        key = "{}_{}".format(self.color, state)

        return self.__images[key]

class Wall:
    # class initialization
    __image = load_image("./rsc/img/brick_wall.png")

    __width, __height = __image.get_size()
    __y_offset = (HOLE_SIZE + __height) // 2

    __surface = pygame.Surface(
        (__width, __height * 2 + HOLE_SIZE),
        pygame.SRCALPHA
    )
    __surface.blit(__image, (0, 0))
    __surface.blit(__image, (0, __height + HOLE_SIZE))

    __speed = MOVE_SPEED

    # here, (x, y) correspond to the center of the hole in a wall
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.__surface.get_rect()
        self.hole_rect = pygame.Rect(0, 0, self.__surface.get_width(), HOLE_SIZE)
        self.rect.center = self.hole_rect.center = (self.x, self.y)
        return

    def move(self):
        self.x += self.__speed
        self.rect.center = self.hole_rect.center = (self.x, self.y)
        return

    def get_surface(self):
        return self.__surface

class Buildings:
    __image = load_image("./rsc/img/buildings.png")
    __tile_width, __tile_height = __image.get_size()
    __num_tiles = (WIDTH // __tile_width) + 2
    __surface = pygame.Surface(
        (__tile_width * __num_tiles, __tile_height),
        pygame.SRCALPHA
    )

    for i in range(__num_tiles):
        __surface.blit(__image, (__tile_width * i, 0))

    def __init__(self, x=0):
        self.x = x
        self.y = HEIGHT - self.__tile_height
        self.rect = self.__surface.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def move(self):
        self.x += WALL_SPEED
        if self.x <= -self.__tile_width:
            self.x += self.__tile_width
        self.rect.left = self.x

    def get_surface(self):
        return self.__surface

class Cloud:
    __image = load_image("./rsc/img/cloud.png")

    def __init__(self):
        self.x = random.randint(0, WIDTH + self.__image.get_width())
        self.y = random.randint(
            int(HEIGHT * (1/8)),
            int(HEIGHT * (1/2))
        )
        self.rect = self.__image.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self):
        self.x += CLOUD_SPEED
        self.rect.center = (self.x, self.y)

    def get_surface(self):
        return self.__image
